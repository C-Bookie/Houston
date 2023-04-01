import time

from music.aiosm_midi.qwerty_piano import QwertyPiano
from music.aiosm_midi.mido_io import MidoIO


class QwertyBroadcast(MidoIO, QwertyPiano):
    def __init__(self):
        MidoIO.__init__(self, (), ('Alex 1',))
        QwertyPiano.__init__(self)

    def run(self):
        while True:
            for message in self.get_messages():
                if message is None:
                    return
                for outport in self.outports:
                    print(message)
                    outport.send(message)

            time.sleep(1/60)


if __name__ == "__main__":
    piano = QwertyBroadcast()
    piano.run()
