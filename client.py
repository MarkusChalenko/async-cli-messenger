from asyncio import StreamReader, StreamWriter

from settings import Node
from user.user_controller import UserController
from user.user_model import User
from utils import get_logger

logger = get_logger(Node.CLIENT)


class Client:
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer
        self.user_controller = UserController(reader, writer)

    async def user_authorize(self):
        user: None | User = None
        while not user:
            try:
                user: User = await self.user_controller.authorize()
            except BaseException:
                continue
        user.clients.append(self)
        return user

    async def handle_input(self):
        try:
            await self.user_controller.handle_input()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
