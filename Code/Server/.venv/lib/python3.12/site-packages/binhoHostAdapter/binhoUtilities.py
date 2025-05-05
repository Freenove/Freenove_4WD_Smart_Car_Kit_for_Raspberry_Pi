## binhoUtilities Python Library
##
## Jonathan Georgino <jonathan@binho.io>
## Binho LLC
## www.binho.io

import sys
import glob
import serial
import warnings

# Source: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
# Claims that it is successfully tested on Windows 8.1 x64, Windows 10 x64, Mac OS X 10.9.x / 10.10.x / 10.11.x and Ubuntu 14.04 / 14.10 / 15.04 / 15.10 with both Python 2 and Python 3.

class binhoUtilities:
    def __init__(self):
        warnings.warn('The binhoUtilities class has been deprecated and will be removed in a future version, see: htps://support.binho.io/python-libraries/binhoutilities for details',
            category=UserWarning)

    def listAvailablePorts(self):
        warnings.warn('The binhoUtilities class has been deprecated and will be removed in a future version, see: htps://support.binho.io/python-libraries/binhoutilities for details',
            category=UserWarning)
        return listAvailablePorts()

    def listAvailableDevices(self):
        warnings.warn('The binhoUtilities class has been deprecated and will be removed in a future version, see: htps://support.binho.io/python-libraries/binhoutilities for details',
            category=UserWarning)
        return listAvailableDevices()

    def getPortByDeviceID(self, deviceID):
        warnings.warn('The binhoUtilities class has been deprecated and will be removed in a future version, see: htps://support.binho.io/python-libraries/binhoutilities for details',
            category=UserWarning)
        return getPortByDeviceID(deviceID)

def _checkForDeviceID(serialPort):
    """
    Checks if a device is a binho and returns the response
    :param serialPort: serial port address
    :type serialPort: str
    :return: DeviceID
    :rtype: str
    """
    comport = serial.Serial(serialPort, baudrate=1000000, timeout=0.025, write_timeout=0.05)
    command = '+ID ?\n'
    comport.write(command.encode('utf-8'))
    receivedData = comport.readline().strip().decode('utf-8')
    if len(receivedData) > 0:
        if receivedData[0] != "-":
            receivedData = comport.readline().strip().decode('utf-8')
    comport.close()
    return receivedData


def listAvailablePorts():
    """
    List serial ports on a system
    :return: List of serial port address
    :rtype: List[str]
    """
    if sys.platform.startswith('win'):
        ports = [f'COM{i + 1}' for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/cu.usbmodem*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port, timeout=500)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def listAvailableDevices():
    """
    Lists connected binhos
    :return: List of serial ports that have binhos attached
    :rtype: List[str]
    """
    ports = listAvailablePorts()
    result = []
    for port in ports:
        try:
            resp = _checkForDeviceID(port)
            if '-ID' in resp:
                result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def getPortByDeviceID(deviceID):
    """
    Get the port address that a specific binho is attached to
    :param deviceID: Device ID string
    :type deviceID: str
    :return: List of ports with a matching device ID
    :rtype: List[str]
    """
    ports = listAvailablePorts()
    result = []
    for port in ports:
        try:
            resp = _checkForDeviceID(port)
            if resp == '-ID ' + deviceID:
                result.append(port)
            elif resp == '-ID 0x' + deviceID:
                result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

if __name__ == '__main__':
    print(listAvailableDevices())
