import uuid
from typing import List


class User:
    # Чтоб добавить аннотацию типов нужно вынести интерфейс комнаты
    # в отдельный файл, т.к. сейчас круговая зависимость. Как ее решить я не понимаю,
    # так как у меня всегда 1 модуль остается без аннотации

    def __init__(self):
        self.id: uuid = uuid.uuid4()
        self.nickname: str = 'AnonUser'
        self.login: str | None = None
        self.password: str | None = None
        self.current_room = None
        self.clients: List = []

    def set_room(self, room):
        self.current_room.member_leave(self)
        self.current_room = room
        self.send_content(f"Your room was changed to: {room.name}")
        self.current_room.member_enter(self)

    def send_content(self, content):
        for client in self.clients:
            client.writer.write(f"{content}\n".encode())
