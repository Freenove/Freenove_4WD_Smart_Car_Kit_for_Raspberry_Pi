import time
from Motor import *
from gpiozero import DistanceSensor
from servo import *
from PCA9685 import PCA9685
import random
import move
import sys

   
PWM = Motor()

PWM.setMotorModel(0, 0, 0, 0)

servo = Servo()
servo.setServoPwm('0', 0)
servo.setServoPwm('1', 0)
