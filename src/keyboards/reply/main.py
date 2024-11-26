from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = [
        "main_panel_kb",
        "get_phone_number_kb",
        ]

main_panel_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [
            KeyboardButton(
                text="запись"
            ),
            KeyboardButton(
                text="связь"
            )
        ]
    ]
)

get_phone_number_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='🖋 РЕГИСТРАЦИЯ',
                request_contact=True
            )
        ]
    ]
)

