import uuid
from typing import List

from decorators import singleton
from settings import Node
from user.user_model import User
from utils import get_logger

logger = get_logger(Node.SERVER)


@singleton
class UserInMemoryStorage:
    def __init__(self):
        self.users: List[User] = []

    def get_by_login(self, login: str) -> User:
        desired_user = [user for user in self.users if user.login == login]
        return desired_user[0] if desired_user else None

    def get_by_id(self, user_id: uuid) -> User:
        desired_user = [user for user in self.users if user.id == user_id]
        return desired_user[0] if desired_user else None

    def save(self, user: User) -> List[User]:
        self.users.append(user)
        logger.debug(f"UserInMemoryStorage | added new user: {user.id}")
        return self.users
