import pyaudio
import numpy as np

# set parameters
sample_rate = 44100
channels = 1
volume = 0.01
tempo = 120

lfo = 1
cutoff_low = 0  # Hz
cutoff_high = 10  # Hz
cutoff_diff = cutoff_high - cutoff_low

note = 69
frequency = 440 * 2 ** ((note - 69) / 12)


def cutoff_1(samples, cutoff_freq):
    signal_fft = np.fft.fft(samples)  # Calculate the FFT of the signal
    freqs = np.fft.fftfreq(len(samples))  # Calculate the frequency range of the signal
    signal_fft[freqs > cutoff_freq] = 0  # Zero out the high-frequency components
    # signal_fft[:] = 0
    # signal_fft[10:] = 1 + 10j
    samples = np.fft.ifft(signal_fft).real  # Calculate the inverse FFT to get the filtered signal
    return samples


def cutoff_2(samples, cutoff_freq):
    # todo limit max acceleration
    #  keep on scale
    signal_fft = np.fft.fft(samples)  # Calculate the FFT of the signal
    # freqs = np.fft.fftfreq(len(samples))  # Calculate the frequency range of the signal
    # signal_fft[freqs > cutoff_freq] = 0  # Zero out the high-frequency components
    # cutoff_freq
    signal_fft[:] = 0
    signal_fft[10:] = 1 + 10j
    samples = np.fft.ifft(signal_fft).real  # Calculate the inverse FFT to get the filtered signal
    return samples


# todo add support for cutoff_freq: List[float]
cutoff = cutoff_1


def main():
    p = pyaudio.PyAudio()
    stream = p.open(output_device_index=2, format=pyaudio.paFloat32, channels=channels, rate=sample_rate, output=True)

    duration = 1
    sample_len = int(duration * sample_rate * channels)

    next_start = 0
    while True:
        t = np.arange(next_start, next_start + sample_len)
        next_start = t[-1] + 1
        t = t / sample_rate

        samples = np.sin(2 * np.pi * frequency * t)  # sin
        # samples = (frequency * t) % 1  # sin
        # lfo_signal = np.sin(2 * np.pi * lfo * t)
        # samples *= lfo_signal  # sin

        # cutoff_freq = lfo_signal * cutoff_diff + cutoff_low
        cutoff_freq = 10
        samples = cutoff(samples, cutoff_freq)

        samples *= volume

        # write samples to stream
        stream.write(samples.astype(np.float32).tobytes())

    # clean up
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
