# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
from adafruit_matrixportal.matrix import Matrix
from messageboard import MessageBoard
from messageboard.fontpool import FontPool
from messageboard.message import Message
import asyncio

matrix = Matrix(width=256, height=32, bit_depth=5)
messageboard = MessageBoard(matrix)
messageboard.set_background(0x000000)
fontpool = FontPool()
fontpool.add_font("font", "fonts/Arial-Bold-24.pcf")

# Create the message ahead of time
message = Message(fontpool.find_font("font"), mask_color=0xFF00FF, opacity=1)
text = "-"
message.add_text(text, color=0xFFFFFF, x_offset=2, y_offset=0)

# task coroutine
async def work():
    while True:
        # Animate the message
        await messageboard.animate(message, "Scroll", "in_from_right")
        time.sleep(1)
        await messageboard.animate(message, "Scroll", "out_to_left")

# main coroutine
async def main():
    # schedule the task
    print('Main start')
    task = asyncio.create_task(work())
    # suspend a moment
    await asyncio.sleep(10)
    # report a message
    print('Main done')
 
# run the asyncio program
asyncio.run(main())

