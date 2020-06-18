import asyncio
import mido

from aiosm import Client


class MidiPiano(Client):
    def __init__(self, name, inport_names, outport_names):
        super().__init__(name)
        self.step_up = 0

        self.white_list_functions += [
            "midi_hex"
        ]

        self.inports = [mido.open_input(inport_name) for inport_name in inport_names]
        self.outports = [mido.open_output(outport_name) for outport_name in outport_names]

    def midi_hex(self, hex):
        msg = mido.Message.from_hex(hex)
        for outport in self.outports:
            outport.send(msg)

    async def run(self):
        await self.connect()
        await self.request("subscribe", "piano")  # comment out to disable receiving midi
        await asyncio.gather(
            super().run(),
            # self.loop()  # comment out to disable midi transition
        )

    async def loop(self):
        asyncio.current_task().set_name(self.__name__ + "-Transmitter")
        while True:
            for inport in self.inports:
                for msg in inport.iter_pending():
                    await self.broadcast("piano", "midi_hex", msg.hex())
            await self.wait()

    def close(self):
        super().close()
        for outport in self.outports:
            outport.close()
    # self.inport.close()


if __name__ == "__main__":
    piano = MidiPiano("Piano",
                      # ('masterkey 61 0',),
                      (),
                      ('Alex 1',))
    asyncio.run(piano.run())
