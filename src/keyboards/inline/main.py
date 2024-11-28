from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import PositiveInt

from src.models import Service

__all__ = [
    "MainEntryCallbackData",
    "approve_ikb",
    "delete_entry_ikb",
    "choose_service_ikb",
    # "ApproveCallbackData"
    ]


class MainEntryCallbackData(CallbackData, prefix='entry'):
    id: PositiveInt
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


def delete_entry_ikb(service: Service):
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="delete", 
                        callback_data=MainEntryCallbackData(id=service.id, action="delete").pack()
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

