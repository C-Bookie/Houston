"""
Using https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
if the wifi adapter won't power up, or the pi keeps hitting kernal panics, then it might be underpowered
    a good test is plugging the adapter in, if it reboots the system, then it's probably a surge of power demand

    todo:
        aiosm
            when idle, wait for a request to `receive` message
            proto messages/request
                receive
                    size
                    action message type
                action
                    set_value(s)
                    set_wifi
                    set_lights
                    set_motors
                    start_subprocess
                    set_eprom
                    set_event listeners
                        sensors/values thresholds
                        passive events
                        active events
                            callbacks
                    report/read/return
                        echo/heartbeat
                        list of sensors
                        time received (testing network and clock)
                        passive events
                            sensors/values reaching thresholds
                        battery/power usage
                        device_info
                            protocol version
                            time up


    sending a message consists of:
        header - set size {HEADER_LEN}, encoded in big endian
            size of Receive message
        Receive message
            size: of next message
            type: proto message type url
                fixme can't figure out how to decode strings, use enum for now

    need to record standard deviation of echo time



"""
import asyncio
import colorsys
import math
import random
import time

import aiosm

from google.protobuf import message as Message

from coronation.python.example_pb2 import ReceiveRequest, LightRequest, RGBValue, SensorReport, Acknowledge

print("Begining project jubliee")


addr, port = "192.168.0.44", 8089

pot_value = 0
last_request = 0
cool_down = 1000

time_on_host, time_on_client = [], []
start_time_on_host, start_time_on_client = 0, 0
count = 0


USING_HEADER = True
HEADER_LEN = 4  # size in bytes


class RadioHacked(aiosm.radio.Radio):
    def prepare(self, message: Message) -> bytes:
        """todo add support for ReceiveRequest"""
        packed_message = message.SerializeToString()
        if not USING_HEADER:  # todo deprecate use of ETX (or use ETX in place of HEADER_LEN)
            if self.ETX in packed_message:
                raise Exception(
                    'message contains exit sequence: ' + self.ETX.decode())  # todo create custom Exception
            packed_message += self.ETX
        else:
            message_len = len(packed_message)
            message_type = {
                "ReceiveRequest": ReceiveRequest.RequestType.ReceiveRequest,
                "LightRequest": ReceiveRequest.RequestType.LightRequest
            }[message.DESCRIPTOR.full_name]
            receive_request = ReceiveRequest(size=message_len, type=message_type)

            packed_receive_request = receive_request.SerializeToString()
            request_len = len(packed_receive_request)
            header = request_len.to_bytes(HEADER_LEN, byteorder='big')
            data = header + packed_receive_request + packed_message
        return data

    def unpack(self, data: bytes) -> bytes:
        if not USING_HEADER:
            return data[0:-self.ETX_LEN]
        pass

    async def receive(self) -> any:
        if not USING_HEADER:
            return await super().receive()

        # todo consider using self.reader.readexactly(HEADER_LEN) for error detection
        raw_data_len = await self.reader.read(HEADER_LEN)  # fixme
        data_len = int.from_bytes(raw_data_len, byteorder='big')
        raw_recieve_request = await self.reader.read(data_len)
        recieve_request = ReceiveRequest()

        try:
            recieve_request.ParseFromString(raw_recieve_request)
        except Message.DecodeError as e:
            breakpoint()  # todo handle properly

        raw_message = await self.reader.read(recieve_request.size)
        message = {
            ReceiveRequest.RequestType.ReceiveRequest: ReceiveRequest,
            ReceiveRequest.RequestType.LightRequest: LightRequest,
            ReceiveRequest.RequestType.SensorReport: SensorReport,
            ReceiveRequest.RequestType.Acknowledge: Acknowledge,
        }[recieve_request.type]()

        try:
            message.ParseFromString(raw_message)
        except Message.DecodeError as e:
            breakpoint()  # todo handle properly

        return message

    async def send(self, message: str) -> None:
        # dprint("Sending", message)
        self.sequence(message)
        await self.writer.drain()


class ResponderHacked(aiosm.responder.Responder, RadioHacked):
    def prepare(self, message: Message) -> bytes:
        return RadioHacked.prepare(self, message)  # todo review if not using super() is safe

    def unpack(self, data: bytes) -> any:
        # todo use protobuf
        #  cannot call <protobuf_message>.ParseFromString() without knowing the message type
        return RadioHacked.unpack(self, data)


class NodeHacked(aiosm.node.Node, ResponderHacked):
    async def callback(self, response) -> None:
        """has to be in Node for use of self.host

        todo generalise
            decode ReceiveRequest
        """

        if isinstance(response, Acknowledge):
            # print("acknowledge received")
            global waiting
            waiting = False
            global start_time_on_host, time_on_client
            start_time_on_host = time.time()
            time_on_client.append(start_time_on_host - start_time_on_client)

        if isinstance(response, SensorReport):
            self.host.brightness = response.pot / 4096
            print(f"brightness: {self.host.brightness}")

            # global last_request
            # if last_request + cool_down < time.time():
            #     await self.host.send_light_request()
            #     last_request = time.time()

    async def run(self):
        await self.host.send_light_request()
        await super().run()


# overload custom node
aiosm.host.Node = NodeHacked

