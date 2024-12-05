import time
from gpiozero import Buzzer
from Command import COMMAND as cmd
buzzer = Buzzer(17)
class Buzzer:
    def run(self,command):
        if command!="0":
            buzzer.on()
        else:
            buzzer.off()
if __name__=='__main__':
    B=Buzzer()
    B.run('1')
    time.sleep(3)
    B.run('0')




