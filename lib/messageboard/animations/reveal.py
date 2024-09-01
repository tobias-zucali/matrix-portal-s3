import time
import bitmaptools
import displayio
from . import Animation


class Reveal(Animation):
    async def scroll_from_to(self, message, duration, start_x, start_y, end_x, end_y):
        """
        Scroll the message from one position to another over a certain period of
        time.

        :param message: The message to animate.
        :param float duration: The period of time to perform the animation over in seconds.
        :param int start_x: The Starting X Position
        :param int start_yx: The Starting Y Position
        :param int end_x: The Ending X Position
        :param int end_y: The Ending Y Position
        :type message: Message
        """
        steps = max(abs(end_x - start_x), abs(end_y - start_y))
        if not steps:
            return
        increment_x = (end_x - start_x) / steps
        increment_y = (end_y - start_y) / steps
        for i in range(steps + 1):
            start_time = time.monotonic()
            current_x = start_x + round(i * increment_x)
            current_y = start_y + round(i * increment_y)
            self._draw(message, current_x, current_y)
            if i <= steps:
                await self._wait(start_time, duration / steps)

    async def in_from_left(self, message, duration=1, step_size=1):
        """Scroll a message in from the left side of the display over a certain period of
        time. The final position is centered.

        :param message: The message to animate.
        :param float duration: (optional) The period of time to perform the animation
                               over in seconds. (default=1)
        :param int x: (optional) The amount of x-offset from the center position (default=0)
        :type message: Message
        """

        image = message.buffer
        crop_image = displayio.Bitmap(
            image.width, image.height, 65535
        )
        crop_image.fill(message.mask_color)

        self._draw(
            crop_image,
            0,
            0,
            message.opacity,
        )

        content_width = message._cursor[0]

        steps = abs(min(content_width, self._display.width) / step_size)
        if not steps:
            return
        for i in range(steps):
            current_width = (i + 1) * 4
            start_time = time.monotonic()
            bitmaptools.blit(crop_image, image, 0, 0, x1=0, x2=current_width + 1, y1=0, y2=self._display.height)
            self._draw(
                crop_image,
                0,
                0,
                message.opacity,
            )

            if i <= steps:
                await self._wait(start_time, duration / current_width)
        
        with_diff = content_width - self._display.width
        if with_diff > 0:
            await self.scroll_from_to(
                message,
                duration / self._display.width * with_diff,
                0,
                0,
                with_diff * -1,
                0
            )
