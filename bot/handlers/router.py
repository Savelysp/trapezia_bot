from aiogram import Router

from bot.handlers import v1

#TODO: Разобраться с ругательством линтера
bot_router = Router()
bot_router.include_router(router=v1.router)

