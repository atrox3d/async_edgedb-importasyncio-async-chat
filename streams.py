import asyncio
import sys
from typing import AsyncIterator


async def split_lines(reader: asyncio.StreamReader) -> AsyncIterator[bytes]:
    data = b''
    try:
        while data := data + await reader.read(100):
            if b'\n' in data:
                message, data = data.split(b'\n', 1)
                yield message
    except ConnectionResetError:
        pass

    if data:
        yield data


async def write(writer: asyncio.StreamWriter, message: bytes) -> None:
    print('sending bytes: ', end='')
    if not message.endswith(b'\n'):
        message += b'\n'
    
    for ch in message:
        await asyncio.sleep(0.1)
        writer.write(bytes([ch]))
        print(
            f'{hex(ch)[2:].upper():0>2}',
            end=''
        )
        sys.stdout.flush()
        if ch == 10:
            print()
    await writer.drain()
