from abc import ABC, abstractmethod

from datetime import datetime
from typing import List, Dict

from message.message import Message
from message.message_storage import MessageInMemoryStorage
from user.user_model import User
from utils import get_logger

logger = get_logger()


class ChatRoom:
    def __init__(self, name: str, members: List[User]):
        self.name: str = name
        self.members: List[User] = members
        self.member_leave_at: Dict[User, str | None] = {}
        self.message_storage: MessageInMemoryStorage = MessageInMemoryStorage()

    def send_message(self, message: Message) -> bool:
        try:
            self.message_storage.save_message(message)
            for member in self.members:
                if member.nickname == message.author:
                    continue
                elif member.current_room != self:
                    continue
                else:
                    member.writer.write(message.formatted_message().encode())
                    return True
        except:
            return False

    def get_messages_after_leave(self, user: User) -> List[Message]:
        member_leave_time: str = self.member_leave_at[user]
        return self.message_storage.get_after_time(member_leave_time)

    def add_member(self, member: User) -> List[User]:
        self.members.append(member)
        return self.members

    def member_leave(self, member: User) -> None:
        self.member_leave_at[member] = datetime.today().strftime('%H:%M:%S')

    def member_enter(self, member: User) -> None:
        try:
            messages_to_send: List[Message] = self.get_messages_after_leave(member)
            self.member_leave_at[member] = None
            [member.writer.write(message.formatted_message().encode()) for message in messages_to_send]
        except:
            # на тот случай, когда комната только создается
            pass

    def have_member(self, member: User) -> bool:
        return True if member in self.members else False



class CommonRoom(ChatRoom):
    def __init__(self, name: str = "Common", members: List[User] = []):
        super().__init__(name, members)

    def get_messages(self):
        pass

    def get_online_members(self):
        return self.members


class PrivateRoom(ChatRoom):
    def __init__(self, name: str = "Private", members: List[User] = []):
        super().__init__(name, members)

    def get_messages(self):
        pass

    def get_online_members(self):
        return self.members

    def add_member(self, members: List[User]) -> List[User]:
        self.members = self.members + members
        return self.members
