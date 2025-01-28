from servo import *

pwm_S=Servo()

for i in range(30, 151):
    pwm_S.setServoPwm('0', i)
    time.sleep(0.02)