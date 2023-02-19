"""
Using https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
if the wifi adapter won't power up, or the pi keeps hitting kernal panics, then it might be underpowered
    a good test is plugging the adapter in, if it reboots the system, then it's probably a surge of power demand

    todo:
        aiosm
            use header
                use Radio.ETX for end of header?
                    no
"""
import asyncio
import random

import aiosm

from google.protobuf import message as protobuf_message

from coronation.python.example_pb2 import LightRequest, RGBValue, SensorLog

print("Begining project jubliee")


addr, port = "192.168.0.18", 8089

pot_value = 0
last_request = 0
cool_down = 1000


USING_HEADER = True
HEADER_LEN = 4  # size in bytes


class RadioHacked(aiosm.radio.Radio):
    def prepare(self, data: bytes) -> bytes:
        if not USING_HEADER:
            if self.ETX in data:
                raise Exception(
                    'message contains exit sequence: ' + self.ETX.decode())  # todo create custom Exception
            data += self.ETX
        else:
            data_len = len(data)
            header = data_len.to_bytes(HEADER_LEN, byteorder='big')
            data = header + data
        return data

    def unpack(self, data: bytes) -> bytes:
        if not USING_HEADER:
            return data[0:-self.ETX_LEN]
        pass

    async def receive(self) -> str:
        if not USING_HEADER:
            return await super().receive()

        # todo consider using self.reader.readexactly(HEADER_LEN)
        raw_data_len = await self.reader.read(HEADER_LEN)  # fixme
        data_len = int.from_bytes(raw_data_len, byteorder='big')
        message = await self.reader.read(data_len)
        return message


class ResponderHacked(aiosm.responder.Responder, RadioHacked):
    def prepare(self, message: protobuf_message) -> bytes:
        data = message.SerializeToString()
        return RadioHacked.prepare(self, data)  # todo review if not using super() is safe

    def unpack(self, data: bytes) -> any:
        # todo use protobuf
        #  cannot call <protobuf_message>.ParseFromString() without knowing the message type
        return RadioHacked.unpack(self, data)


class NodeHacked(aiosm.node.Node, ResponderHacked):
    async def callback(self, response) -> None:
        """has to be in Node for use of self.host

        todo generalise
        """
        message = SensorLog()
        try:
            message.ParseFromString(response)
        except protobuf_message.DecodeError:
            breakpoint()  # todo handle properly

        global pot_value
        pot_value = message.pot / 4096

        self.host.brightness = pot_value
        print(f"brightness: {pot_value}")

        # global last_request
        # if last_request + cool_down < time.time():
        #     await self.host.send_light_request()
        #     last_request = time.time()


# overload custom node
aiosm.host.Node = NodeHacked


class SubHost(aiosm.host.Host):
    def __init__(self):
        super().__init__(addr=addr, port=port)
        self.message = LightRequest()

        self.message.lights = self.lights = 10
        self.message.offset = 0

        self.brightness = 1

    async def send_light_request(self):
        del self.message.value_array[:]  # recycling message
        max_brightness = int(self.brightness * 255)

        for i in range(self.lights):
            red = random.randint(0, max_brightness)
            green = random.randint(0, max_brightness)
            blue = random.randint(0, max_brightness)
            self.message.value_array.append(RGBValue(red=red, green=green, blue=blue))
            print(f"RGB {i}: ({red}, {green}, {blue})")

        for connection in self.connections:
            await connection.send(self.message)

    async def run(self):
        await super(SubHost, self).run()
        await asyncio.sleep(1)

        while True:
            await self.send_light_request()
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
