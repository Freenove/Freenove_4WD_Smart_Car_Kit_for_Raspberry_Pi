import time
import RPi.GPIO as GPIO
from Command import COMMAND as cmd
GPIO.setwarnings(False)
Buzzer_Pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Buzzer_Pin,GPIO.OUT)
class Buzzer:
    def run(self,command):
        if command==cmd.CMD_START:
            GPIO.output(Buzzer_Pin,True)
        elif command==cmd.CMD_STOP:
            GPIO.output(Buzzer_Pin,False)
        else:
            GPIO.output(Buzzer_Pin,False)
            
        

if __name__=='__main__':
    B=Buzzer()
    B.run(cmd.CMD_START)
    time.sleep(3)
    B.run(cmd.CMD_STOP)



