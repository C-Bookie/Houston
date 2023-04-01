from pedalboard import Pedalboard, Chorus, Compressor, Delay, Gain, Reverb, Phaser
from pedalboard.io import AudioStream



# Open up an audio stream:
with AudioStream(
  input_device_name=AudioStream.input_device_names[0],
  output_device_name=AudioStream.output_device_names[1]
) as stream:
    # Audio is now streaming through this pedalboard and out of your speakers!
    stream.plugins = Pedalboard([
      # Compressor(threshold_db=-50, ratio=25),
      # gain,
        Gain(gain_db=1),
      # Chorus(),
      # Phaser(),
      # Convolution("./guitar_amp.wav", 1.0),
      # Reverb(room_size=0.25),
    ])

    while True:
        msg = input("Press enter to stop streaming...")
        match msg:
            case "q":
                break
            case _:
                value = int(msg)
                breakpoint()
