import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random
import move

REVERSE_THRESHOLD = 60

trigger_pin = 27
echo_pin    = 22
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)
class Ultrasonic:
    def __init__(self):        
        self.move = move()
    def get_distance(self):
        distance_cm = sensor.distance * 100
        return  int(distance_cm)
    
    def run_motor(self, M):
        if M < REVERSE_THRESHOLD :
            self.move.back()
            if random.random() < 0.5:
                self.move.right()
            else:
                self.move.left()

        else :
            self.move.forward()
        

    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        self.pwm_S.setServoPwm('0', 90)
        while True:
            M = self.get_distance()
            
            print(M)
            self.run_motor(M)
            time.sleep(0.2)
            
            
        
ultrasonic=Ultrasonic()              
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)
