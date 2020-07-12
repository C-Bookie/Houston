import asyncio
from music.aiosm_midi.mido_io import MidoIO

from aiosm import Client


class MidiPiano(MidoIO, Client):
    def __init__(self, name, inport_names, outport_names):
        Client.__init__(name, addr='127.0.0.1')
        MidoIO.__init__(inport_names, outport_names)
        self.step_up = 0

        self.white_list_functions += [
            "midi_hex"
        ]

    async def run(self):
        await self.connect()
        await self.request("subscribe", "piano")  # comment out to disable receiving midi
        await asyncio.gather(
            super().run(),  # midi receiving
            # self.loop()  # midi transition
        )

    async def loop(self):
        asyncio.current_task().set_name(self.__name__ + "-Transmitter")
        while True:
            for inport in self.inports:
                for msg in inport.iter_pending():
                    await self.broadcast("piano", "midi_hex", msg.hex())
            await self.wait()

    def close(self):
        super(Client, self).close()
        super(MidoIO, self).close()


if __name__ == "__main__":
    piano = MidiPiano("Piano",
                      # ('masterkey 61 0',),
                      (),
                      ('Alex 1',))
    asyncio.run(piano.run())
