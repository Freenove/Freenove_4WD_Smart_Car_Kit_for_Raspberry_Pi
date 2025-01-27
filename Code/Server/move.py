import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random

SLEEP_TIME = 0.1

class Move:
    def __init__(self):        
        self.PWM = Motor()
    
    def back(self):
        self.PWM.setMotorModel(-600,-600,-600,-600)
        time.sleep(SLEEP_TIME)
    
    def forward(self):
        self.PWM.setMotorModel(600,600,600,600)
        time.sleep(SLEEP_TIME)
    
    def right(self, deg = 90):
        self.PWM.setMotorModel(1600,1600,-1600,-1600)
        # time.sleep(SLEEP_TIME * (deg / 180) * 10)
        time.sleep(0.5)
    
    def left(self, deg = 90):
        self.PWM.setMotorModel(-1600,-1600,1600,1600)
        # time.sleep(SLEEP_TIME * (deg / 180) * 10)
        time.sleep(0.5)
    
    def stop(self):
        self.PWM.setMotorModel(0, 0, 0, 0)
