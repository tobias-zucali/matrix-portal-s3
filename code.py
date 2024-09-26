from adafruit_matrixportal.matrix import Matrix
from messageboard import MessageBoard
from messageboard.animations import AnimationCancelled
from messageboard.fontpool import FontPool
from messageboard.message import Message
import asyncio

# Setup Board
matrix = Matrix(width=256, height=32, bit_depth=5)
messageboard = MessageBoard(matrix)
messageboard.set_background(0x000000)
fontpool = FontPool()
fontpool.add_font("font_bold_24", "fonts/Kanit-Regular-24.pcf")
font_bold_24 = fontpool.find_font("font_bold_24")
fontpool.add_font("font_light_24", "fonts/Kanit-Light-24.pcf")
font_light_24 = fontpool.find_font("font_light_24")
font_light_18 = fontpool.find_font("font_lsmall_ight")
fontpool.add_font("font_thin_18", "fonts/Kanit-Thin-18.pcf")
font_thin_18 = fontpool.find_font("font_thin_18")

def get_text_message(text):
    messageboard.set_background(0x000000)
    message = Message(font_thin_18, mask_color=0xFF00FF, opacity=1)
    message.add_text(text, color=0xFFFFFF, x_offset=4, y_offset=0)
    return message

async def reveal(message):
    await messageboard.animate(message, "Reveal", "in_from_left", step_size=4)

async def show(message, duration=0):
    await messageboard.animate(message, "Static", "show", duration=duration)

async def show_with_progress(message, duration=1, color=None):
    await messageboard.animate(message, "Static", "show_with_progress", duration=duration, color=color)

async def hide(message, duration=0):
    await messageboard.animate(message, "Static", "hide", duration=duration)


async def slide_top(message):
    await messageboard.animate(message, "Scroll", "out_to_top")

async def main():
    while True:
        messageboard.set_background(0x000000)
        message = Message(font_bold_24, mask_color=0xFF00FF, opacity=0.5)
        message.add_image("images/kunstverein_b.bmp", x_offset=0, y_offset=0)
        message.add_image("images/artmagazin_b.bmp", x_offset=16, y_offset=0)
        await reveal(message)
        await show(message, duration=2)
        await messageboard.animate(message, "Static", "blink", count=9, duration=2)
        message = Message(font_bold_24, mask_color=0xFF00FF, opacity=0.35)
        message.add_image("images/open_night_b.bmp", x_offset=0, y_offset=0)
        messageboard.set_message_position(0, 0)
        await messageboard.animate(message, "Static", "blink", count=9, duration=2)

while True:
    try:
        asyncio.run(main())
    except AnimationCancelled:
        pass

