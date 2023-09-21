from typing import List

from message.message import Message
from settings import Node
from utils import get_logger

logger = get_logger(Node.SERVER)


class MessageInMemoryStorage:
    def __init__(self):
        self.messages: List[Message] = []

    def save_message(self, message: Message) -> None:
        self.messages.append(message)

    def get_after_time(self, time: str) -> List[Message]:
        index = [i for i in range(len(self.messages)) if self.messages[i].timestamp > time][0]
        return self.messages[index:]

