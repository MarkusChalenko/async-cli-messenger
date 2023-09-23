from datetime import datetime

from user.user_model import User


class Message:
    def __init__(self, author: User, content: str):
        self.content: str = content
        self.author: str = author.nickname
        self.room = author.current_room
        self.timestamp: str = datetime.today().strftime('%H:%M:%S')

    def formatted_message(self) -> str:
        return f"({self.timestamp}) {self.author} >>> {self.content}"
