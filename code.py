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
fontpool.add_font("font_bold", "fonts/Kanit-Regular-24.pcf")
fontpool.add_font("font_light", "fonts/Kanit-Light-24.pcf")
fontpool.add_font("font_thin", "fonts/Kanit-Thin-24.pcf")

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
    font_bold = fontpool.find_font("font_bold")
    font_light = fontpool.find_font("font_light")
    font_thin = fontpool.find_font("font_thin")
    message = Message(font_light, mask_color=0xFF00FF, opacity=1)
    message.add_text(text, color=0xFFFFFF, x_offset=2, y_offset=-8, font=font_bold)
    message.add_image("images/mkrz_ship.bmp", x_offset=2, y_offset=6)
    message.add_text(text, color=0xFFFFFF, x_offset=2, y_offset=-8, font=font_light)
    message.add_text(text, color=0xFFFFFF, x_offset=2, y_offset=-8, font=font_thin)
    return message

# task coroutine
async def animate_message(text="???"):
    while True:
        # Animate the message
        message = create_text_message(text)
        # await messageboard.animate(message, "Static", "show")
        # await asyncio.sleep(1)
        await messageboard.animate(message, "Static", "show")

# main coroutine
next_text = "mkrz"

async def main():
    global next_text
    print('Main start')

    # TODO: move try/except into task
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

