from asyncio import StreamReader, StreamWriter
from typing import Optional

from message.message import Message
from user.user_model import User
from user.user_storage import UserInMemoryStorage


class UserService:
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.r = reader
        self.w = writer
        self.user: User = User()
        self.storage = UserInMemoryStorage()

    async def login(self) -> Optional[User]:
        login: str = await self._login_request()
        password: str = await self._password_request()
        self.user: User = self.storage.get_by_login(login)
        if self.user.password == password:
            self.w.write(f"Hello {self.user.nickname}!\n".encode())
            return self.user
        else:
            self.w.write("Login or password is incorrect\n".encode())
            return None

    async def registration(self) -> User:
        self.user.login = await self._login_registration_request()
        self.user.password = await self._password_registration_request()
        self.user.nickname = await self._nickname_registration_request()

        self.storage.save(self.user)
        self.w.write("You have successfully registered\n".encode())

        return self.user

    def send_message(self, content: str):
        message: Message = Message(self.get_user(), content)
        self.user.current_room.send_message(message)
        return True

    def get_user(self) -> User:
        return self.user

    async def _login_registration_request(self) -> str:
        self.w.write("Enter your login\n".encode())
        login = (await self.r.readline()).decode().strip()
        while self._check_login(login):
            self.w.write("This login is already occupied, choose another one\n".encode())
            login = (await self.r.readline()).decode().strip()

        return login

    async def _password_registration_request(self) -> str:
        self.w.write("Enter your password\n".encode())
        password = (await self.r.readline()).decode().strip()
        password_repeat = None
        while password != password_repeat:
            self.w.write("Enter your password again\n".encode())
            password_repeat = (await self.r.readline()).decode().strip()
            if not self._check_password(password_repeat, password):
                self.w.write("Incorrect password\n".encode())
        return password

    async def _nickname_registration_request(self) -> str:
        self.w.write("Enter your nickname\n".encode())
        nickname = (await self.r.readline()).decode().strip()
        while self._check_nickname(nickname):
            self.w.write("This nickname is already occupied, choose another one\n".encode())
            nickname = (await self.r.readline()).decode().strip()
        return nickname

    async def _login_request(self) -> str:
        self.w.write(f"Enter your login\n".encode())
        return (await self.r.readline()).decode().strip()

    async def _password_request(self) -> str:
        self.w.write(f"Enter your password\n".encode())
        return (await self.r.readline()).decode().strip()

    def _check_password(self, passed_password: str, password: str | None = None) -> bool:
        if not password:
            password = self.user.password
        return passed_password == password

    def _check_login(self, login: str) -> bool:
        return bool(self.storage.get_by_login(login))

    def _check_nickname(self, nickname: str) -> bool:
        return bool(self.storage.get_by_nickname(nickname))
