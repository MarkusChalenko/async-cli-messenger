from room.room_storage import RoomInMemoryStorage
from user.user_model import User
from user.user_storage import UserInMemoryStorage
from utils import get_logger

logger = get_logger()

user_storage: UserInMemoryStorage = UserInMemoryStorage()
room_storage: RoomInMemoryStorage = RoomInMemoryStorage()


class Command:
    def execute(self):
        pass


class CommandCreatePrivateRoom(Command):
    def __init__(self, user: User, second_user_login: str,):
        self.login = second_user_login
        self.user = user

    def execute(self):
        try:
            second_user: User = user_storage.get_by_login(self.login)

            have_room_already = room_storage.get_private_chat_room((self.user, second_user))
            if not have_room_already:
                room_storage.add_private_chat_room((self.user, second_user))

            self.user.set_room(room_storage.get_private_chat_room((self.user, second_user)))
        except:
            self.user.writer.write("No such user\n".encode())


class CommandChangeChatRoom(Command):
    def __init__(self, user: User, second_user_login: str):
        self.user = user
        self.second_user = user_storage.get_by_login(second_user_login)

    def execute(self):
        room = room_storage.get_private_chat_room((self.user, self.second_user))
        if room:
            self.user.set_room(room)
        else:
            self.user.writer.write(f"Cant find this room\n".encode())


class CommandChangeToCommonRoom(Command):
    def __init__(self, user: User):
        self.user = user

    def execute(self):
        self.user.set_room(room_storage.get_common_room())


class CommandGetUserRooms(Command):
    def __init__(self, user: User):
        self.user: User = user

    def execute(self):
        self.user.writer.write(f"Rooms:\n".encode())
        for name, room in room_storage.chat_rooms:
            if room.have_member(self.user):
                self.user.writer.write(f"{room.name}\n".encode())
        return 0


class CommandFactory:
    @staticmethod
    def create_command(command_call: str, user: User):
        command_call: list[str] = command_call.strip().split(' ')
        if command_call[0] == "/chat":
            return CommandCreatePrivateRoom(user, command_call[1])
        elif command_call[0] == "/goto":
            return CommandChangeChatRoom(user, command_call[1])
        elif command_call[0] == "/common":
            return CommandChangeToCommonRoom(user)
        elif command_call[0] == "/rooms":
            return CommandGetUserRooms(user)
        else:
            return None


class CommandExecutor:
    def __init__(self, command_factory: CommandFactory = CommandFactory):
        self.command_factory = command_factory

    def is_command(self, user_input, user: User):
        return True if self.command_factory.create_command(user_input, user) else False

    def execute_command(self, command_call, user: User):
        command = self.command_factory.create_command(command_call, user)
        if command:
            command.execute()
        else:
            print("Несуществующая команда")