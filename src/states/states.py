from aiogram.fsm.state import State, StatesGroup

__all__ = [
        "UserStatesGroup",
        ]


class CreateUserStatesGroup(StatesGroup):
    name = State()
    phone_number = State()

class CreateEntryStatesGroup(StatesGroup):
    approve = State()
    time = State()

class UserStatesGroup(StatesGroup):
    create_user = CreateUserStatesGroup
    create_entry = CreateEntryStatesGroup

