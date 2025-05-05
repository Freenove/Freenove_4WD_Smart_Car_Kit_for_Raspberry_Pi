## binhoHostAdapter Python Library
##
## Jonathan Georgino <jonathan@binho.io>
## Binho LLC
## www.binho.io

import threading
import queue
import signal
import sys
import serial
import os
import enum

class SerialPortManager(threading.Thread):

        serialPort = None
        txdQueue = None
        rxdQueue = None
        intQueue = None
        stopper = None
        inBridgeMode = False

        def __init__(self, serialPort, txdQueue, rxdQueue, intQueue, stopper):
            super().__init__()
            self.serialPort = serialPort
            self.txdQueue = txdQueue
            self.rxdQueue = rxdQueue
            self.intQueue = intQueue
            self.stopper = stopper
            self.exception = None
            self.daemon = True

        def run(self):

            try:
                comport = serial.Serial(self.serialPort, baudrate=1000000, timeout=0.025, write_timeout=0.05)
            except:
                self.stopper.set()

            while not self.stopper.is_set():

                try:
                    if self.inBridgeMode:

                        if comport.in_waiting > 0:
                            receivedData = comport.read().decode("utf-8")
                            self.rxdQueue.put(receivedData)

                        if self.txdQueue.empty() == False:
                            serialData = self.txdQueue.get()
                            comport.write(serialData.encode('utf-8'))
                    else:

                        if comport.in_waiting > 0:
                            receivedData = comport.readline().strip().decode("utf-8")

                            if(len(receivedData) > 0):

                                if receivedData[0] == '!':
                                    self.intQueue.put(receivedData)
                                elif receivedData[0] == '-':
                                    self.rxdQueue.put(receivedData)

                        if self.txdQueue.empty() == False:
                            serialCommand = self.txdQueue.get() + '\n'
                            comport.write(serialCommand.encode("utf-8"))

                except Exception as e:
                    self.stopper.set()
                    self.exception = e
                    # print('Comm Error!')

        def get_exception(self):
            return self.exception

        def startUartBridge(self):
            self.inBridgeMode = True

        def stopUartBridge(self):
            self.inBridgeMode = False


class SignalHandler:
    """
    The object that will handle signals and stop the worker threads.
    """

    #: The stop event that's shared by this handler and threads.
    stopper = None

    #: The pool of worker threads
    workers = None

    def __init__(self, stopper, manager):
        self.stopper = stopper
        self.manager = manager

    def __call__(self, signum, frame):
        """
        This will be called by the python signal module
        https://docs.python.org/3/library/signal.html#signal.signal
        """
        self.stopper.set()

        self.manager.join()

        sys.exit(0)

    def sendStop(self):

        self.stopper.set()

        self.manager.join()


class binhoException(Exception):
    pass


class oneWireCmd(enum.Enum):
    """Enum for exchangeBytes1WIRE"""
    NONE = "NONE"
    SELECT = "SELECT"
    SKIP = "SKIP"


