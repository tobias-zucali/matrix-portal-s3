import time
import board
import neopixel
from digitalio import DigitalInOut, Direction

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, auto_write=False)
RED = (255, 0, 0)
LIGHTRED = (20, 0, 0)

def color_chase(color, wait):
    pixels[0] = color
    time.sleep(wait)
    pixels.show()
    time.sleep(0.5)

RED = (255, 0, 0)
LIGHTRED = (20, 0, 0)

while True:
    color_chase(RED, 1)
    color_chase(LIGHTRED, 1)
