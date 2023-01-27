"""The purpose of this script is to prototype a hacked aiosm.Radio to use headers

todo


"""
import asyncio
import aiosm

USING_HEADER = True
HEADER_LEN = 4  # size in bytes


class HackedRadio(aiosm.Radio):
    def prepare(self, message: str) -> bytes:
        if not USING_HEADER:
            return super().prepare(message)

        # todo: use header
        data = message.encode()

        header = r""
        return header + data

    def unpack(self, data: bytes) -> str:
        if not USING_HEADER:
            return super().unpack(data)

        return data[0:-self.ETX_LEN]


aiosm.Radio = HackedRadio


def main():
    loop = asyncio.get_event_loop()

    host = aiosm.Host()

    task1 = loop.create_task(host.run())
    task1.set_name("Host")

    asyncio.gather(task1)
    # asyncio.gather(task2)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
