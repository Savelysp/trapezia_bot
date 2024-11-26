from aiogram.fsm.state import State, StatesGroup

__all__ = [
        "UserStatesGroup",
        ]


class CreateUserStatesGroup(StatesGroup):
    name = State()
    phone_number = State()


class UserStatesGroup(StatesGroup):
    create = CreateUserStatesGroup