waiting = False


def temp_to_rgb(temp):
    temp = max(1000, min(40000, temp))
    temp /= 100
    red = 255
    green = 255
    blue = 255

    if temp <= 66:
        red = min(255, max(0, 255 * (1 - ((temp - 60) * (329.698727446 / (temp - 60))) / 255)))
        green = min(255, max(0, 255 * (1 - ((temp - 60) * (99.4708025861 / (temp - 60))) / 255)))
        blue = 255
    else:
        red = min(255, max(0, 255 * (1 - ((temp - 60) * (288.1221695283 / (temp - 60))) / 255)))
        green = min(255, max(0, 255 * (1 - ((temp - 60) * (99.4708025861 / (temp - 60))) / 255)))
        blue = min(255, max(0, 255 * (1 - ((temp - 60) * (138.5177312231 / (temp - 60))) / 255)))

    return red, green, blue




class SubHost(aiosm.host.Host):

    def __init__(self):
        super().__init__(addr=addr, port=port)
        self.message = LightRequest()

        self.message.lights = self.lights = 10
        self.message.offset = 4

        self.brightness = 1
        self.rotation_speed = 2
        self.pulse_speed = 24
        self.saturation_speed = 1
        self.transition_speed = 1
        self.modulation_speed = 0.9

    async def send_light_request_1(self):
        del self.message.value_array[:]  # recycling message
        # max_brightness = int(self.brightness * 255)
        for i in range(self.lights):
            h = ((time.time() / self.rotation_speed) + (i / self.lights)) % 1
            golden = (1 + 5 ** 0.5) / 2
            s = ((time.time() / (-self.rotation_speed*golden)) + (i / self.lights)) % 1
            s = (1/2) + (abs((s*2)-1)/2)

            red, green, blue = colorsys.hsv_to_rgb(h, s, self.brightness)
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)
            self.message.value_array.append(RGBValue(red=red, green=green, blue=blue))
            # print(f"RGB {i}: ({red}, {green}, {blue})")

        for connection in self.connections:
            await connection.send(self.message)

    async def send_light_request_2(self):
        del self.message.value_array[:]  # recycling message

        for i in range(self.lights):
            h = ((time.time() / self.rotation_speed) + (i / self.lights)) % 1

            # Smoother sine wave-based modulation for saturation
            s = 0.5 * (1 + math.sin(2 * math.pi * (time.time() / self.saturation_speed) + (i / self.lights)))

            # Smoother sine wave-based modulation for brightness
            modulated_brightness = 0.5 * self.brightness * (
                        1 + math.sin(2 * math.pi * (time.time() / self.pulse_speed) + (i / self.lights)))

            red, green, blue = colorsys.hsv_to_rgb(h, s, modulated_brightness)
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)
            self.message.value_array.append(RGBValue(red=red, green=green, blue=blue))

        for connection in self.connections:
            await connection.send(self.message)

    async def send_light_request_3(self):
        del self.message.value_array[:]  # recycling message

        for i in range(self.lights):
            temp = ((time.time() / self.rotation_speed) + (i / self.lights)) % 1
            temp = int(1000 + (temp * 4000))  # Convert the range of 1000K to 5000K and ensure temp is an integer

            red, green, blue = temp_to_rgb(temp)
            grb_color = (green, red, blue)  # Swap red and green values for GRB color order

            # Convert float RGB values to integers
            int_grb_color = (int(grb_color[0]), int(grb_color[1]), int(grb_color[2]))

            self.message.value_array.append(
                RGBValue(red=int_grb_color[0], green=int_grb_color[1], blue=int_grb_color[2]))

        for connection in self.connections:
            await connection.send(self.message)

    send_light_request = send_light_request_1

    async def run(self):
        try:
            await super(SubHost, self).run()
        except OSError as exc:  # [Errno 49]
            raise Exception("did you check the IP?") from exc
        await asyncio.sleep(1)

        global waiting
        global start_time_on_host

        while True:
            if not waiting:
                waiting = True
                await self.send_light_request()
                global time_on_host, start_time_on_client, count
                count += 1
                start_time_on_client = time.time()
                time_on_host.append(start_time_on_client - start_time_on_host)

            await asyncio.sleep(0)
            # await asyncio.sleep(1/(2**3))  # todo replace with await for confirmation of message received

# look into async executor pool
# https://stackoverflow.com/questions/29269370/how-to-properly-create-and-run-concurrent-tasks-using-pythons-asyncio-module


async def status_printer():
    global time_on_host, time_on_client, count
    while True:
        if time_on_host and time_on_client:
            print(
                f"{count=},",
                f"total_time_on_host={sum(time_on_host):.4f},",
                f"total_time_on_client={sum(time_on_client):.4f},",
                f"max_time_on_host={max(time_on_host):.4f},",
                f"max_time_on_client={max(time_on_client):.4f}"
            )
            time_on_host, time_on_client = [], []
            count = 0
        await asyncio.sleep(1)


def main():
    loop = asyncio.get_event_loop()

    host = SubHost()

    task1 = loop.create_task(host.run())
    task1.set_name("Host")

    task2 = loop.create_task(status_printer())
    task2.set_name("Status")

    asyncio.gather(task1)
    asyncio.gather(task2)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
