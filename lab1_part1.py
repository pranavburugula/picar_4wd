import picar_4wd as fc
import numpy as np
from picar_4wd import Speed
import time
import signal

def quit_handler(signal, frame):
    fc.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, quit_handler)

MIN_DIST_TO_BUMPER = 20
FORWARD_SPEED = 20
BACK_SPEED = 10
TURN_SPEED = 20

fc.forward(FORWARD_SPEED)
while 1:
    if fc.get_distance_at(0) <= MIN_DIST_TO_BUMPER:
        fc.stop()
        fc.backward(BACK_SPEED)
        time.sleep(0.5)
        rand_time = np.random.rand() * 2
        direction = np.random.randint(0,2)
        if direction == 0:
            fc.turn_right(TURN_SPEED)
        elif direction == 1:
            fc.turn_left(TURN_SPEED)
        time.sleep(rand_time)
        fc.stop()
        fc.forward(FORWARD_SPEED)

fc.stop()