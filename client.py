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
        self.user: None | User = None
        self.user_controller = UserController(reader, writer)

    async def user_authorize(self):
        self.user: User = await self.user_controller.authorize()
        return self.user

    async def handle_input(self):
        try:
            await self.user_controller.handle_input()
        except BaseException as ex:
            return ex
