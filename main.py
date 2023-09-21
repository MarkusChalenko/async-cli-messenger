import asyncio

from server import Server

if __name__ == '__main__':
    srv = Server()
    asyncio.run(srv.listen())
