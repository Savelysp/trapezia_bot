from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

__all__ = []


class EntryCallbackData(CallbackData, prefix="entry"):
    action: Literal["create", "delete"]

