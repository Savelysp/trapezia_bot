from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from src.keyboards import get_phone_number_kb, main_panel_kb
from src.models import User
from src.settings import sessionmaker
from sqlalchemy import select
from aiogram.fsm.context import FSMContext
from src.states import UserStatesGroup


__all__ = ["router"]


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    text = "привет"
    await state.clear()
    await message.answer(
            text=text,
            reply_markup=main_panel_kb
            )


@router.message(F.text == "связь")
async def support_message(message: Message):
    text = "ссылка"
    await message.delete()
    await message.answer(
        text=text,
        )


@router.message(F.text == "запись")
async def entry_message(message: Message):
    async with sessionmaker() as session:
        try:
            await session.execute(
                select(User).where(User.id == message.from_user.id)
                )
        except Exception:
            text = "нет"
            await message.answer(
                text=text,
                reply_markup=get_phone_number_kb
                )
        else:
            text = "да"
            await message.answer(
                text=text,
                reply_markup=
                )


@router.message(F.contact)
async def collect_phone_number(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    # await state.set_state(state=UserStatesGroup.create.phone_number)
    await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(state=UserStatesGroup.create.name)
    text = "как к вам обращаться"
    await message.answer(
            text=text
            )


@router.message(UserStatesGroup.create.name)
async def set_user_name(message: Message, state: FSMContext):
    if len(message.text) > 32:
        text = f"имя {message.text} слишком длинное"
        await message.answer(
                text=text
                )
    else:
        state_data = await state.get_data()
        await state.clear()
        async with sessionmaker() as session:
            user = User(id=message.from_user.id, name=message.text, phone=state_data.phone_number)
            session.add(instance=user)
            try:
                await session.commit()
            except IntegrityError:
                await message.answer(text="ошибка")
            else:
                await message.answer(text="вы зареганы")



@router.callback_query(MainEntryCallbackData.filter(F.action == 'create'))
async def create_entry(message: Message):
    ...

