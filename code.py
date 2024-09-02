from adafruit_matrixportal.matrix import Matrix
from adafruit_mcp230xx.mcp23017 import MCP23017
from config.messages import BUTTONS, INTRO, ERROR_TIMEOUT
from digitalio import Direction, Pull
from messageboard import MessageBoard
from messageboard.animations import AnimationCancelled
from messageboard.fontpool import FontPool
from messageboard.message import Message
import asyncio
import board
import busio
import time

# Setup Board
matrix = Matrix(width=256, height=32, bit_depth=5)
messageboard = MessageBoard(matrix)
messageboard.set_background(0x000000)
fontpool = FontPool()
fontpool.add_font("font_bold", "fonts/Kanit-Regular-24.pcf")
font_bold = fontpool.find_font("font_bold")
fontpool.add_font("font_light", "fonts/Kanit-Light-24.pcf")
font_light = fontpool.find_font("font_light")
# fontpool.add_font("font_thin", "fonts/Kanit-Thin-24.pcf")
# font_thin = fontpool.find_font("font_thin")
# fontpool.add_font("font_small_light", "fonts/Kanit-Light-18.pcf")
# font_small_light = fontpool.find_font("font_lsmall_ight")
fontpool.add_font("font_small_thin", "fonts/Kanit-Thin-18.pcf")
font_small_thin = fontpool.find_font("font_small_thin")
# fontpool.add_font("font_x_small_light", "fonts/Kanit-Light-14.pcf")
# font_x_small_light = fontpool.find_font("font_lsmall_ight")
fontpool.add_font("font_x_small_thin", "fonts/Kanit-Thin-14.pcf")
font_x_small_thin = fontpool.find_font("font_x_small_thin")

# setup IO
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

for button in BUTTONS:
    button["io"] = mcp.get_pin(button["pin"])
    button["io"].direction = Direction.INPUT
    button["io"].pull = Pull.UP
    button["value"] = button["io"].value
    button["last_shown"] = 0
    button["throttle"] = button.get("throttle", 1) # throttle executions 1 sec by default

def get_text_message(text):
    messageboard.set_background(0x000000)
    message = Message(font_x_small_thin, mask_color=0xFF00FF, opacity=1)
    message.add_text(text, color=0xFFFFFF, x_offset=4, y_offset=4)
    return message

async def sleep_and_check(button_definition, duration, start_time=None):
    global next_button_definition
    if start_time is None:
        start_time = time.monotonic()
    while time.monotonic() < (start_time + duration):
        await asyncio.sleep(0)
        if next_button_definition is not button_definition:
            raise AnimationCancelled()
    return time.monotonic()

async def reveal(message):
    await messageboard.animate(message, "Reveal", "in_from_left", step_size=4)

async def show(message, duration=0):
    await messageboard.animate(message, "Static", "show", duration=duration)

async def hide(message, duration=0):
    await messageboard.animate(message, "Static", "hide", duration=duration)

async def blink(message):
    await messageboard.animate(message, "Static", "blink")

async def slide_top(message):
    await messageboard.animate(message, "Scroll", "out_to_top")

async def show_intro():
    while True:
        messageboard.set_background(0x000033)
        message = Message(font_bold, mask_color=0xFF00FF, opacity=1)
        message.add_text("mkrz", color=0xFFFFFF, x_offset=4, y_offset=-9)
        message.add_image("images/mkrz_ship.bmp", x_offset=2, y_offset=6)
        await reveal(message)
        await show(message, duration=2)
        await blink(message)

        for line in INTRO["lines"]:
            message = get_text_message(line)
            await reveal(message)
            await show(message, duration=2)

async def show_alert(button_definition):
    start_time = time.monotonic()
    messageboard.set_background(button_definition["background"])
    message = Message(font_light, mask_color=0xFF00FF, opacity=1)
    text_parts = button_definition["text"]
    for i, text in enumerate(text_parts):
        message.add_text(text, color=0xFFFFFF, x_offset=4, y_offset=-9)
        await show(message, duration=0.5)
        if i < len(text_parts) - 1:
            await hide(message, duration=0.5)
    await check_timeouts(message, button_definition, start_time)

async def show_text(button_definition):
    start_time = time.monotonic()

    for i, line in enumerate(button_definition["text"]):
        message = get_text_message(line)
        if i == 0:
            await blink(message)
            await show(message, duration=2)
        else:
            await reveal(message)
            await show(message, duration=1)
    await check_timeouts(message, button_definition, start_time)

async def check_timeouts(message, button_definition, start_time):
    intro_timeout = button_definition.get("intro_timeout", None)
    error_timeout = button_definition.get("error_timeout", None)
    if error_timeout is not None:
        duration = max((start_time + error_timeout) - time.monotonic(), 0)
        await show(
            message,
            duration=duration
        )
        await main_show(ERROR_TIMEOUT)
    elif intro_timeout is not None:
        duration = max((start_time + intro_timeout) - time.monotonic(), 0)
        await show(
            message,
            duration=duration
        )
        await main_show(None)

async def main_show(button_definition):
    if button_definition is None:
        await show_intro()
    else:
        type = button_definition.get("type", None)
        if type is "alert":
            await show_alert(button_definition)
        else:
            await show_text(button_definition)

next_button_definition = None

def switch_button(button_definition):
    global next_button_definition
    next_button_definition = button_definition
    raise AnimationCancelled(button_definition)

# main coroutine
async def main():
    global next_button_definition
    asyncio.create_task(main_show(next_button_definition))

    while True:
        for button in BUTTONS:
            if button["io"].value != button["value"]:
                button["value"] = button["io"].value

                if button["last_shown"] + button["throttle"] < time.monotonic():
                    button["last_shown"] = time.monotonic()
                    switch_button(button)
        await asyncio.sleep(0)
 
# run the asyncio program
while True:
    try:
        asyncio.run(main())
    except AnimationCancelled:
        pass

