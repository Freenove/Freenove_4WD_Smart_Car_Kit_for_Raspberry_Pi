import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685
class Ultrasonic:
    def __init__(self):        
        GPIO.setwarnings(False)        
        self.trigger_pin = 27
        self.echo_pin = 22
        self.MAX_DISTANCE = 300               # define the maximum measuring distance, unit: cm
        self.timeOut = self.MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
        
    def pulseIn(self,pin,level,timeOut): # obtain pulse time of a pin under timeOut
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0;
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0;
        pulseTime = (time.time() - t0)*1000000
        return pulseTime
    
    def get_distance(self):     # get the measurement results of ultrasonic module,with unit: cm
        distance_cm=[0,0,0,0,0]
        for i in range(5):
            GPIO.output(self.trigger_pin,GPIO.HIGH)      # make trigger_pin output 10us HIGH level 
            time.sleep(0.00001)     # 10us
            GPIO.output(self.trigger_pin,GPIO.LOW) # make trigger_pin output LOW level 
            pingTime = self.pulseIn(self.echo_pin,GPIO.HIGH,self.timeOut)   # read plus time of echo_pin
            distance_cm[i] = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s
        distance_cm=sorted(distance_cm)
        return  int(distance_cm[2])
    
    def run_motor(self,L,M,R):
        if (L < 30 and M < 30 and R <30) or M < 30 :
            self.PWM.setMotorModel(-1450,-1450,-1450,-1450) 
            time.sleep(0.1)   
            if L < R:
                self.PWM.setMotorModel(1450,1450,-1450,-1450)
            else :
                self.PWM.setMotorModel(-1450,-1450,1450,1450)
        elif L < 30 and M < 30:
            PWM.setMotorModel(1500,1500,-1500,-1500)
        elif R < 30 and M < 30:
            PWM.setMotorModel(-1500,-1500,1500,1500)
        elif L < 20 :
            PWM.setMotorModel(2000,2000,-500,-500)
            if L < 10 :
                PWM.setMotorModel(1500,1500,-1000,-1000)
        elif R < 20 :
            PWM.setMotorModel(-500,-500,2000,2000)
            if R < 10 :
                PWM.setMotorModel(-1500,-1500,1500,1500)
        else :
            self.PWM.setMotorModel(600,600,600,600)
                

    def run2(self):
        self.pwm=Motor()
        self.pwm_s = Servo()
        self.pwm_s.setServoPwm('0', 90)
        time.sleep(0.2)
        M = self.get_distance()

        if M < 30:
            self.pwm_s.setServoPwm('0', 30)
            time.sleep(0.2)
            L = self.get_distance()
            self.pwm_s.setServoPwm('0', 151)
            time.sleep(0.2)
            R = self.get_distance()
            self.run_motor(L, M, R)
            self.pwm_s.setServoPwm('0', 90)

    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
        while True:
            for i in range(90,30,-60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)
            for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)
        
            
        
ultrasonic=Ultrasonic()              
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)

