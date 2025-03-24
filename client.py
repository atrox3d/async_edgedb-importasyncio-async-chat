import asyncio
from os import write
import sys
from typing import IO


async def send_file(file: IO[str]) -> None:
    
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888
    )
    
    for message in file:
        # writer.write(message.encode())
        # await writer.drain()
        
        # simulate network slowness
        for ch in message.encode():             # get the bytes from message
            await asyncio.sleep(0.1)            # simulate network slowness
            writer.write(bytes([ch]))           # send a single byte array???
            print(
                f'{hex(ch)[2:].upper():0>2}',   # prints hex values without prefix
                end=''
            )
            sys.stdout.flush()                  # i'm not sure about this
            if ch == 10:                        # i think this is \n
                print()                         # print new line
            
        data = await reader.read(100)
        text = data.decode()
        print(f'received {text!r}')
        
        if text == 'quit\n':
            break

    print('closing connection')
    writer.close()


if __name__ == '__main__':
    asyncio.run(send_file(sys.stdin))
