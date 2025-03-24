import asyncio
import sys
from typing import IO


async def handle_connection(
    reader: asyncio.StreamReader, 
    writer: asyncio.StreamWriter
) -> None:
    addr = writer.get_extra_info("peername")
    print(f'connection from {addr!r}')
    
    while message := await reader.read(100):
        text = message.decode()
        print(f'received {text!r} from {addr!r}')
        print(f'sending {text!r}', file=sys.stderr)
        writer.write(message)
        await writer.drain()
        if text == 'quit\n':
            break
    print(f'closing connection from {addr!r}')
    writer.close()


async def main() -> None:
    server = await asyncio.start_server(
        handle_connection, '127.0.0.1', 8888
    )
    
    addr = server.sockets[0].getsockname() if server.sockets else 'Unknown'
    print(f'Serving on {addr}')
    
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
