#!/usr/bin/env python3
#############################################################################
# Filename    : ADC.py
# Description : ADC and DAC
# Author      : freenove
# modification: 2018/09/15
########################################################################
import smbus
import time
class Adc:
    def __init__(self):
        self.address = 0x48  #default address of PCF8591
        self.bus=smbus.SMBus(1)
        self.cmd=0x40        #command

    def analogRead(self,chn):#read ADC value,chn:0,1,2,3
        value=[0,0,0,0,0,0,0,0,0]
        for i in range(9):
            value[i] = self.bus.read_byte_data(self.address,self.cmd+chn)
        value=sorted(value)
        return value[4]
    def analogWrite(self,value):#write DAC value
        self.bus.write_byte_data(address,cmd,value)
    def loop(self):
        while True:
            self.value = self.analogRead(2)   #read the ADC value of channel 0,1,2,3
            #analogWrite(value)      #write the DAC value
            self.voltage = self.value / 256.0 * 3.3  #calculate the voltage value
            print ('ADC Value : %d, Voltage : %.2f'%(self.value,self.voltage))
            time.sleep(0.01)
    def recvADC(self,channel):
        while(1):
            self.value = self.analogRead(channel)   #read the ADC value of channel 0,1,2,
            self.value1 = self.analogRead(channel)
            if self.value==self.value1:
                break;
        self.voltage = self.value / 256.0 * 3.3  #calculate the voltage value
        self.voltage = round(self.voltage,2)
        return self.voltage
    def destroy():
        self.bus.close()

def loop():
    while True:
        adc=Adc()
        Left_IDR=adc.recvADC(0)
        print (Left_IDR)
        Right_IDR=adc.recvADC(1)
        print (Right_IDR)
        Power=adc.recvADC(2)
        print (Power)
        time.sleep(1)
        #print '----'

def destroy():
    pass

# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()