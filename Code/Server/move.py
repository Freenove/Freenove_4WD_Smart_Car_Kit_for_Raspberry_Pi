import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random

SLEEP_TIME = 0.1

FORWARD_BACKWARD_SPEED = 1000
TURN_SPEED = 1600

class Move:
    def __init__(self):        
        self.PWM = Motor()
    
    def back(self):
        self.PWM.setMotorModel(-FORWARD_BACKWARD_SPEED,-FORWARD_BACKWARD_SPEED,-FORWARD_BACKWARD_SPEED,-FORWARD_BACKWARD_SPEED)
        time.sleep(SLEEP_TIME * 7)
        self.stop()
    
    def forward(self):
        self.PWM.setMotorModel(FORWARD_BACKWARD_SPEED,FORWARD_BACKWARD_SPEED,FORWARD_BACKWARD_SPEED,FORWARD_BACKWARD_SPEED)
        time.sleep(SLEEP_TIME * 7)
        self.stop()
    
    def right(self, deg = 90):
        self.PWM.setMotorModel(TURN_SPEED,TURN_SPEED,-TURN_SPEED,-TURN_SPEED)
        time.sleep(SLEEP_TIME * (deg / 180) * 10)
        self.stop()
    
    def left(self, deg = 90):
        self.PWM.setMotorModel(-TURN_SPEED,-TURN_SPEED,TURN_SPEED,TURN_SPEED)
        time.sleep(SLEEP_TIME * (deg / 180) * 10)
        self.stop()
    
    def stop(self):
        self.PWM.setMotorModel(0, 0, 0, 0)
        time.sleep(SLEEP_TIME)
    
    def lot_right(self):
        self.PWM.setMotorModel(TURN_SPEED,TURN_SPEED,-TURN_SPEED,-TURN_SPEED)
    
    def lot_left(self):
        self.PWM.setMotorModel(-TURN_SPEED,-TURN_SPEED,TURN_SPEED,TURN_SPEED)