class binhoHostAdapter:

    # Constructor, needs a serial port as a parameter

    def __init__(self, serialPort):

        self.serialPort = serialPort
        self.handler = None
        self.manager = None
        self.interrupts = None
        self._stopper = None
        self._txdQueue = None
        self._rxdQueue = None
        self._intQueue = None
        self._debug = os.getenv('BINHO_NOVA_DEBUG')

        try:
            comport = serial.Serial(serialPort, baudrate=1000000, timeout=0.025, write_timeout=0.05)
            comport.close()
        except:
            print("Error: Unable to connect to Binho device on port " + serialPort)
            print("Cannot continue script... Exiting")
            sys.exit(1)

        self.interrupts = set()

        self._stopper = threading.Event()
        self._txdQueue = queue.Queue()
        self._rxdQueue = queue.Queue()
        self._intQueue = queue.Queue()

        # we need to keep track of the workers but not start them yet
        #workers = [StatusChecker(url_queue, result_queue, stopper) for i in range(num_workers)]
        self.manager = SerialPortManager(self.serialPort, self._txdQueue, self._rxdQueue, self._intQueue, self._stopper)

        # create our signal handler and connect it
        self.handler = SignalHandler(self._stopper, self.manager)
        signal.signal(signal.SIGINT, self.handler)

        # start the threads!
        self.manager.daemon = True

        self.manager.start()

    # Destructor

    def __del__(self):

        if self.handler is not None:
            try:
                self.handler.sendStop()
            except:
                pass

    # Private functions
    
    def _sendCommand(self, command):
        if self._debug is not None:
            print(command)
        self._txdQueue.put(command)

    def _readResponse(self):

        result = '[ERROR]'

        if self.manager.is_alive():
            if not self.manager.get_exception():
                result = self._rxdQueue.get()
        else:
            print('Connection with Device Lost!')
            self.handler.sendStop()

        if self._debug is not None:
            print(result)
        return result

    def _checkInterrupts(self):

        while self._intQueue.empty() == False:
            self.interrupts.add(self._intQueue.get())

    def _checkDeviceSuccess(self, ret_str):
        if ret_str == '-OK':
            return True
        elif ret_str == '-NG':
            return False
        else:
            raise binhoException(f'Invalid command response: {ret_str}')

    # Public functions

    # Communication Management

    def open(self):

        self.interrupts.clear()
        self.manager.start()

    def isConnected(self):

        return self.manager.is_alive()

    def isCommError(self):

        e = self.manager.get_exception()

        if e:
            return True
        else:
            return False

    def close(self):

        self.handler.sendStop()

    def interruptCount(self):

        self._checkInterrupts()

        return len(self.interrupts)

    def interruptCheck(self, interrupt):

        self._checkInterrupts()

        if interrupt in self.interrupts:
            return True
        else:
            return False

    def interruptClear(self, interrupt):

        self.interrupts.discard(interrupt)

    def interruptClearAll(self):

        self.interrupts.clear()

    def getInterrupts(self):

        self._checkInterrupts()

        return self.interrupts.copy()

    ## DEVICE COMMANDS

    def echo(self):

        self._sendCommand('+ECHO')
        result = self._readResponse()

        return result

    def ping(self):

        self._sendCommand('+PING')
        result = self._readResponse()

        return result

    ## GET/SET OperationMode
    ##
    ## parameters:
    ##  mode        I2C|IIC, SPI, IO

    def setOperationMode(self, coreIndex, mode):

        self._sendCommand('+MODE ' + str(coreIndex) + ' ' + mode)
        result = self._readResponse()

        return result

    def getOperationMode(self, coreIndex):

        self._sendCommand('+MODE ' + str(coreIndex) + ' ?')
        result = self._readResponse()

        return result

    def setNumericalBase(self, base):

        self._sendCommand('+BASE ' + str(base))
        result = self._readResponse()

        return result

    def getNumericalBase(self):

        self._sendCommand('+BASE ?')
        result = self._readResponse()

        return result

    def setLEDRGB(self, red, green, blue):

        self._sendCommand('+LED ' + str(red) + ' ' + str(green) + ' ' + str(blue))
        result = self._readResponse()

        return result

    def setLEDColor(self, color):

        self._sendCommand('+LED ' + color)
        result = self._readResponse()

        return result

    def getFirmwareVer(self):

        self._sendCommand('+FWVER')
        result = self._readResponse()

        return result

    def getHardwareVer(self):

        self._sendCommand('+HWVER')
        result = self._readResponse()

        return result

    def getCommandVer(self):

        self._sendCommand('+CMDVER')
        result = self._readResponse()

        return result

    def resetToBtldr(self):

        self._sendCommand('+BTLDR')
        result = self._readResponse()

        return result

    def reset(self):

        self._sendCommand('+RESET')
        result = self._readResponse()

        return result

    def getDeviceID(self):

        self._sendCommand('+ID')
        result = self._readResponse()

        return result

    ## BUFFER COMMANDS

    def clearBuffer(self, bufferIndex):

        self._sendCommand('BUF' + str(bufferIndex) + ' CLEAR')
        result = self._readResponse()

        return result

    def addByteToBuffer(self, bufferIndex, value):

        self._sendCommand('BUF' + str(bufferIndex) + ' ADD ' + str(value))
        result = self._readResponse()

        return result

    def readBuffer(self, bufferIndex, numBytes):

        self._sendCommand('BUF' + str(bufferIndex) + ' READ ' + str(numBytes))
        result = self._readResponse()

        return result

    def writeToBuffer(self, bufferIndex, startIndex, data):

        bufferData = ''

        for x in data:
            bufferData += ' ' + str(x)

        self._sendCommand('BUF' + str(bufferIndex) + ' WRITE ' + str(startIndex) + bufferData)
        result = self._readResponse()

        return result

    ## I2C COMMANDS

    def setClockI2C(self, i2cIndex, clock):

        self._sendCommand('I2C' + str(i2cIndex) + ' CLK ' + str(clock))
        result = self._readResponse()

        return result

    def getClockI2C(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' CLK ?')
        result = self._readResponse()

        return result

    def setPullUpStateI2C(self, i2cIndex, pullUpState):

        self._sendCommand('I2C' + str(i2cIndex) + ' PULL ' + str(pullUpState))
        result = self._readResponse()

        return result

    def getPullUpStateI2C(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' PULL ?')
        result = self._readResponse()

        return result

    def scanBusI2C(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' SCAN')
        result = self._readResponse()

        return result

    def scanAddrI2C(self, i2cIndex, address):

        self._sendCommand('I2C' + str(i2cIndex) + ' SCAN ' + str(address))
        result = self._readResponse()

        return result

    def writeI2C(self, i2cIndex, address, startingRegister, data):

        dataPacket = ''

        for x in data:
            dataPacket += ' ' + str(x)

        self._sendCommand('I2C' + str(i2cIndex) + ' WRITE ' + str(address) + ' ' + str(startingRegister) + dataPacket)
        result = self._readResponse()

        return result

    def writeByteI2C(self, i2cIndex, data):

        self._sendCommand('I2C' + str(i2cIndex) + ' WRITE ' + str(data))
        result = self._readResponse()

        return result

    def readByteI2C(self, i2cIndex, address):

        self._sendCommand('I2C' + str(i2cIndex) + ' REQ ' + str(address) + ' 1')
        result = self._readResponse()

        return result

    def readBytesI2C(self, i2cIndex, address, numBytes):

        self._sendCommand('I2C' + str(i2cIndex) + ' REQ ' + str(address) + ' ' + str(numBytes))
        result = self._readResponse()

        return result

    def readI2C(self, i2cIndex, address, startingRegister, numBytes):

        self._sendCommand('I2C' + str(i2cIndex) + ' READ ' + str(address) + ' ' + str(startingRegister) + ' ' + str(numBytes))
        result = self._readResponse()

        return result

    def getReceivedDataI2C(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' READ')
        result = self._readResponse()

        return result

    def writeFromBufferI2C(self, i2cIndex, numBytes):

        self._sendCommand('I2C' + str(i2cIndex) + ' WRITE BUF0 ' + str(numBytes))
        result = self._readResponse()

        return result

    def readToBufferI2C(self, i2cIndex, address, numBytes):

        self._sendCommand('I2C' + str(i2cIndex) + ' REQ ' + str(address) + ' BUF0 ' + str(numBytes))
        result = self._readResponse()

        return result

    def writeToReadFromI2C(self, i2cIndex, address, stop, numReadBytes, numWriteBytes, data):

        dataPacket = ''
        endStop = '1'

        if numWriteBytes > 0:
            for i in range(numWriteBytes):
                dataPacket += "{:02x}".format(data[i])
        else:
            dataPacket = '0'

        if stop == False:
            endStop = '0'

        self._sendCommand('I2C' + str(i2cIndex) + ' WHR ' + str(address) + ' ' + endStop + ' ' + str(numReadBytes) + ' ' + str(numWriteBytes) + ' ' + dataPacket)
        result = self._readResponse()

        return result

    def startI2C(self, i2cIndex, address):

        self._sendCommand('I2C' + str(i2cIndex) + ' START ' + str(address))
        result = self._readResponse()

        return result

    def endI2C(self, i2cIndex, repeat=False):

        if repeat == True:
            self._sendCommand('I2C' + str(i2cIndex) + ' END R')
        else:
            self._sendCommand('I2C' + str(i2cIndex) + ' END')

        result = self._readResponse()

        return result

    def setSlaveAddressI2C(self, i2cIndex, address):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE ' + str(address))
        result = self._readResponse()

        return result

    def getSlaveAddressI2C(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE ?')
        result = self._readResponse()

        return result

    def getSlaveRequestInterruptI2C(self, i2cIndex):

        result = self.interruptCheck('!I2C' + str(i2cIndex) + ' SLAVE RQ')

        return result

    def clearSlaveRequestInterruptI2C(self, i2cIndex):

        self.interruptClear('!I2C' + str(i2cIndex) + ' SLAVE RQ')

    def getSlaveReceiveInterruptI2C(self, i2cIndex):

        result = self.interruptCheck('!I2C' + str(i2cIndex) + ' SLAVE RX')

        return result

    def clearSlaveReceiveInterruptI2C(self, i2cIndex):

        self.interruptClear('!I2C' + str(i2cIndex) + ' SLAVE RX')

    def setSlaveRegisterI2C(self, i2cIndex, register, value):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE REG ' + str(register) + ' ' + str(value))
        result = self._readResponse()

        return result

    def getSlaveRegisterI2C(self, i2cIndex, register):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE REG ' + str(register) + ' ?')
        result = self._readResponse()

        return result

    def setSlaveReadMaskI2C(self, i2cIndex, register, value):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE READMASK ' + str(register) + ' ' + str(value))
        result = self._readResponse()

        return result

    def getSlaveReadMaskI2C(self, i2cIndex, register):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE READMASK ' + str(register) + ' ?')
        result = self._readResponse()

        return result

    def setSlaveWriteMaskI2C(self, i2cIndex, register, value):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE WRITEMASK ' + str(register) + ' ' + str(value))
        result = self._readResponse()

        return result

    def getSlaveWriteMaskI2C(self, i2cIndex, register):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE WRITEMASK ' + str(register) + ' ?')
        result = self._readResponse()

        return result

    def setSlaveModeI2C(self, i2cIndex, mode):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE MODE ' + str(mode))
        result = self._readResponse()

        return result

    def getSlaveModeI2C(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE MODE ' + '?')
        result = self._readResponse()

        return result

    def setSlaveRegisterCount(self, i2cIndex, registerCount):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE REGCNT ' + str(registerCount))
        result = self._readResponse()

        return result

    def getSlaveRegisterCount(self, i2cIndex):

        self._sendCommand('I2C' + str(i2cIndex) + ' SLAVE REGCNT ' + '?')
        result = self._readResponse()

        return result

    ## SPI COMMANDS

    def setClockSPI(self, spiIndex, clock):

        self._sendCommand('SPI' + str(spiIndex) + ' CLK ' + str(clock))
        result = self._readResponse()

        return result

    def getClockSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' CLK ?')
        result = self._readResponse()

        return result

    def setOrderSPI(self, spiIndex, order):

        self._sendCommand('SPI' + str(spiIndex) + ' ORDER ' + order)
        result = self._readResponse()

        return result

    def getOrderSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' ORDER ?')
        result = self._readResponse()

        return result

    def setModeSPI(self, spiIndex, mode):

        self._sendCommand('SPI' + str(spiIndex) + ' MODE ' + str(mode))
        result = self._readResponse()

        return result

    def getModeSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' MODE ?')
        result = self._readResponse()

        return result

    def getCpolSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' CPOL ?')
        result = self._readResponse()

        return result

    def getCphaSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' CPHA ?')
        result = self._readResponse()

        return result

    def setBitsPerTransferSPI(self, spiIndex, bits):

        self._sendCommand('SPI' + str(spiIndex) + ' TXBITS ' + str(bits))
        result = self._readResponse()

        return result

    def getBitsPerTransferSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' TXBITS ?')
        result = self._readResponse()

        return result

    def beginSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' BEGIN')
        result = self._readResponse()

        return result

    def transferSPI(self, spiIndex, data):

        self._sendCommand('SPI' + str(spiIndex) + ' TXRX ' + str(data))
        result = self._readResponse()

        return result

    def transferBufferSPI(self, spiIndex, numBytes):
        self._sendCommand('SPI' + str(spiIndex) + ' TXRX BUF0 ' + str(numBytes))
        result = self._readResponse()

        return result

    def writeToReadFromSPI(self, spiIndex, write, read, numBytes, data):

        dataPacket = ''
        writeOnlyFlag = '0'

        if write:
            if numBytes > 0:
                for i in range(numBytes):
                    dataPacket += "{:02x}".format(data[i])
            else:
                dataPacket = '0'
        else:
            # read only, keep writing the same value
            for i in range(numBytes):
                    dataPacket += "{:02x}".format(data)

        if read == False:
            writeOnlyFlag = '1'

        self._sendCommand('SPI' + str(spiIndex) + ' WHR ' + writeOnlyFlag + ' ' + str(numBytes) + ' ' + dataPacket)
        result = self._readResponse()
        #print(result)
        return result

    def endSPI(self, spiIndex):

        self._sendCommand('SPI' + str(spiIndex) + ' END')
        result = self._readResponse()

        return result

    ## UART COMMANDS

    def setBaudRateUART(self, uartIndex, baud):

        self._sendCommand('UART' + str(uartIndex) + ' BAUD ' + str(baud))
        result = self._readResponse()

        return result

    def getBaudRateUART(self, uartIndex):

        self._sendCommand('UART' + str(uartIndex) + ' BAUD ?')
        result = self._readResponse()

        return result

    def setDataBitsUART(self, uartIndex, databits):

        self._sendCommand('UART' + str(uartIndex) + ' DATABITS ' + str(databits))
        result = self._readResponse()

        return result

    def getDataBitsUART(self, uartIndex):

        self._sendCommand('UART' + str(uartIndex) + ' DATABITS ?')
        result = self._readResponse()

        return result

    def setParityUART(self, uartIndex, parity):

        self._sendCommand('UART' + str(uartIndex) + ' PARITY ' + str(parity))
        result = self._readResponse()

        return result

    def getParityUART(self, uartIndex):

        self._sendCommand('UART' + str(uartIndex) + ' PARITY ?')
        result = self._readResponse()

        return result

    def setStopBitsUART(self, uartIndex, stopbits):

        self._sendCommand('UART' + str(uartIndex) + ' STOPBITS ' + str(stopbits))
        result = self._readResponse()

        return result

    def getStopBitsUART(self, uartIndex):

        self._sendCommand('UART' + str(uartIndex) + ' STOPBITS ?')
        result = self._readResponse()

        return result

    def setEscapeSequenceUART(self, uartIndex, escape):

        self._sendCommand('UART' + str(uartIndex) + ' ESC ' + escape)
        result = self._readResponse()

        return result

    def getEscapeSequenceUART(self, uartIndex):

        self._sendCommand('UART' + str(uartIndex) + ' ESC ?')
        result = self._readResponse()

        return result

    def beginBridgeUART(self, uartIndex):

        self._sendCommand('UART' + str(uartIndex) + ' BEGIN')
        result = self._readResponse()

        self.manager.startUartBridge()

        return result

    def stopBridgeUART(self, sequence):

        self.manager.stopUartBridge()
        self._txdQueue.put(sequence)
        result = self._readResponse()

        return result

    def writeBridgeUART(self, data):

        self._txdQueue.put(data)

    def readBridgeUART(self):

        return self._rxdQueue.get()

    ## 1WIRE COMMANDS

    def begin1WIRE(self, pin, pullup=True, oneWireIndex=0):
        """
        This function starts the 1-WIRE Master on the given IO pin. The 1-Wire protocol can be used
        on any of the IO pins, however it is especially convenient to use it on IO0 and IO2 as the
        internal pull-up resistor can be used thus eliminating the need for an external pull-up resistor.

        :param pin: The binho pin to use for 1-Wire comms can be 0-4
        :type pin: int
        :param pullup: True or False, enable the pullup on the IO pin
        :type pullup: bool
        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """

        if pullup:
            self._sendCommand(f'1WIRE{oneWireIndex} BEGIN {pin} PULL')
        else:
            self._sendCommand(f'1WIRE{oneWireIndex} BEGIN {pin}')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire Begin received NAK')

    def reset1WIRE(self, oneWireIndex=0):
        """
        Send a 1-Wire reset pulse, return True if the binho receives a
        presence pulse False otherwise

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :return: True if the binho receives a presence pulse False otherwise
        :rtype: bool
        """

        self._sendCommand(f'1WIRE{oneWireIndex} RESET')

        return self._checkDeviceSuccess(self._readResponse())

    def writeByte1WIRE(self, data, oneWireIndex=0, powered=True):
        """
        Write a byte over 1-Wire

        :param data: Data byte to write
        :type data: int
        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :param powered: Leave 1-Wire power on after this command finsihes
        :type powered: bool
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """

        if not 0 <= data <= 255:
            raise binhoException(f'Data byte must be in range 0-255, not {data}')

        if powered:
            self._sendCommand(f'1WIRE{oneWireIndex} WRITE {data} POWER')
        else:
            self._sendCommand(f'1WIRE{oneWireIndex} WRITE {data}')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire Write received NAK')

    def readByte1WIRE(self, oneWireIndex=0):
        """
        Reads one byte over 1-Wire

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: Received byte
        :rtype: int
        """
        self._sendCommand(f'1WIRE{oneWireIndex} READ')
        result = self._readResponse()

        if result == '-NG':
            raise binhoException('Error executing 1-Wire Read received NAK')


        return int(result[15:], 16)

    def exchangeBytes1WIRE(self, oneWireCmd=oneWireCmd.NONE, bytesToWrite=None, bytesToRead=0, oneWireIndex=0):
        """
        Issues one of the following commands to the one wire bus:
            None (this is the default)
            Reset then Select ROM (requires a one wire address in the address buffer)
            Reset then Skip ROM
        Then writes bytesToWrite (max 1024) out to the bus
        Then reads bytesToRead (max 1024) from the bus

        :param oneWireCmd: 1-Wire command to send out on the bus
        :type oneWireCmd: oneWireCmd
        :param bytesToWrite: bytearray of bytes to write out to the 1-Wire bus after the 1-Wire Cmd
        :type bytesToWrite: bytearray
        :param bytesToRead: Number of bytes to read after writeing bytes
        :type bytesToRead: int
        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :return: A bytearray of bytes that were read out
        :rtype: bytearray
        """

        if len(bytesToWrite) > 1024:
            raise ValueError("WHR command can only write 1024 bytea at a time!")

        if bytesToRead > 1024:
            raise ValueError("WHR command can only read 1024 bytea at a time!")

        self._sendCommand(f'1WIRE{oneWireIndex} '
                          f'WHR {oneWireCmd.value} '
                          f'{bytesToRead} '
                          f'{len(bytesToWrite)} '
                          f'{"".join(f"{b:02x}" for b in bytesToWrite)}'
                    )

        result = self._readResponse()

        if bytesToRead == 0:
            if not result.startswith("-OK"):
                raise RuntimeError(f"Error Binho responded with {result}, not the expected \"-OK\"")
            else:
                return bytearray()
        else:
            if not result.startswith("-1WIRE0 RXD "):
                raise RuntimeError(f"Error Binho responded with {result}, not the expected \"-1WIRE0 RXD ...\"")
            else:
                return bytearray.fromhex(result[12:])

    def select1WIRE(self, oneWireIndex=0):
        """
        Select the device that was found as a result of the most recent SEARCH command

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """
        self._sendCommand(f'1WIRE{oneWireIndex} SELECT')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire Select received NAK')

    def skip1WIRE(self, oneWireIndex=0):
        """
        Skip the device selection process, if there is one device on the bus

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """
        self._sendCommand(f'1WIRE{oneWireIndex} SKIP')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire Skip received NAK')

    def depower1WIRE(self, oneWireIndex=0):
        """
        Power down the 1-WIRE bus

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """
        self._sendCommand(f'1WIRE{oneWireIndex} DEPOWER')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire depower received NAK')

    def getAddress1WIRE(self, oneWireIndex=0):
        """
        Returns the address that was found by performing a 1-Wire search

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: Bytearray of the address
        :rtype: bytearray
        """
        self._sendCommand(f'1WIRE{oneWireIndex} ADDR ?')
        result = self._readResponse()

        if result == '-NG':
            raise binhoException('Error executing 1-Wire Read received NAK')

        return bytearray.fromhex(result[13:].replace("0x", ""))

    def search1WIRE(self, oneWireIndex=0, normalSearch=True):
        """
        Begin the process of searching for devices on the 1-WIRE bus.
        The address of the found device will be stored in internal address buffer

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :param normalSearch: Whether to perform a normal search (returning all devices)
                                or only return alarming devices
        :type normalSearch: bool
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """
        if normalSearch:
            self._sendCommand(f'1WIRE{oneWireIndex} SEARCH')
        else:
            self._sendCommand(f'1WIRE{oneWireIndex} SEARCH COND')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire search received NAK')

    def resetSearch1WIRE(self, oneWireIndex=0):
        """
        Resets 1-Wire search so a new one can occur

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """
        self._sendCommand(f'1WIRE{oneWireIndex} SEARCH RESET')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire search reset received NAK')

    def targetSearch1WIRE(self, target, oneWireIndex=0):
        """
        Searches the 1-WIRE bus for devices belonging to a specific family code

        :param oneWireIndex: The 1-Wire index, 0 on the binho nova
        :type oneWireIndex: int
        :param target: 1-byte long device family code for which to search
        :type target: int
        :raises binhoException: if the command is unsuccessful
        :return: None
        :rtype: None
        """
        if not 0 <= target <= 255:
            raise binhoException(f'Target byte must be in range 0-255, not {target}')

        self._sendCommand(f'1WIRE{oneWireIndex} SEARCH {target}')

        if not self._checkDeviceSuccess(self._readResponse()):
            raise binhoException('Error executing 1-Wire target search received NAK')

    ## SWI COMMANDS

    def beginSWI(self, swiIndex, pin, pullup):

        if not pullup:
            self._sendCommand('SWI' + str(swiIndex) + ' BEGIN ' + str(pin))
        else:
            self._sendCommand('SWI' + str(swiIndex) + ' BEGIN ' + str(pin) + ' PULL')

        result = self._readResponse()

        return result

    def sendTokenSWI(self, swiIndex, token):

        self._sendCommand('SWI' + str(swiIndex) + ' TOKEN ' + str(token))
        result = self._readResponse()

        return result

    def sendFlagSWI(self, swiIndex, flag):

        self._sendCommand('SWI' + str(swiIndex) + ' FLAG ' + str(flag))
        result = self._readResponse()

        return result

    def sendCommandFlagSWI(self, swiIndex):

        self._sendCommand('SWI' + str(swiIndex) + ' FLAG COMMAND')
        result = self._readResponse()

        return result

    def sendTransmitFlagSWI(self, swiIndex):

        self._sendCommand('SWI' + str(swiIndex) + ' FLAG TRANSMIT')
        result = self._readResponse()

        return result

    def sendIdleFlagSWI(self, swiIndex):

        self._sendCommand('SWI' + str(swiIndex) + ' FLAG IDLE')
        result = self._readResponse()

        return result

    def sendSleepFlagSWI(self, swiIndex):

        self._sendCommand('SWI' + str(swiIndex) + ' FLAG SLEEP')
        result = self._readResponse()

        return result

    def transmitByteSWI(self, swiIndex, data):

        self._sendCommand('SWI' + str(swiIndex) + ' TX ' + str(data))
        result = self._readResponse()

        return result

    def receiveBytesSWI(self, swiIndex, count):

        self._sendCommand('SWI' + str(swiIndex) + ' RX ' + str(count))
        result = self._readResponse()

        return result

    def setPacketOpCodeSWI(self, swiIndex, opCode):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET OPCODE ' + str(opCode))
        result = self._readResponse()

        return result

    def setPacketParam1SWI(self, swiIndex, value):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET PARAM1 ' + str(value))
        result = self._readResponse()

        return result

    def setPacketParam2SWI(self, swiIndex, value):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET PARAM2 ' + str(value))
        result = self._readResponse()

        return result

    def setPacketDataSWI(self, swiIndex, index, value):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET DATA ' + str(index) + ' ' + str(value))
        result = self._readResponse()
        
        return result

    def setPacketDataFromBufferSWI(self, swiIndex, byteCount, bufferName):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET DATA ' + str(byteCount) + ' ' + str(bufferName))
        result = self._readResponse()

        return result

    def sendPacketSWI(self, swiIndex):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET SEND')
        result = self._readResponse()

        return result

    def clearPacketSWI(self, swiIndex):

        self._sendCommand('SWI' + str(swiIndex) + ' PACKET CLEAR')
        result = self._readResponse()

        return result

    ## IO COMMANDS

    ## GET/SET IOpinMode
    ##
    ## parameters:
    ##  ioNumber    0, 1, 2, 3, 4
    ##  mode        DIN, DOUT, AIN, AOUT, TOUCH, PWM
    ##
    ##  Note that not all modes are available on all pins

    def setIOpinMode(self, ioNumber, mode):

        self._sendCommand('IO' + str(ioNumber) + ' MODE ' + mode)
        result = self._readResponse()

        return result

    def getIOpinMode(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' MODE ?')
        result = self._readResponse()

        return result

    ## GET/SET PWMFREQ
    ##
    ## parameters:
    ##  ioNumber    0, 2, 3, 4
    ##  freq        750 to 80000 Hz

    def setIOpinPWMFreq(self, ioNumber, freq):

        self._sendCommand('IO' + str(ioNumber) + ' PWMFREQ ' + str(freq))
        result = self._readResponse()

        return result

    def getIOpinPWMFreq(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' PWMFREQ ?')
        result = self._readResponse()

        return result

    ## GET/SET IOpinInterrupt
    ##
    ## parameters:
    ##  ioNumber    0, 1, 2, 3, 4
    ##  intMode     CHANGE|CHANGING, RISE|RISING, FALL|FALLING, NONE|OFF|0

    def setIOpinInterrupt(self, ioNumber, intMode):

        self._sendCommand('IO' + str(ioNumber) + ' INT ' + intMode)
        result = self._readResponse()

        return result

    def getIOpinInterrupt(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' INT ?')
        result = self._readResponse()

        return result

    ## GET/SET IOpinValue
    ##
    ## parameters:
    ##  ioNumber    0, 1, 2, 3, 4
    ##  value       0|LOW, 1|HIGH, x%, Volts

    def setIOpinValue(self, ioNumber, value):

        self._sendCommand('IO' + str(ioNumber) + ' VALUE ' + str(value))
        result = self._readResponse()

        return result

    def getIOpinValue(self, ioNumber):

        self._sendCommand('IO' + str(ioNumber) + ' VALUE ?')
        result = self._readResponse()

        return result

    def getIOpinInterruptFlag(self, ioNumber):

        result = self.interruptCheck('!I0' + str(ioNumber))

        return result

    def clearIOpinInterruptFlag(self, ioNumber):

        self.interruptClear('!IO' + str(ioNumber))
