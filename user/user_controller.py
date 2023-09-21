from asyncio import StreamReader, StreamWriter

from command import CommandExecutor
from settings import Node
from user.user_model import User
from user.user_service import UserService
from utils import get_logger

logger = get_logger(Node.CLIENT)


class UserController:
    def __init__(self, r: StreamReader, w: StreamWriter):
        self.service = UserService(r, w)
        self.command = CommandExecutor()
        self.user: User | None = None
        self.r = r
        self.w = w

    async def authorize(self):
        self.w.write("Log in(1) | Registration(Other)\n".encode())
        chosen = (await self.r.readline()).decode().strip()
        self.user = await self._choose(chosen, self.service.login(), self.service.registration())
        self.w.write(f"Wellcome, { self.user.nickname }\n".encode())
        logger.debug(f"Authorized: {self.user}")
        return self.user

    async def handle_input(self):
        while True:
            if self.w.transport.is_closing():
                return Exception
            content = (await self.r.readline()).decode().strip()
            if not content:
                continue
            elif self.command.is_command(content, self.user):
                self.command.execute_command(content, self.user)
            else:
                self.service.send_message(content)

    async def _choose(self, chosen: str, *funcs):
        if chosen == '1':
            func_to_execute = funcs[0]
            return await func_to_execute
        else:
            func_to_execute = funcs[1]
            return await func_to_execute
