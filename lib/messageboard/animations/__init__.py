# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import asyncio
import time

class AnimationCancelled(Exception):
    pass


class Animation:
    _cancelled = False

    def __init__(self, display, draw_callback, starting_position=(0, 0), shift_count=(0, 0)):
        self._display = display
        starting_position = (
            starting_position[0] - shift_count[0] * self._display.width,
            starting_position[1] - shift_count[1] * self._display.height
        )
        self._position = starting_position
        self._draw = draw_callback
    
    def cancel(self):
        self._cancelled = True

    async def _wait(self, start_time, duration):
        """Uses time.monotonic() to wait from the start time for a specified duration"""
        await asyncio.sleep(0)
        while time.monotonic() < (start_time + duration):
            print("asyncio.sleep")
            await asyncio.sleep(0)
        if self._cancelled:
            raise AnimationCancelled()
        return time.monotonic()

    def _get_centered_position(self, message):
        return int(self._display.width / 2 - message.buffer.width / 2), int(
            self._display.height / 2 - message.buffer.height / 2
        )
