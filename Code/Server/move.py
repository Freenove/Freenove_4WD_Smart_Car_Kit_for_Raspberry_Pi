import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random


class Move:
    def __init__(self):        
        self.PWM = Motor()
    
    def back(self):
        self.PWM.setMotorModel(-600,-600,-600,-600)
        time.sleep(1)
    
    def forward(self):
        self.PWM.setMotorModel(600,600,600,600)
        time.sleep(1)
    
    def right(self):
        self.PWM.setMotorModel(600,600,-600,-600)
        time.sleep(1)
    
    def left(self):
        self.PWM.setMotorModel(-600,-600,600,600)
        time.sleep(1)
    
    def stop(self):
        self.PWM.setMotorModel(0, 0, 0, 0)
