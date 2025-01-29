import move
import sys
import time

m = move()

if sys.argv[1] == 'r':
    m.lot_right()
else:
    m.lot_left()

try:
    while True:
        time.sleep(0.3)
except KeyboardInterrupt:
    m.stop()
    time.sleep(0.3)