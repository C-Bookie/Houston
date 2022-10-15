"""
Using https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
if the wifi adapter won't power up, or the pi keeps hitting kernal panics, then it might be underpowered
    a good test is plugging the adapter in, if it reboots the system, then it's probably a surge of power demand
"""
import array
import asyncio
import base64
from typing import List, Tuple

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import aiosm

from random import random

import colorsys

import math

RUNNING_ON_PI = True

if RUNNING_ON_PI:
    import Adafruit_SSD1306
else:
    import pygame


print("Begining project jubliee")

font = ImageFont.load_default()


class Display:  # fixme should be abstract
    def __init__(self):
        if RUNNING_ON_PI:
            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)

            self.disp.begin()
            self.disp.clear()
            self.disp.display()

            self.width = self.disp.width
            self.height = self.disp.height
        else:
            self.width, self.height = 128, 64
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Serious Work - not games")

            # self.clock = pygame.time.Clock()

    def paint(self, image: Image):
        if RUNNING_ON_PI:
            self.disp.clear()
            self.disp.image(image)
            self.disp.display()

            # time.sleep(1)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)

            image = image.convert("RGB")
            surface = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()
            self.screen.blit(surface, (0, 0))
            # pygame.display.flip()
            pygame.display.update()


class LightRangeRequest:
    def __init__(self, values: List[Tuple[int, int, int]], offset: int):
        """A serializable request of light values
        todo:
            make @dataclass
            test

        :param values: a list of hsl values for each light
        :param offset: the starting index of the light
        """
        # type check
        for value in values:
            for arg in value:
                if not 0 <= arg < 256:
                    raise Exception("Values must be between 0 and 256 (including 0).")

        self.values = values
        self.offset = offset

    def serialize(self) -> dict:  # fixme rename
        """Return the request serialised to be sent"""
        values = "".join([base64.b64encode(array.array('B', led)).decode('utf-8') for led in self.values])
        return {"size": len(self.values), "values": values, "offset": self.offset}


if RUNNING_ON_PI:
    addr, port = "192.168.5.1", 8089
else:
    addr, port = "192.168.1.250", 8089

host = aiosm.Host(addr=addr, port=port)


async def director():
    rh, gh, bh = 10, 10, 10

    display = Display()

    image = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(image)

    screen_rows = 7
    screen_cols = 21
    log = []

    client = aiosm.Client("director", addr, port)

    await asyncio.sleep(1)

    await client.connect()
    # fixme copy spiritus_lumina.aiosm.audio_graph

    cycle = 0
    while 1:
        cycle += 1

        def get_line(left, right):
            return left + (" " * (screen_cols - (len(left) + len(right)))) + right

        header = [
            get_line("Jubliee", str(cycle)),
            f"Con: {len(host.connections)}",
        ]

        # print("\n".join(header))
        #
        # log.append(f"woo: {i}")

        msg = header + log[-(screen_rows-len(header)):]

        draw.rectangle((0, 0, image.width, image.height), 0)
        for n, line in enumerate(msg):
            draw.text((1, n*9-1), line, font=font, fill=255)

#        display.paint(image)

        number_of_leds = 150
        batch = 30
        for i in range(0, number_of_leds, batch):
            values = []
            for n in range(batch):
                h = (i + n) / number_of_leds
                h *= 8 
                h += cycle / (7.4 * 4)
                h %= 1
                # h = random()
                v = 0.9
                l = v
                s = 0.95
                r1, g1, b1 = colorsys.hls_to_rgb(h, l, s)
                r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)

                # r, g, b = r1, g1, b1
                r, g, b = r2, g2, b2
                # r, g, b = r1-r2, g1-g2, b1-b2
                # rh, gh, bh = min(rh, r), min(gh, g), min(bh, b)

                values.append((
                    int(r * ((1 << 8) - 1)),
                    int(g * ((1 << 8) - 1)),
                    int(b * ((1 << 8) - 1))
                ))
            light_request = LightRangeRequest(values=values, offset=i)
            await client.broadcast("pitta", "fast_light", light_request.serialize())  # fixme why does this run twice

        # clock.tick(1)  # fps
        await asyncio.sleep(1/4)


# look into async executor pool https://stackoverflow.com/questions/29269370/how-to-properly-create-and-run-concurrent-tasks-using-pythons-asyncio-module

def main():
    loop = asyncio.get_event_loop()

    task1 = loop.create_task(host.run())
    task1.set_name("Host")

    task2 = loop.create_task(director())
    task2.set_name("director")

    asyncio.gather(task1, task2)
    # asyncio.gather(task2)
    loop.run_forever()
    loop.close()


def test():
    display = Display()

    import time

    image = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(image)
    # draw.rectangle((0, 0, display.width, display.height), 255)

    for y in range(0, display.height, 8):
        for x in range(0, display.width, 8):
            draw.rectangle((x, y, x+8, y+8), 255)
            time.sleep(0.25)
            display.paint(image)


if __name__ == '__main__':
    main()
    # test()
