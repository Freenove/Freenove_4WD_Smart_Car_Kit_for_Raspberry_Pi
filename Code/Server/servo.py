import time
from PCA9685 import PCA9685
class Servo:
    def __init__(self):
        self.PwmServo = PCA9685(0x40, debug=True)
        self.PwmServo.setPWMFreq(50)
        self.PwmServo.setServoPulse(8,1500)
        self.PwmServo.setServoPulse(9,850)
    def setServoPwm(self,channel1,channel2,angle1,angle2,error=10):
        if channel1==1:
            self.PwmServo.setServoPulse(8,2500-int((angle1+error)/0.09))
        else:
            pass
        if channel2==1:
            self.PwmServo.setServoPulse(9,500+int((angle2+error)/0.09))
        else:
            pass


pwm=Servo()
def loop():
    for i in range(180):
        pwm.setServoPwm(1,0,i,0)
        time.sleep(0.01)
    for i in range(180,0,-1):
        pwm.setServoPwm(1,0,i,0)
        time.sleep(0.01)          

def destroy():
    pwm.setServoPwm(1,1,90,20)

# Main program logic follows:
if __name__ == '__main__':
    pwm.setServoPwm(1,1,90,20)
    

    
       



    
