import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random

SLEEP_TIME = 0.5

class Move:
    def __init__(self):        
        self.PWM = Motor()
    
    def back(self):
        self.PWM.setMotorModel(-600,-600,-600,-600)
        time.sleep(SLEEP_TIME)
    
    def forward(self):
        self.PWM.setMotorModel(600,600,600,600)
        time.sleep(SLEEP_TIME)
    
    def right(self):
        self.PWM.setMotorModel(600,600,-600,-600)
        time.sleep(SLEEP_TIME)
    
    def left(self):
        self.PWM.setMotorModel(-600,-600,600,600)
        time.sleep(SLEEP_TIME)
    
    def stop(self):
        self.PWM.setMotorModel(0, 0, 0, 0)
