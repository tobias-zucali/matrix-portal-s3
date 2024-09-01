from adafruit_matrixportal.matrix import Matrix
from adafruit_mcp230xx.mcp23017 import MCP23017
from config.messages import BUTTONS, INTRO, TIMEOUT
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
fontpool.add_font("font_thin", "fonts/Kanit-Thin-24.pcf")
font_thin = fontpool.find_font("font_thin")
fontpool.add_font("font_small_bold", "fonts/Kanit-Regular-18.pcf")
font_small_bold = fontpool.find_font("font_small_bold")
fontpool.add_font("font_small_light", "fonts/Kanit-Light-18.pcf")
font_small_light = fontpool.find_font("font_lsmall_ight")
fontpool.add_font("font_small_thin", "fonts/Kanit-Thin-18.pcf")
font_small_thin = fontpool.find_font("font_small_thin")

# setup IO

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

for button in BUTTONS:
    if not "pin" in button:
        print("button not valid")
        print(button)
        # TODO: Throw nice error
        break
    button["io"] = mcp.get_pin(button["pin"])
    button["io"].direction = Direction.INPUT
    button["io"].pull = Pull.UP
    button["value"] = button["io"].value
    button["last_shown"] = 0
    button["throttle"] = button.get("throttle", 1) # throttle executions 1 sec by default

def get_text_message(text):
    messageboard.set_background(0x000000)
    message = Message(font_small_thin, mask_color=0xFF00FF, opacity=1)
    message.add_text(text, color=0xFFFFFF, x_offset=4, y_offset=0)
    return message

async def reveal(message, sleep=1):
    await messageboard.animate(message, "Reveal", "in_from_left", step_size=4)
    await asyncio.sleep(sleep)

async def blink(message, sleep=0):
    await messageboard.animate(message, "Static", "blink")
    await asyncio.sleep(sleep)

async def slide_top(message, sleep=0):
    await messageboard.animate(message, "Scroll", "scroll_to_top")
    await asyncio.sleep(sleep)

async def show_intro():
    while True:
        messageboard.set_background(0x000033)
        message = Message(font_bold, mask_color=0xFF00FF, opacity=1)
        message.add_text("mkrz", color=0xFFFFFF, x_offset=4, y_offset=-9)
        message.add_image("images/mkrz_ship.bmp", x_offset=2, y_offset=6)
        await reveal(message, 2)
        await blink(message)

        for line in INTRO["lines"]:
            await reveal(get_text_message(line), 1)

async def show_alert(background, text_parts):
    print(text_parts)
    messageboard.set_background(background)
    message = Message(font_light, mask_color=0xFF00FF, opacity=1)
    for i, text in enumerate(text_parts):
        message.add_text(text, color=0xFFFFFF, x_offset=4, y_offset=-9)
        await messageboard.animate(message, "Static", "show")
        await asyncio.sleep(0.5)
        if i < len(text_parts) - 1:
            await messageboard.animate(message, "Static", "hide")

async def show_start(button_definition):
    await show_alert(0x001100, button_definition["text"])

async def show_end(button_definition):
    await show_alert(0x001100, button_definition["text"])
    await asyncio.sleep(10)
    await show_intro()

async def show_timeout():
    print("show_timeout")
    await show_alert(0x110000, TIMEOUT["text"])
    await asyncio.sleep(10)
    await show_intro()

async def show_button(button_definition):
    message = get_text_message(button_definition["text"])
    await reveal(message, 2)
    await blink(message)
    await slide_top(message)

# task coroutine
async def show(button_definition):
    try:
        if button_definition is None:
            await show_intro()
        else:
            start_time = time.monotonic()
            type = button_definition.get("type", None)
            if type is "start":
                await show_start(button_definition)
            if type is "end":
                await show_end(button_definition)
            else:
                await show_button(button_definition)

            timeout = button_definition.get("timeout", None)
            if timeout is not None:
                remaining_timeout = (start_time + timeout) - time.monotonic()
                if (remaining_timeout > 0):
                    await asyncio.sleep(remaining_timeout)
                await show_timeout()
                
    except AnimationCancelled:
        pass

# main coroutine
async def main():
    asyncio.create_task(show(None))

    while True:
        for button in BUTTONS:
            if button["io"].value != button["value"]:
                button["value"] = button["io"].value

                if button["last_shown"] + button["throttle"] < time.monotonic():
                    button["last_shown"] = time.monotonic()
                    asyncio.create_task(show(button))
        await asyncio.sleep(0)
 
# run the asyncio program
asyncio.run(main())

