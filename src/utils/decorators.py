from aiogram.types import Message
from src.models import User
from src.settings import sessionmaker
from sqlalchemy import select
from src.keyboards import get_phone_number_kb


__all__ = ["check_user_existence"]

def check_user_existence(func):
    async def wrapper(message: Message):
        async with sessionmaker() as session:
            user = select(User)
            user = user.filter(User.id == message.from_user.id)
            result = await session.scalars(statement=user)
            if result.fetchall():
                return await func(message)
            else:
                text = "вы не зарегестрированы"
                await message.answer(
                        text=text,
                        reply_markup=get_phone_number_kb
                        )
    return wrapper

