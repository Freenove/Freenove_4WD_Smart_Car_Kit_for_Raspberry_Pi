import time
import RPi.GPIO as GPIO
from Command import COMMAND as cmd
GPIO.setwarnings(False)
Buzzer_Pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Buzzer_Pin,GPIO.OUT)

class Buzzer:
    def run(self, command):
        if command!="0":
            GPIO.output(Buzzer_Pin, True)
        else:
            GPIO.output(Buzzer_Pin, False)

    def __del__(self):
        'Make sure the sound goes off once a program terminates'
        GPIO.output(Buzzer_Pin, False)

            
if __name__=='__main__':
    B=Buzzer()
    print('Activate Buzzer and wait for 1s')
    B.run('1')
    time.sleep(1)
