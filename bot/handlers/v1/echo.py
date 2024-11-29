from datetime import datetime
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from src.keyboards import (
    MainEntryCallbackData,
    approve_ikb,
    choose_service_ikb,
    delete_entry_ikb,
    # get_phone_number_kb,
    main_panel_kb,
    # ApproveCallbackData
)
from src.models import User, Service, Entry
from src.settings import sessionmaker
from src.states import UserStatesGroup
from src.utils import check_user_existence

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


@router.message(F.text == "записаться")
@check_user_existence
async def create_entry_message(message: Message):
    await message.delete()
    # async with sessionmaker() as session:
    #     service = Service(id=2, name='test2', title='test', price=12.00)
    #     session.add(instance=service)
    #     try:
    #         await session.commit()
    #     except IntegrityError:
    #         print("сервис не создан")
    async with sessionmaker() as session:
        services = select(Service)
        services = await session.scalars(statement=services)
        text = "да"
        await message.answer(
            text=text,
            reply_markup=choose_service_ikb(services=services.fetchall())
            )


@router.callback_query(MainEntryCallbackData.filter(F.action == 'choose'))
async def choose_service_message(callback: CallbackQuery, callback_data: MainEntryCallbackData, state: FSMContext):
    await state.clear()
    await state.update_data(service_id=callback_data.id)
    await state.set_state(state=UserStatesGroup.create_entry.time)
    await callback.message.edit_text(
            text="введите время"
            )


@router.message(UserStatesGroup.create_entry.time)
async def set_entry_time(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(time=message.text)
    await state.set_state(state=UserStatesGroup.create_entry.approve)
    state_data = await state.get_data()
    await message.answer(
            text=f"{state_data["service_id"]} и {state_data["time"]}",
            reply_markup=approve_ikb
            )


@router.callback_query(UserStatesGroup.create_entry.approve, F.data == "yes") 
async def approve_entry(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await state.clear()
    entry = Entry(
            user_id=callback.from_user.id, 
            service_id=int(state_data["service_id"]), 
            entry_time=datetime.strptime(state_data["time"], "%Y-%m-%d %H-%M")
            )
    async with sessionmaker() as session:
        session.add(instance=entry)
        try:
            await session.commit()
        except Exception as e:
            print(e, "это наша ошибка")
            print("хрень какая-то")
        else:
            await callback.message.edit_text(
                    text="супер",
                    )
            await callback.message.edit_reply_markup(
                    reply_markup=main_panel_kb
                    )


@router.callback_query(UserStatesGroup.create_entry.approve, F.data == "no") 
async def cancel_entry(callback: CallbackQuery, state: FSMContext):
    state.clear()
    await callback.message.edit_text(
            text="ok"
            )
 

@router.message(F.text == "мои записи")
@check_user_existence
async def check_entries(message: Message):
    await message.delete()
    async with sessionmaker() as session:
        entries = select(Entry)
        entries = entries.filter(Entry.user_id == message.from_user.id)
        entries = await session.scalars(statement=entries)
        entries = [entry for entry in entries.fetchall()]
        if entries:
            for entry in entries:
                await message.answer(
                        text=f"{entry.entry_time}", 
                        reply_markup=delete_entry_ikb(entry=entry)
                        )
        else:
            await message.answer(text="d", reply_markup=main_panel_kb)


@router.callback_query(MainEntryCallbackData.filter(F.action == "delete"))
async def delete_entry(callback: CallbackQuery, callback_data: MainEntryCallbackData):
    await callback.message.delete()
    async with sessionmaker() as session:
        await session.execute(delete(Entry).filter(Entry.entry_time == datetime.strptime(callback_data.id, "%Y-%m-%d %H-%M-%S")))
        await session.commit()



@router.message(F.contact)
async def collect_phone_number(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(state=UserStatesGroup.create_user.name)
    text = "как к вам обращаться"
    await message.answer(text=text)

    
@router.message(UserStatesGroup.create_user.name)
async def set_user_name(message: Message, state: FSMContext):
    await message.delete()
    if len(message.text) > 32:
        text = f"имя {message.text} слишком длинное"
        await message.answer(text=text)
    else:
        state_data = await state.get_data()
        await state.clear()
        async with sessionmaker() as session:
            user = User(id=message.from_user.id, name=message.text, phone=state_data["phone_number"])
            session.add(instance=user)
            try:
                await session.commit()
            except IntegrityError:
                await message.answer(text="ошибка")
            else:
                await message.answer(text="вы зареганы", reply_markup=main_panel_kb)

