import time

import pyaudio
import mido
import numpy as np

# set parameters
filename = 'LINCPOCH.midi'
sample_rate = 44100
channels = 1
volume = 0.5
tempo = 120

# initialize PyAudio
p = pyaudio.PyAudio()

# create stream
stream = p.open(format=pyaudio.paFloat32, channels=channels, rate=sample_rate, output=True)

notes_on = {}

# open MIDI file
midi_file = mido.MidiFile(filename)

# process MIDI messages
for message in midi_file.play():

    duration = message.time

    if duration > 0:
        notes_up = {note: vel for note, vel in notes_on.items() if vel != 0}
        if len(notes_up) > 1:
            raise Exception("hmm")
        if len(notes_up) == 0:
            time.sleep(duration)

        note, vel = next(iter(notes_up.items()))

        # calculate frequency of note
        frequency = 440 * 2 ** ((note - 69) / 12)

        # generate samples for note
        samples = np.zeros(int(duration * sample_rate * channels))
        t = np.arange(len(samples)) / sample_rate
        samples = volume * np.sin(2 * np.pi * frequency * t)

        # write samples to stream
        stream.write(samples.astype(np.float32).tobytes())

    # skip non-note messages
    if not isinstance(message, mido.Message):
        raise Exception("hmm")

    note = message.note
    velocity = message.velocity

    if message.type == 'note_on':
        notes_on[note] = velocity

    if message.type == 'note_off':
        notes_on[note] = 0


# clean up
stream.stop_stream()
stream.close()
p.terminate()
