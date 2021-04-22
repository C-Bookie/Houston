import time
import wave

import torch

import numpy as np

import pyaudio
import matplotlib.pyplot as plt

from scrambler.audio_streams import get_api_by_name, CHUNK_SIZE, get_device_info

pa_manager = pyaudio.PyAudio()

chunk = 1024

api_info = get_api_by_name(pa_manager, "ASIO")  # fixme todo ASIO only works using a callback
# api_info = pa_manager.get_default_host_api_info()

input_device_info = pa_manager.get_device_info_by_index(api_info["defaultInputDevice"])
output_device_info = pa_manager.get_device_info_by_index(api_info["defaultOutputDevice"])

# input_device_info = get_device_info(pa_manager, as_input=True)
# output_device_info = get_device_info(pa_manager, as_input=False)

wf = wave.open("spiritus_lumina/audio/mass48-short.wav", 'rb')
# wf = wave.open("spiritus_lumina/audio/mass48.wav", 'rb')


format = pa_manager.get_format_from_width(2)
channels = input_device_info["maxInputChannels"]
# rate = int(input_device_info["defaultSampleRate"])
rate = wf.getframerate()
print(rate)

count = 0
use_input = True
use_callback = False


def analysis(data_in):
    global count
    if count % 500 == 0:
        data_np = np.frombuffer(data_in, dtype=np.int16)
        data_np = data_np.astype(np.float64)
        data_np /= 2**16
        data_np = data_np.reshape((-1, 2))
        # data_np = np.fft.fft2(data_np)
        # data_np = data_np.transpose().real
        plt.plot(data_np.real)
        plt.show()
        # print(f"count: {count}, sum: {sum(sum(abs(data_np)))}")
    count += 1


def callback_fn(data_in=None, frame_count=None, time_info=None, status=None):
    # print(in_data, frame_count, time_info, status)
    global use_input
    if not use_input:
        data_in = wf.readframes(chunk)

    if data_in == b'':
        return b'', pyaudio.paComplete


    # return data_in, pyaudio.paContinue

    data_np = np.frombuffer(data_in, dtype=np.int16)

    data_torch = torch.from_numpy(data_np)
    data_torch = torch.reshape(data_torch, (-1, 2))
    data_torch = data_torch.type(torch.float64)
    data_torch = torch.fft.fft2(data_torch)
    data_torch /= 2**16

    data_torch = data_torch.real + (data_torch.imag * 1j)

    data_torch *= 2**16
    data_torch = torch.fft.ifft2(data_torch)
    data_torch = data_torch.type(torch.int16)
    data_np_out = data_torch.cpu().detach().numpy()

    data_out = data_np_out.tobytes()

    analysis(data_out)

    return data_out, pyaudio.paContinue


callback = callback_fn if use_callback else None

stream = pa_manager.open(
    format=format,
    channels=channels,
    rate=rate,
    frames_per_buffer=chunk,  # device_info["defaultSampleRate"] // framerate
    input=use_input,
    input_device_index=input_device_info["index"],
    output=True,
    output_device_index=output_device_info["index"],
    stream_callback=callback,
)


try:
    # if use_input:
        # stream.start_stream()

    if callback:
        while stream.is_active():
            time.sleep(0.1)
    else:
        time.sleep(0.5)  # fixme remove

        while 1:
            input_buffer = None
            if use_input:
                input_buffer = stream.read(chunk, exception_on_overflow=False)
            data, state = callback_fn(input_buffer)

            if state == pyaudio.paComplete:
                break

            stream.write(data)
finally:
    stream.stop_stream()
    stream.close()

    pa_manager.terminate()
    print("Shutdown gently")
