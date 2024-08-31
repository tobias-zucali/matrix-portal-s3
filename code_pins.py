# SPDX-FileCopyrightText: 2020 anecdata for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Neradoc for Adafruit Industries
# SPDX-FileCopyrightText: 2021-2023 Kattni Rembor for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

print()
print("Built-> In Modules")
help("modules")

"""
Standard output:

__future__        canio             math              synthio
__main__          codeop            max3421e          sys
_asyncio          collections       mdns              terminalio
_bleio            countio           memorymap         time
_eve              digitalio         microcontroller   touchio
_pixelmap         displayio         micropython       traceback
adafruit_bus_device                 dualbank          msgpack           ulab
adafruit_bus_device.i2c_device      epaperdisplay     neopixel_write    ulab.numpy
adafruit_bus_device.spi_device      errno             nvm               ulab.numpy.fft
adafruit_pixelbuf espidf            onewireio         ulab.numpy.linalg
aesio             espnow            os                ulab.scipy
alarm             espulp            ps2io             ulab.scipy.linalg
analogbufio       fontio            pulseio           ulab.scipy.optimize
analogio          fourwire          pwmio             ulab.scipy.signal
array             framebufferio     rainbowio         ulab.scipy.special
atexit            frequencyio       random            ulab.utils
audiobusio        gc                re                usb
audiocore         getpass           rgbmatrix         usb.core
audiomixer        gifio             rotaryio          usb_cdc
audiomp3          hashlib           rtc               usb_hid
binascii          i2cdisplaybus     sdcardio          usb_midi
bitbangio         io                select            vectorio
bitmapfilter      ipaddress         sharpdisplay      warnings
bitmaptools       jpegio            socketpool        watchdog
board             json              ssl               wifi
builtins          keypad            storage           zlib
busdisplay        keypad_demux      struct
busio             locale            supervisor
Plus any modules on the filesystem
"""

"""CircuitPython Essentials Pin Map Script"""
import microcontroller
import board
try:
    import cyw43  # raspberrypi
except ImportError:
    cyw43 = None

board_pins = []
for pin in dir(microcontroller.pin):
    if (isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin) or
        (cyw43 and isinstance(getattr(microcontroller.pin, pin), cyw43.CywPin))):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append(f"board.{alias}")
        # Add the original GPIO name, in parentheses.
        if pins:
            # Only include pins that are in board.
            pins.append(f"({str(pin)})")
            board_pins.append(" ".join(pins))

print()
print()
print("> Available Pins")
for pins in sorted(board_pins):
    print(pins)

"""
Standard output:

board.A0 (GPIO12)
board.A1 (GPIO3)
board.A2 (GPIO9)
board.A3 (GPIO10)
board.A4 (GPIO11)
board.ACCELEROMETER_INTERRUPT (GPIO15)
board.BOOT0 board.BUTTON board.D0 (GPIO0)
board.BUTTON_DOWN (GPIO7)
board.BUTTON_UP (GPIO6)
board.D13 board.L board.LED (GPIO13)
board.D16 board.SDA (GPIO16)
board.D17 board.SCL (GPIO17)
board.D18 board.TX (GPIO18)
board.D8 board.RX (GPIO8)
board.MTX_ADDRA (GPIO45)
board.MTX_ADDRB (GPIO36)
board.MTX_ADDRC (GPIO48)
board.MTX_ADDRD (GPIO35)
board.MTX_ADDRE (GPIO21)
board.MTX_B1 (GPIO40)
board.MTX_B2 (GPIO37)
board.MTX_CLK (GPIO2)
board.MTX_G1 (GPIO41)
board.MTX_G2 (GPIO39)
board.MTX_LAT (GPIO47)
board.MTX_OE (GPIO14)
board.MTX_R1 (GPIO42)
board.MTX_R2 (GPIO38)
board.NEOPIXEL (GPIO4)
"""
