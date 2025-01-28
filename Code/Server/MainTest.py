import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random
import move
import sys

REVERSE_THRESHOLD = 45

trigger_pin = 27
echo_pin    = 22
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)
class Ultrasonic:
    def __init__(self):        
        self.move = move.Move()
    def get_distance(self):
        distance_cm = sensor.distance * 100
        return  int(distance_cm)
    
    def run_motor(self, M):
        if M < REVERSE_THRESHOLD :
            self.move.back()
            if random.random() < 0.5:
                print("right")
                self.move.right()
            else:
                print("left")
                self.move.left()

        else :
            self.move.forward()
        

    def run(self, args):
        self.pwm_S=Servo()
        self.pwm_S.setServoPwm('0', 90)

        if len(args) > 2:
            if args[1] == 'r':
                print("r")
                for _ in range(int(args[2])):
                    self.move.right()
            
            if args[1] == 'l':
                print("l")
                for _ in range(int(args[2])):
                    self.move.left()

        while True:
            tot = []
            for angle in [60, 75, 90, 105, 120]:
                self.pwm_S.setServoPwm('0', angle)
                tot.append(self.get_distance())
                time.sleep(0.02)
            
            self.pwm_S.setServoPwm('0', 90)

            M = max(tot)
            
            print(M)
            self.run_motor(M)
            time.sleep(0.2)
            
            
        
ultrasonic=Ultrasonic()              
# Main program logic follows:

# command line: sudo python MainTest.py <l/r/None> <num>

"""
l/r/None refers to if you want to move right or left at the beginning. the number is how many times
"""
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        ultrasonic.run(sys.argv)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        ultrasonic.move.stop()
        ultrasonic.pwm_S.setServoPwm('0',90)
