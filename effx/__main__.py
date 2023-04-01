# Don't do import *! (It just makes this example smaller)
from pedalboard import *
from pedalboard.io import AudioFile
from pedalboard.pedalboard import Pedalboard

with AudioFile('guitar-input.wav', 'r') as f:
  audio = f.read(f.frames)
  samplerate = f.samplerate

# Make a pretty interesting sounding guitar pedalboard:
board = Pedalboard([
    Compressor(threshold_db=-50, ratio=25),
    Gain(gain_db=30),
    Chorus(),
    LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
    Phaser(),
    Convolution("./guitar_amp.wav", 1.0),
    Reverb(room_size=0.25),
])

# Pedalboard objects behave like lists, so you can add plugins:
board.append(Compressor(threshold_db=-25, ratio=10))
board.append(Gain(gain_db=10))
board.append(Limiter())

# ... or change parameters easily:
board[0].threshold_db = -40

# Run the audio through this pedalboard!
effected = board(audio, samplerate)

# Write the audio back as a wav file:
with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
  f.write(effected)