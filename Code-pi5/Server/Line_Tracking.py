import time
from Motor import *
from gpiozero import LineSensor
IR01 = 14
IR02 = 15
IR03 = 23
IR01_sensor = LineSensor(IR01)
IR02_sensor = LineSensor(IR02)
IR03_sensor = LineSensor(IR03)
class Line_Tracking:
    def __init__(self):
        pass

    def test_Infrared(self):
        try:
            while True:
                if IR01_sensor.value !=True and IR02_sensor.value == True and IR03_sensor.value !=True:
                    print ('Middle')
                elif IR01_sensor.value !=True and IR02_sensor.value != True and IR03_sensor.value ==True:
                    print ('Right')
                elif IR01_sensor.value ==True and IR02_sensor.value != True and IR03_sensor.value !=True:
                    print ('Left')
        except KeyboardInterrupt:
            print ("\nEnd of program")
        
    def run(self):
        while True:
            self.LMR=0x00
            if IR01_sensor.value == True:
                self.LMR=(self.LMR | 4)
            if R02_sensor.value == True:
                self.LMR=(self.LMR | 2)
            if IR03_sensor.value == True:
                self.LMR=(self.LMR | 1)
            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR==6:
                PWM.setMotorModel(-2000,-2000,4000,4000)
            elif self.LMR==1:
                PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR==3:
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(0,0,0,0)
            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.test_Infrared()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
