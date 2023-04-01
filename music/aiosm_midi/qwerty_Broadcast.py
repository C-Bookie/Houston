from music.aiosm_midi.qwerty_piano import QwertyPiano
from aiosm import Client
import asyncio


class QwertyBroadcast(Client, QwertyPiano):
    def __init__(self):
        Client.__init__("qwerty_broadcast")
        QwertyPiano.__init__()

    async def run(self):
        await self.connect()
        # await self.request("subscribe", "keyboard")
        await asyncio.gather(
            super().run(),
            self.loop()
        )

    async def loop(self):
        asyncio.current_task().set_name(self.__name__ + "-Transmitter")
        while True:
            if not self.ready:  # todo add to self.wait()
                return
            for message in self.get_messages():
                if message is None:
                    await self.quit()
                await self.broadcast("piano", "midi_hex", message.hex())

            await self.wait()


if __name__ == "__main__":
    piano = QwertyBroadcast()
    asyncio.run(piano.run())
