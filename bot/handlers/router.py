from aiogram import Router

from bot.handlers import v1

bot_router = Router()
bot_router.include_router(router=v1.router)
