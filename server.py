from asyncio import StreamReader, StreamWriter, start_server
from typing import Dict

from room.chat_room import CommonRoom
from client import Client
from room.room_storage import RoomInMemoryStorage
from settings import Node
from user.user_model import User
from utils import get_logger

logger = get_logger(Node.SERVER)

room_storage: RoomInMemoryStorage = RoomInMemoryStorage()


class Server:
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.common_room: CommonRoom = room_storage.get_common_room()
        self.host = host
        self.port = port
        self.clients: Dict[User, Client] = {}

    async def client_connected(self, reader: StreamReader, writer: StreamWriter):
        logger.info("Someone are connected")
        client = Client(reader, writer)
        await client.user_authorize()
        self._add_member_to_common_room(client)
        await client.handle_input()

    async def listen(self):
        logger.info("Starting server ...")
        srv = await start_server(
            self.client_connected, self.host, self.port)

        logger.info("Server started successfully")
        async with srv:
            await srv.serve_forever()

    def _add_member_to_common_room(self, member: Client):
        logger.info(f"Common Room | added user { member.user.nickname }")
        self.common_room.add_member(member.user)
        member.user.current_room = room_storage.get_common_room()
        self._send_last_messages(member)
        logger.info(f"Common Room | users online: { self.common_room.get_online_members() }")

    def _send_last_messages(self, member: Client, count: int = 20):
        for message in self.common_room.message_storage.messages[-count:]:
            member.user.writer.write(f"{message.formatted_message()}".encode())
        return 0
