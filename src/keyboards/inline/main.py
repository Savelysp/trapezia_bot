from datetime import datetime
from typing import Any, Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import PositiveInt

from src.models import Service, Entry

__all__ = [
    "MainEntryCallbackData",
    "approve_ikb",
    "delete_entry_ikb",
    "choose_service_ikb",
    # "ApproveCallbackData"
    ]


class MainEntryCallbackData(CallbackData, prefix='entry'):
    id: PositiveInt | str
    action: Literal['delete', 'choose']


# class ApproveCallbackData(CallbackData, prefix="approve"):
#     action: Literal["yes", "no"]


approve_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ДА", callback_data="yes"),
            InlineKeyboardButton(text="НЕТ", callback_data="no"),
        ]
    ]
)


def delete_entry_ikb(entry: Entry):
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="delete", 
                        # callback_data=str(entry.entry_time)
                        callback_data=MainEntryCallbackData(id=str(entry.entry_time).replace(":", "-"), action="delete").pack()
                        )
                    ]
                ]
            )


def choose_service_ikb(services: Service):
    builder = InlineKeyboardBuilder()
    for service in services:
        builder.row(InlineKeyboardButton(
            text=service.name,
            callback_data=MainEntryCallbackData(id=service.id, action="choose").pack()
            )
        )
    return builder.as_markup()

