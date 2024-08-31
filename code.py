# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
from adafruit_matrixportal.matrix import Matrix
from messageboard import MessageBoard
from messageboard.fontpool import FontPool
from messageboard.message import Message

matrix = Matrix(width=256, height=32, bit_depth=5)
messageboard = MessageBoard(matrix)
messageboard.set_background("images/background.bmp")
messageboard.set_background(0x0000FF)
fontpool = FontPool()
fontpool.add_font("font", "fonts/Arial-Bold-24.pcf")

# Create the message ahead of time
message = Message(fontpool.find_font("font"), mask_color=0xFF00FF, opacity=1)
message.add_image("images/logo.bmp")
text = "hala madrid"
message.add_text(text, color=0xFFFFFF, x_offset=2, y_offset=0)

while True:
    # Animate the message
    messageboard.animate(message, "Scroll", "in_from_right", duration=1)
    time.sleep(1)
    messageboard.animate(message, "Scroll", "out_to_left")
