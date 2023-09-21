import uuid
from asyncio import StreamReader, StreamWriter


class User:
    nickname: str = 'AnonUser'
    login: str
    password: str
    current_room: None
    # Чтоб добавить аннотацию типов нужно вынести интерфейс комнаты
    # в отдельный файл, т.к. сейчас круговая зависимость. Как ее решить я не понимаю,
    # так как у меня всегда 1 модуль остается без аннотации

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.id: uuid = uuid.uuid4()
        self.reader: StreamReader = reader
        self.writer: StreamWriter = writer

    def set_room(self, room):
        self.current_room.member_leave(self)
        self.current_room = room
        self.writer.write(f"Your room was changed to: {room.name}\n".encode())
        self.current_room.member_enter(self)
