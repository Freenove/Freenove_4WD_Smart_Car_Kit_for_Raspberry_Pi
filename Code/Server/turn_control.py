import move
import sys

mover = move.Move()

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == 'r':
        mover.right(float(sys.argv[i + 1]))
    elif sys.argv[i] == 'l':
        mover.left(float(sys.argv[i + 1]))
    elif sys.argv[i] == 'b':
        mover.back
    else:
        mover.forward()
