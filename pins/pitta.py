from random import randint
from typing import List, Tuple

from aiosm import Client
import asyncio


class BreadKnife(Client):
    def __init__(self):
        # super().__init__("bread_knife", "192.168.0.23", 8089)  # not working? check 3rd number of IP
        super().__init__("bread_knife", "192.168.5.1", 8888)  # not working? check 3rd number of IP
        self.update_rate = 5

    async def run(self):
        self.white_list_functions.append("report")
        await self.connect()
        await self.request("subscribe", "pizza")
        await asyncio.gather(
            super().run(),
            self.loop()
        )

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

        def serialize(self) -> str:  # fixme rename
            """Return the request serialised to be sent"""
            return {"size": len(self.values), "values": self.values, "offset": self.offset}

        def split(self, chunk_size: int) -> list:
            """Splits a light request into a list of requests of the given maximum size.

            :param chunk_size: the maximum size of each section
            :return: List[BreadKnife.LightRangeRequest]
            """
            sections = len(self.values) // chunk_size
            requests: List[BreadKnife.LightRangeRequest] = []
            for i in range(sections):
                start = i * chunk_size
                end = (i + 1) * chunk_size
                requests.append(BreadKnife.LightRangeRequest(self.values[start:end]))
            return requests

        async def send(self, mail_list: str, function: str):
            parent: BreadKnife  # todo: unsure how to initialize
            await parent.broadcast(mail_list, function, self.serialize())

    async def report(self, button: bool):
        await self.broadcast("pitta", "light", button)

    async def loop(self):
        asyncio.current_task().set_name(self.__name__ + "-Transmitter")

        await self.broadcast("pitta", "light", True)

        while True:
            if not self.ready:  # todo add to self.wait()
                return

            for i in range(0, 150, 10):
                light_request = self.LightRangeRequest(
                    values=[(randint(0, 255), randint(0, 255), randint(0, 255)) for i in range(10)],
                    offset=i,
                )
                await self.broadcast("pitta", "fast_light", light_request.serialize())  # fixme why does this run twice

            await self.wait()


if __name__ == "__main__":
    bread_knife = BreadKnife()
    asyncio.run(bread_knife.run())
