# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from adafruit_matrixportal.matrix import Matrix
from digitalio import DigitalInOut, Direction, Pull
from messageboard import MessageBoard
from messageboard.animations import AnimationCancelled
from messageboard.fontpool import FontPool
from messageboard.message import Message
import asyncio
import board

# Setup Board
matrix = Matrix(width=256, height=32, bit_depth=5)
messageboard = MessageBoard(matrix)
messageboard.set_background(0x000000)
fontpool = FontPool()
fontpool.add_font("font", "fonts/Arial-Bold-24.pcf")

# Setup Buttons
BUTTON_LIST = [
    {
        "text": "I am UP",
        "pin": board.BUTTON_UP,
    },
    {
        "text": "I am DOWN",
        "pin": board.BUTTON_DOWN,
    }
]

for button in BUTTON_LIST:
    io = DigitalInOut(button["pin"])
    io.direction = Direction.INPUT
    io.pull = Pull.UP
    button["io"] = io
    button["value"] = io.value


def create_text_message(text):
    # Create the message ahead of time
    message = Message(fontpool.find_font("font"), mask_color=0xFF00FF, opacity=1)
    message.add_text(text, color=0xFFFFFF, x_offset=2, y_offset=0)
    return message

# task coroutine
async def animate_message(text="???"):
    while True:
        # Animate the message
        message = create_text_message(text)
        await messageboard.animate(message, "Scroll", "in_from_right")
        await asyncio.sleep(1)
        await messageboard.animate(message, "Scroll", "out_to_left")

# main coroutine
next_text = "Hello World"

async def main():
    global next_text
    print('Main start')

    # TODO: move catch into task
    try:
        asyncio.create_task(animate_message(next_text))
    except AnimationCancelled:
        pass

    # suspend a moment
    while True:
        break_loop = False
        for button in BUTTON_LIST:
            if button["io"].value != button["value"]:
                button["value"] = button["value"]
                print(button)

                # TODO: use 1sec debounce instead?
                if button["text"] != next_text:
                    next_text = button["text"]
                    break_loop = True
                    break
        if break_loop:
            break
        await asyncio.sleep(0)
        
    print('Main done')
 
# run the asyncio program
while True:
    asyncio.run(main())

