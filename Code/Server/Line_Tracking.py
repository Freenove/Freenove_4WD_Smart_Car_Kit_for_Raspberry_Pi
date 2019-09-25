import time
from Motor import *
import RPi.GPIO as GPIO
IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)
class Line_Tracking:
    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(IR03)==True:
                self.LMR=(self.LMR | 1)
            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                PWM.setMotorModel(-1400,-1400,1400,1400)
            elif self.LMR==6:
                PWM.setMotorModel(-800,-800,1200,1200)
            elif self.LMR==1:
                PWM.setMotorModel(1400,1400,-1400,-1400)
            elif self.LMR==3:
                PWM.setMotorModel(1200,1200,-800,-800)
            elif self.LMR==7:
                pass
            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
