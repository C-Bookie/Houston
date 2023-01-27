import time
import wave
from io import BytesIO

import pyaudio
import math

import matplotlib.pyplot as plt


def noise():
    # Set the parameters for the sine wave
    frequency = 400    # Hertz
    duration = 4       # seconds
    sample_rate = 44100  # Hz

    # Calculate the number of samples needed
    num_samples = duration * sample_rate

    # Generate the sine wave
    sine_wave = [math.sin(2*math.pi*(frequency)*(i/sample_rate)) for i in range(num_samples)]

    # Scale the sine wave to fit in a 16-bit signed integer
    sine_wave = [int(((x+1)/2) * 255) for x in sine_wave]

    # sample_range = 1000
    # plt.plot(range(sample_range), sine_wave[:sample_range])
    # plt.show()

    # Convert the sine wave to a bytestring
    sine_wave = bytearray(sine_wave)

    # Create a BytesIO object to write the sine wave to
    output = BytesIO()

    # Create a wave file with the sine wave data
    wave_file = wave.open(output, "wb")
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(sine_wave)
    wave_file.close()

    # Rewind the BytesIO object
    output.seek(0)

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    with wave.open(output, "rb") as wave_file:
        def stream_callback(in_data, frame_count, time_info, status):
            data = wave_file.readframes(1024)
            if data is None:
                return (data, pyaudio.paComplete)
            return (data, pyaudio.paContinue)

            # Generate the sine wave data
            # data = bytearray(num_samples * 2)
            # for i in range(num_samples):
            #     # Calculate the angle at the current sample
            #     angle = 2 * math.pi * frequency * (i / sample_rate)
            #     # Calculate the sine of the angle
            #     value = math.sin(angle)
            #     # Scale and map the value to the range of -32768 to 32767
            #     value = int(value * 32767)
            #     # Write the value to the output buffer as a 16-bit signed integer
            #     data[i * 2] = value & 0xff
            #     data[i * 2 + 1] = (value >> 8) & 0xff
            # # Return the data and number of frames written
            # return (data, pyaudio.paContinue)

        # Open a stream to play the sine wave
        stream = p.open(format=p.get_format_from_width(2),
                        channels=1,
                        rate=sample_rate,
                        output=True,
                        stream_callback=stream_callback
        )

    # Read the sine wave data from the BytesIO object and play it
    #     wave_file.setpos(0)
    #     next = wave_file.readframes(1024)
    #     while True:
    #         data = next
    #         next = wave_file.readframes(1024)
    #         if not data:
    #             break
    #         stream.write(data)

        stream.start_stream()

        # The loop is different as well...
        while stream.is_active():
            time.sleep(0.1)

    # Close the stream and PyAudio object
    stream.stop_stream()
    stream.close()
    p.terminate()


def diog():
    import pyaudio

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Get the number of available output devices
    num_devices = p.get_host_api_info_by_index(0)['deviceCount']

    # Print details of each output device
    for device_index in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, device_index)
        if device_info['maxOutputChannels'] > 0:
            print("Output device #{}: {}".format(device_index, device_info['name']))
            print("  Sample rate: {} Hz".format(device_info['defaultSampleRate']))
            print("  Number of channels: {}".format(device_info['maxOutputChannels']))

    # Close the PyAudio object
    p.terminate()


if __name__ == "__main__":
    noise()
    # diog()
