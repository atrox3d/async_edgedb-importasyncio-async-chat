import asyncio
import contextlib
import sys
from typing import IO

from streams import write, split_lines


async def handle_reads(reader: asyncio.StreamReader) -> None:
    async for message in split_lines(reader):
        text = message.decode()
        print(f'received {text!r}')
        if text == 'quit\n':
            break





async def send_file(file: IO[str]) -> None:
    
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    read_handler = asyncio.create_task(handle_reads(reader))
    
    for message in file:
        # simulate network slowness
        await write(writer, message.encode())
    read_handler.cancel()
    
    with contextlib.suppress(asyncio.CancelledError):
        await read_handler
        

    print('closing connection')
    writer.close()


if __name__ == '__main__':
    asyncio.run(send_file(sys.stdin))
