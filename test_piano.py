import mido
import pygame.midi

import connection


class Piano(connection.Client):
    def __init__(self):
        super().__init__()
        pygame.midi.init()
        self.midiPort = mido.open_output("moo 1")

        self.white_list_functions += [
            "note",
            "sustain"
        ]

    def connect(self):
        super().connect()
        self.send_data({
            "type": "register",
            "args": [
                "piano",
                2077
            ]
        })

    def note(self, note, down, vel=0.5):
        if 0 <= note <= 127:
            command = 'note_on' if down else 'note_off'
            vel = int(vel*127)
            msg = mido.Message(command, note=note, velocity=vel)
            self.midiPort.send(msg)
            print(pygame.midi.midi_to_ansi_note(note) + ": " + command)
        else:
            print("Note out of range: " + str(note))

    def sustain(self, down):
        value = 127 if down else 0
        msg = mido.Message("control_change", control=64, value=value)
        self.midiPort.send(msg)
        print("Sustain " + ("down" if down else "up"))


if __name__ == "__main__":
    piano = Piano()
    piano.run()


    # pygame.midi.quit()
