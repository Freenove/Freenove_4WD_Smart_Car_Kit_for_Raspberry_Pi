import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random

SLEEP_TIME = 0.1

FORWARD_BACKWARD_SPEED = 500
TURN_SPEED = 1600

class Move:
    def __init__(self):        
        self.PWM = Motor()
    
    def back(self):
        self.PWM.setMotorModel(-FORWARD_BACKWARD_SPEED,-FORWARD_BACKWARD_SPEED,-FORWARD_BACKWARD_SPEED,-FORWARD_BACKWARD_SPEED)
        time.sleep(SLEEP_TIME)
    
    def forward(self):
        self.PWM.setMotorModel(FORWARD_BACKWARD_SPEED,FORWARD_BACKWARD_SPEED,FORWARD_BACKWARD_SPEED,FORWARD_BACKWARD_SPEED)
        time.sleep(SLEEP_TIME)
    
    def right(self, deg = 90):
        self.PWM.setMotorModel(TURN_SPEED,TURN_SPEED,-TURN_SPEED,-TURN_SPEED)
        time.sleep(SLEEP_TIME * (deg / 180) * 10)
    
    def left(self, deg = 90):
        self.PWM.setMotorModel(-TURN_SPEED,-TURN_SPEED,TURN_SPEED,TURN_SPEED)
        time.sleep(SLEEP_TIME * (deg / 180) * 10)
    
    def stop(self):
        self.PWM.setMotorModel(0, 0, 0, 0)
        time.sleep(SLEEP_TIME)
