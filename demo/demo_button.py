import time
import board
from digitalio import DigitalInOut, Direction, Pull

button_up = DigitalInOut(board.BUTTON_UP)
button_up.direction = Direction.INPUT
button_up.pull = Pull.UP

while True:
    if not button_up.value:
        print("BTN is down")
    else:
        print("BTN is up")
        pass

    time.sleep(0.1) # sleep for debounce
