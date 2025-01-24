import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random

trigger_pin = 27
echo_pin    = 22
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)
class Ultrasonic:
    def __init__(self):        
        pass
    def get_distance(self):     # get the measurement results of ultrasonic module,with unit: cm
        distance_cm = sensor.distance * 100
        return  int(distance_cm)
    
    def run_motor(self,L,M,R):
        if (L < 30 and M < 30 and R <30) or M < 30 :
            self.PWM.setMotorModel(-600,-600,-600,-600) # move backwards
            time.sleep(1)   
            # if L < R:
            #     self.PWM.setMotorModel(1450,1450,-1450,-1450) # turn right
            #     return
            # elif L > R:
            #     self.PWM.setMotorModel(-1450,-1450,1450,1450) # turn left
            #     return
            
            if random.random() < 0.5:
                self.PWM.setMotorModel(1000,1000,-1000,-1000)
            else:
                self.PWM.setMotorModel(-1000,-1000,1000,1000)

            time.sleep(1)

        # elif L < 30 and M < 30:
        #     PWM.setMotorModel(1500,1500,-1500,-1500) # turn right
        # elif R < 30 and M < 30:
        #     PWM.setMotorModel(-1500,-1500,1500,1500) # turn left
        # elif L < 20 :
        #     PWM.setMotorModel(2000,2000,-500,-500) # turn right
        #     if L < 10 :
        #         PWM.setMotorModel(1500,1500,-1000,-1000) # turn very right
        # elif R < 20 :
        #     PWM.setMotorModel(-500,-500,2000,2000) # turn left
        #     if R < 10 :
        #         PWM.setMotorModel(-1500,-1500,1500,1500) # turn very left
        else :
            self.PWM.setMotorModel(600,600,600,600) # move forward
        

    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        # for i in range(30,151,60):
        #         self.pwm_S.setServoPwm('0',i)
        #         time.sleep(0.2)
        #         if i==30:
        #             L = self.get_distance()
        #         elif i==90:
        #             M = self.get_distance()
        #         else:
        #             R = self.get_distance()
        while True:
            # for i in range(90,30,-60):
            #     self.pwm_S.setServoPwm('0',i)
            #     time.sleep(0.2)
            #     if i==30:
            #         L = self.get_distance()
            #     elif i==90:
            #         M = self.get_distance()
            #     else:
            #         R = self.get_distance()

            #     print("first", L, M, R)
            #     self.run_motor(L,M,R)
            # for i in range(30,151,60):
            #     self.pwm_S.setServoPwm('0',i)
            #     time.sleep(0.2)
            #     if i==30:
            #         L = self.get_distance()
            #     elif i==90:
            #         M = self.get_distance()
            #     else:
            #         R = self.get_distance()
            #     self.run_motor(L,M,R)
            #     print("second", L, M, R)
            self.pwm_S.setServoPwm('0', 90)
            time.sleep(0.2)
            M = self.get_distance()
            
            self.run_motor(300,M,300)
            
            
        
ultrasonic=Ultrasonic()              
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)
