import mido
import asyncio
import numpy as np
import pedalboard
import sounddevice as sd


# Define the sample rate and duration for the audio stream
# Define the audio settings
sample_rate = 48000
block_size = 1024

MAX_KEYS = 108
OCTAVE_SHIFT = -1

def noteToFreq(note):
    a = 440 #frequency of A (coomon value is 440Hz)
    return (a / 32) * (2 ** ((note + (OCTAVE_SHIFT * 12) - 9) / 12))


# Define the function to generate the saw wave
class Oscillator:
    gain = 0.1

    keys = [0]*MAX_KEYS  # array of volumes per key
    # cutoff_frequency = 5000  # TODO

    def generate_audio_chunk(self, frames, start_time=0):
        duration = frames / float(sample_rate)
        time_axis = np.linspace(start_time, start_time + duration, frames, False)

        result_waveform = np.zeros((frames,))
        for note, volume in enumerate(self.keys):
            if volume == 0:
                continue

            frequency = noteToFreq(note)
            key_waveform = (2 * (time_axis * frequency - np.floor(0.5 + time_axis * frequency))) / 2
            key_waveform *= volume
            result_waveform += key_waveform

        result_waveform *= self.gain
        return result_waveform

class Reverb:
    reflection = 0.99

    def __init__(self, size):
        self.buffer = np.zeros((size,))
        self.pos = 0

    def step(self, in_data):  # fixme with a loop
        # Update the buffer with the new input data
        self.buffer[self.pos:self.pos + len(in_data)] *= self.reflection
        self.buffer[self.pos:self.pos + len(in_data)] += in_data * (1 - self.reflection)

        out_data = self.buffer[self.pos:self.pos + len(in_data)]

        self.pos += len(in_data)
        self.pos %= len(in_data)

        return out_data


class LowPassFilter:
    cutoff_freq = 1000
    resonance = 0.5

    def __init__(self):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.x1 = self.x2 = self.y1 = self.y2 = 0

        self.calc_coeff()

    def calc_coeff(self):
        # Calculate the filter coefficients based on the cutoff frequency and resonance
        c = 1.0 / np.tan(np.pi * self.cutoff_freq / self.sample_rate)
        r = 1.0 - 3.0 * self.resonance
        self.a1 = 2.0 * (r * np.cos(np.pi * self.cutoff_freq / self.sample_rate))
        self.a2 = -(r ** 2)
        self.b0 = (1.0 - np.cos(np.pi * self.cutoff_freq / self.sample_rate)) / 2.0
        self.b1 = 1.0 - np.cos(np.pi * self.cutoff_freq / self.sample_rate)
        self.b2 = (1.0 - np.cos(np.pi * self.cutoff_freq / self.sample_rate)) / 2.0

    def step(self, in_data):
        out_data = np.zeros_like(in_data)

        # Apply the filter to the input data in blocks of block_size
        for i in range(0, len(in_data), self.block_size):
            # Get the current block of input data
            x = in_data[i:i+self.block_size]

            # Apply the filter to the current block of input data
            y = self.b0 * x + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2

            # Update the state variables for the next block
            self.x2 = self.x1
            self.x1 = x[-1]
            self.y2 = self.y1
            self.y1 = y[-1]

            # Add the filtered block to the output data
            out_data[i:i+self.block_size] = y

        return out_data


def mixer(a, b, wet):
    return (a * wet) + (b * (1-wet))


oscillator = Oscillator()
reverb = Reverb(block_size * 2)
filter = LowPassFilter()


def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    waveform = oscillator.generate_audio_chunk(frames, time.currentTime)
    # waveform = mixer(reverb.step(waveform), waveform, 1)
    waveform = mixer(filter.step(waveform), waveform, 1)
    # todo add safety limits
    outdata[:] = waveform.reshape(-1, 1)

def make_stream():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    def callback(message):
        loop.call_soon_threadsafe(queue.put_nowait, message)

    async def stream():
        while True:
            yield await queue.get()
    return callback, stream()


# Define an async coroutine to stream audio
async def stream_audio():
    # Start the audio stream using the callback function
    with sd.OutputStream(
            # device="External Headphones",
            samplerate=sample_rate, blocksize=block_size, channels=1, dtype=np.float32,
                         callback=audio_callback):

        # create a callback/stream pair and pass callback to mido
        cb, stream = make_stream()
        mido.open_input(callback=cb)


        # print messages as they come just by reading from stream
        async for message in stream:
            print(message)
            if message.type == 'note_on':
                # oscillator.keys[message.note-1] = (message.velocity / 100) ** (1/2)
                oscillator.keys[message.note-1] = 1

            if message.type == 'note_off':
                oscillator.keys[message.note-1] = 0


def main():
    loop = asyncio.get_event_loop()

    task1 = loop.create_task(stream_audio())
    task1.set_name("Keyboard")

    asyncio.gather(task1)
    # Run the event loop until interrupted

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()

    # with sd.OutputStream(
    #         device="External Headphones",
    #         samplerate=sample_rate, blocksize=block_size, channels=1, dtype=np.float32,
    #                      callback=audio_callback):
    #
    #     input()
