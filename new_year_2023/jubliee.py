"""
Using https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
if the wifi adapter won't power up, or the pi keeps hitting kernal panics, then it might be underpowered
    a good test is plugging the adapter in, if it reboots the system, then it's probably a surge of power demand

    todo:
        aiosm
            use header
                use Radio.ETX for end of header?
"""
import asyncio
import random
import time

import aiosm
from aiosm.dprint import dprint

from google.protobuf import message as protobuf_message

# from aiosm.radio import Radio
# from aiosm.clinet import Client
# from aiosm.node import Node
# from aiosm.responder import Responder
# from aiosm.host import Host

from new_year_2023.python.example_pb2 import LightRequest, RGBValue, SensorLog

print("Begining project jubliee")


addr, port = "192.168.1.130", 8089

# host = aiosm.Host(addr=addr, port=port)


def hacked_send():
    print("moo")
    return "moo"

# fixme
aiosm.node.Node.send = hacked_send


pot_value = 0
last_request = 0
cool_down = 1000


USING_HEADER = True
HEADER_LEN = 4  # size in bytes


class NodeHacked(aiosm.node.Node):
    def unpack(self, data: bytes) -> str:
        if USING_HEADER:
            raise NotImplemented()
        else:
            return data[0:-self.ETX_LEN]

    async def callback(self, response) -> None:
        """Hacking callback for receiving messages"""
        message = SensorLog()
        try:
            message.ParseFromString(response)
        except protobuf_message.DecodeError:
            breakpoint()

        global pot_value
        pot_value = message.pot / 4096

        global last_request
        if last_request + cool_down < time.time():
            await self.host.send_light_request()
            last_request = time.time()


aiosm.host.Node = NodeHacked


class SubHost(aiosm.host.Host):
    def __init__(self):
        super().__init__(addr=addr, port=port)
        self.message = LightRequest()

        sel
        self.message.lights = self.lights
        self.message.offset = 0

    async def send_light_request(self):
        del self.message.value_array[:]
        # todo: don't use Radio.ETX
        #  random ints will result in ETX
        self.message.value_array.extend([RGBValue(
            red=random.randint(0, 7) * 16,
            green=random.randint(0, 7) * 16,
            blue=random.randint(0, 7) * 16,
        ) for _i in range(self.lights)])
        # self.message.value_array.extend([RGBValue(
        #     red=64,
        #     green=64,
        #     blue=blue=random.randint(0, 1) * 256,
        # ) for _i in range(self.lights)])

        for i in range(self.lights):
            red = self.message.value_array[i].red
            green = self.message.value_array[i].green
            blue = self.message.value_array[i].blue
            print(f"RGB {i}: ({red}, {green}, {blue})")

        for connection in self.connections:
            # dprint("Sending", self.message)
            # data = message.encode()
            # todo move to NodeHacked.pack()
            data = self.message.SerializeToString()
            if not USING_HEADER:
                if connection.ETX in data:
                    raise Exception(
                        'message contains exit sequence: ' + connection.ETX.decode())  # todo create custom Exception
                data += connection.ETX
            else:
                data_len = len(data)
                print(data_len)
                byte_mask = ((1 << 8)-1)
                # header = r''.join([
                #     (data_len >> (8 * i)) & byte_mask
                #     for i in range(HEADER_LEN)
                # ])
                header = bytes([
                    (data_len >> (8 * (HEADER_LEN-i-1))) & byte_mask
                    for i in range(HEADER_LEN)
                ])
                print(header)
                data = header + data
            connection.writer.write(data)
            await connection.writer.drain()

    async def run(self):
        await super(SubHost, self).run()

        await asyncio.sleep(1)

        while True:
            await self.send_light_request()

            # clock.tick(1)  # fps
            await asyncio.sleep(8)

# look into async executor pool
# https://stackoverflow.com/questions/29269370/how-to-properly-create-and-run-concurrent-tasks-using-pythons-asyncio-module


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
