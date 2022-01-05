from random import randint

from aiosm import Client
import asyncio


class BreadKnife(Client):
    def __init__(self):
        super().__init__("bread_knife", "192.168.1.6", 8089)
        self.update_rate = 5

    async def run(self):
        self.white_list_functions.append("report")
        await self.connect()
        await self.request("subscribe", "pizza")
        await asyncio.gather(
            super().run(),
            self.loop()
        )

    async def report(self, button: bool):
        await self.broadcast("pitta", "light", button)

    async def loop(self):
        asyncio.current_task().set_name(self.__name__ + "-Transmitter")

        await self.broadcast("pitta", "light", True)

        while True:
            if not self.ready:  # todo add to self.wait()
                return

            lights = [(randint(0, 255), randint(0, 255), randint(0, 255)) for i in range(1)]

            await self.broadcast("pitta", "fast_light", lights)

            await self.wait()


if __name__ == "__main__":
    bread_knife = BreadKnife()
    asyncio.run(bread_knife.run())
