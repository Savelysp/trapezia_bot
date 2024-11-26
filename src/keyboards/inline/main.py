from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

all = [
    "MainEntryCallbackData",
    "main_entry_ikb",
    ]


class MainEntryCallbackData(CallbackData, prefix='entry'):
    action: Literal['create', 'delete']


main_entry_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="lkfajsd",
                callback_data=MainEntryCallbackData(action='create').pack()
                ),
            InlineKeyboardButton(
                text="nnnnn",
                callback_data=MainEntryCallbackData(action='delete').pack()
                )
        ]
    ]
)

