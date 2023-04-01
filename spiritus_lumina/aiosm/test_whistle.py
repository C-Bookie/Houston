import asyncio
import math
import queue
import threading

import numpy as np
import phue
import pyaudio

from aiosm import Client


# https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo.py
def openInputStream(id=None, framerate=None):
    useloopback = False

    p = pyaudio.PyAudio()

    try:
        default_device_index = p.get_default_input_device_info()
    except IOError:
        default_device_index = -1

    if id is None:
        for i in range(0, p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(str(info["index"]) + ":  \t %s \t %s" % (
                p.get_host_api_info_by_index(info["hostApi"])["name"], info["name"]))

            if default_device_index == -1:
                default_device_index = info["index"]

        # Handle no devices available
        if default_device_index == -1:
            print("No device available. Quitting.")
            exit()

        # Get input or default
        device_id = int(input("Choose Input device: ") or default_device_index)
    else:
        device_id = id
    print("")

    # Get device info
    try:
        device_info = p.get_device_info_by_index(device_id)
    except IOError:
        device_info = p.get_device_info_by_index(default_device_index)
        print("Selection not available, using default.")

    # Choose between loopback or standard mode
    is_input = device_info["maxInputChannels"] > 0
    is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
    if is_input:
        print("Selection is input using standard mode.\n")
    else:
        if is_wasapi:
            useloopback = True
            print("Selection is output. Using loopback mode.\n")
        else:
            print("Selection is output and does not support loopback mode. Quitting.\n")
            exit()

    # Open stream
    channelcount = device_info["maxInputChannels"] if (
            device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info[
        "maxOutputChannels"]
    if framerate is None:
        frames_per_buffer = 1024
    else:
        frames_per_buffer = int(device_info["defaultSampleRate"] / framerate)

    stream = p.open(format=pyaudio.paInt16,
                    channels=channelcount,
                    rate=int(device_info["defaultSampleRate"]),
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=device_info["index"])
                    # as_loopback=useloopback)

    return stream, device_info


class LiveInputStream(threading.Thread):
    def __init__(s, stream, chunk):
        threading.Thread.__init__(s)
        s.stream = stream
        s.chunk = chunk
        s.queue = queue.Queue()

    def run(s):
        while True:
            s.queue.put(s.stream.read(s.chunk))


def openOutpoutStream(id=None, framerate=None):
    p = pyaudio.PyAudio()

    try:
        default_device_index = p.get_default_output_device_info()["index"]
    except IOError:
        default_device_index = -1

    if id is None:
        for i in range(0, p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(str(info["index"]) + ":  \t %s \t %s" % (
            p.get_host_api_info_by_index(info["hostApi"])["name"], info["name"]))

            if default_device_index == -1:
                default_device_index = info["index"]

        # Handle no devices available
        if default_device_index == -1:
            print("No device available. Quitting.")
            exit()

        # Get input or default
        device_id = int(input("Choose output device: ") or default_device_index)
    else:
        device_id = id
    print("")

    # Get device info
    try:
        device_info = p.get_device_info_by_index(device_id)
    except IOError:
        device_info = p.get_device_info_by_index(default_device_index)
        print("Selection not available, using default.")

    # Choose between loopback or standard mode
    is_output = device_info["maxOutputChannels"] > 0
    if device_info["maxOutputChannels"] == 0:
        print("not an output.\n")
        exit()

    # Open stream
    # channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
    channelcount = 2
    if framerate is None:
        frames_per_buffer = 1024
    else:
        frames_per_buffer = int(device_info["defaultSampleRate"] / framerate)

    stream = p.open(format=pyaudio.paInt16,
                    channels=channelcount,
                    rate=int(device_info["defaultSampleRate"]),
                    output=True,
                    frames_per_buffer=frames_per_buffer,
                    output_device_index=device_info["index"])

    return stream, device_info


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class MidiWhistle(Client):
    def __init__(self):
        super().__init__("Whistler")

        # self.center = (0.1, 0.1, 0.2)

        # self.velocity = 9  # lower is brighter
        # self.curve = 1
        # self.cap = 1
        # # self.cutin = 0.0
        # # self.cutoff = 1
        # self.hueCo = (1 / 4)
        # self.satCo = (1 / 5)
        # self.briCo = (1 / 1)

        self.velocity = 0.001
        self.curve = 2
        self.cap = 2
        # self.cutin = 0.0
        # self.cutoff = 1
        self.hueCo = 1
        self.satCo = 1/5
        self.briCo = 10

        self.frame_rate = 10

        in_stream, input_info = openInputStream(2, self.frame_rate)
        # in_stream, input_info = openOutpoutStream(None, self.frame_rate)
        stream_framerate = int(input_info["defaultSampleRate"])
        chunk_size = stream_framerate // self.frame_rate
        self.live_input_stream = LiveInputStream(in_stream, chunk_size)
        self.live_input_stream.start()

        self.threshold = 4

        bridgeIP = '192.168.1.227'
        self.b = phue.Bridge(bridgeIP)
        self.b.connect()

    async def run(self):
        await self.connect()
        # await self.request("subscribe", "piano")  # comment out to disable receiving midi
        await asyncio.gather(
            super().run(),
            self.loop()  # comment out to disable midi transition
        )

    def loop(self):
        # asyncio.current_task().set_name(self.__name__ + "-Transmitter")

        while True:

            data = self.live_input_stream.queue.get()
            da = np.fromstring(data, dtype=np.int16)
            left, right = da[0::2], da[1::2]  # left and right channel
            sample = right

            sample = self.velocity * sample  # / self.frame_rate

            graph = np.abs(np.fft.rfft(sample).real)  # ** (1 / co)
            graph = np.array([x * (int(y) << 16) for x, y in zip(range(len(graph)), graph)])
            graph1 = sigmoid(graph) * 2 - 1
            graph = graph ** self.curve

            min_cut = 0
            max_cut = int(len(graph1) / self.cap)

            l = max_cut - min_cut
            graph1 = graph1[min_cut:max_cut]

            points_x = []
            points_y = []
            for i in range(l):
                freq = graph1[i]
                theta = i / l
                theta **= self.hueCo
                # theta *= self.cutoff - self.cutin  # cuts pink from the rainbow
                # theta += self.cutin
                theta *= math.pi * 2
                points_x += [freq * math.sin(theta)]
                points_y += [freq * math.cos(theta)]

            x = np.sum(points_x) / len(points_x)
            y = np.sum(points_y) / len(points_y)

            hue = (math.atan2(x, y) + (2 * math.pi if x < 0 else 0)) / (2 * math.pi)
            sat = math.sqrt((x * x) + (y * y))
            bri = sum(sigmoid(abs(sample)) * 2 - 1) / len(sample)

            sat **= self.satCo
            bri **= self.briCo

            peaks = []
            troughs = []  # fixme
            last_vol = 0
            last_vol_high = 0
            last_i_high = 0
            last_vol_low = 0
            pass_thresh = False
            for i in range(len(graph)):
                vol = graph[i]

                if last_vol <= vol:
                    last_vol_high = vol
                    last_i_high = i
                    if last_vol_low + self.threshold < last_vol_high:
                        pass_thresh = True
                else:
                    last_vol_low = vol
                    if pass_thresh and last_vol_low + self.threshold < last_vol_high:
                        peaks += [last_i_high]
                        pass_thresh = False

                last_vol = vol

            # await self.broadcast("graph", "draw",
            #                      self.frame_rate,
            #                      list(graph),
            #                      list(graph1),
            #                      list(sample),
            #                      (hue, sat, bri),
            #                      peaks,
            #                      troughs)

            command = {
                'transitiontime': 1,
                'hue': int(hue * 65535),
                'sat': int(sat * 254),
                'bri': int(bri * 254),
            }
            self.b.set_light('cal', command)

            print(command)

            self.live_input_stream.queue.task_done()


if __name__ == "__main__":
    whistle = MidiWhistle()
    whistle.loop()

    # asyncio.run(whistle.run())
