import smbus
import time
class Adc:
    def __init__(self):
        # Get I2C bus
        self.bus = smbus.SMBus(1)
        # I2C address of the device
        self.ADDRESS            = 0x48
        # PCF8591 Command
        self.PCF8591_CMD                        =0x40  #Command
        # ADS7830 Command Set
        self.ADS7830_CMD_SD_SINGLE              = 0x84 # Single-Ended Inputs
        self.ADS7830_CMD_SNGL_CHANNEL_0         = 0x00 # +IN = CH0, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_1         = 0x40 # +IN = CH1, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_2         = 0x10 # +IN = CH2, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_3         = 0x50 # +IN = CH3, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_4         = 0x20 # +IN = CH4, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_5         = 0x60 # +IN = CH5, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_6         = 0x30 # +IN = CH6, -IN = GND
        self.ADS7830_CMD_SNGL_CHANNEL_7         = 0x70 # +IN = CH7, -IN = GND
        self.ADS7830_CMD_PD_POWER_DOWN          = 0x00 # Power Down Between A/D Converter Conversions
        self.ADS7830_CMD_PD_REF_OFF             = 0x04 # Internal Reference OFF and A/D Converter ON
        self.ADS7830_CMD_PD_REF_ON              = 0x08 # Internal Reference ON and A/D Converter OFF
        self.ADS7830_CMD_PD_REF_ON_AD_ON        = 0x0C # Internal Reference ON and A/D Converter ON
        for i in range(3):
            aa=self.bus.read_byte_data(self.ADDRESS,0xf4)
            if aa < 150:
                self.Index="PCF8591"
            else:
                self.Index="ADS7830" 
    def analogReadPCF8591(self,chn):#PCF8591 read ADC value,chn:0,1,2,3
        value=[0,0,0,0,0,0,0,0,0]
        for i in range(9):
            value[i] = self.bus.read_byte_data(self.ADDRESS,self.PCF8591_CMD+chn)
        value=sorted(value)
        return value[4]   
        
    def analogWritePCF8591(self,value):#PCF8591 write DAC value
        self.bus.write_byte_data(self.ADDRESS,cmd,value)
        
    def recvPCF8591(self,channel):#PCF8591 write DAC value
        while(1):
            value1 = self.analogReadPCF8591(channel)   #read the ADC value of channel 0,1,2,
            value2 = self.analogReadPCF8591(channel)
            if value1==value2:
                break;
        voltage = value1 / 256.0 * 3.3  #calculate the voltage value
        voltage = round(voltage,2)
        return voltage
    def recvADS7830(self,channel):
        """Select the Command data from the given provided value above"""
        if channel == 0:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_0)
        elif channel == 1:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_1)
        elif channel == 2:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_2)
        elif channel == 3:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_3)
        elif channel == 4:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_4)
        elif channel == 5:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_5)
        elif channel == 6:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_6)
        elif channel == 7:
            COMMAND_SET = (self.ADS7830_CMD_SD_SINGLE | self.ADS7830_CMD_SNGL_CHANNEL_7)
        
        self.bus.write_byte(self.ADDRESS, COMMAND_SET)
        while(1):
            value1 = self.bus.read_byte(self.ADDRESS)
            value2 = self.bus.read_byte(self.ADDRESS)
            if value1==value2:
                break;
        voltage = value1 / 256.0 * 3.3  #calculate the voltage value
        voltage = round(voltage,2)
        return voltage
        
    def recvADC(self,channel):
        if self.Index=="PCF8591":
            data=self.recvPCF8591(channel)
        elif self.Index=="ADS7830":
            data=self.recvADS7830(channel)
        return data
    def i2cClose(self):
        self.bus.close()

def loop():
    adc=Adc()
    while True:
        Left_IDR=adc.recvADC(0)
        print (Left_IDR)
        Right_IDR=adc.recvADC(1)
        print (Right_IDR)
        Power=adc.recvADC(2)*3
        print (Power)
        time.sleep(1)
        print ('----')
def destroy():
    pass
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
