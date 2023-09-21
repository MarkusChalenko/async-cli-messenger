from typing import Dict

from decorators import singleton
from room.chat_room import CommonRoom, PrivateRoom, ChatRoom
from settings import Node
from user.user_model import User
from utils import get_logger

logger = get_logger(Node.SERVER)


@singleton
class RoomInMemoryStorage:
    def __init__(self):
        self.common_room: CommonRoom = CommonRoom('Common')
        self.chat_rooms: Dict[tuple, ChatRoom] = {}

    def add_private_chat_room(self, members: tuple[User, User]):
        key = members
        self.chat_rooms[key] = PrivateRoom(f"{members[0].nickname}-{members[1].nickname}", list(members))

    def get_common_room(self) -> CommonRoom:
        return self.common_room

    def get_private_chat_room(self, members: tuple[User, User]) -> PrivateRoom | None:
        key = members
        room = self.chat_rooms.get(key, None)
        if not room:
            room = self.chat_rooms.get(key[::-1], None)
        return room
