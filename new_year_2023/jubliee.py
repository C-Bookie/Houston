"""
Using https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
if the wifi adapter won't power up, or the pi keeps hitting kernal panics, then it might be underpowered
    a good test is plugging the adapter in, if it reboots the system, then it's probably a surge of power demand
"""
import array
import asyncio
import base64
import random
from typing import List, Tuple

import aiosm

import colorsys

from aiosm import Radio, Client
from aiosm.dprint import dprint

from new_year_2023.protobuf.python.example_pb2 import ExampleMessage

print("Begining project jubliee")


addr, port = "192.168.1.130", 8089

# host = aiosm.Host(addr=addr, port=port)


class SubHost(aiosm.Host):
    def __init__(self):
        super().__init__(addr=addr, port=port)

    async def run(self):
        await super(SubHost, self).run()

        await asyncio.sleep(1)

        message = ExampleMessage()
        while True:
            message.value = random.randint(65, 90)
            message.value_array[:] = []  # clear
            message.value_array.extend([random.randint(65, 90) for i in range(10)])

            for connection in self.connections:
                dprint("Sending", message)
                # data = message.encode()
                data = message.SerializeToString()
                if connection.ETX in data:
                    raise Exception(
                        'message contains exit sequence: ' + connection.ETX.decode())  # todo create custom Exception
                data += connection.ETX
                connection.writer.write(data)
                await connection.writer.drain()

            # clock.tick(1)  # fps
            await asyncio.sleep(4)

# look into async executor pool https://stackoverflow.com/questions/29269370/how-to-properly-create-and-run-concurrent-tasks-using-pythons-asyncio-module


def main():
    loop = asyncio.get_event_loop()

    host = SubHost()

    task1 = loop.create_task(host.run())
    task1.set_name("Host")

    asyncio.gather(task1)
    # asyncio.gather(task2)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
