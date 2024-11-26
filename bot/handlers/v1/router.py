from aiogram import Router

from bot.handlers.v1 import echo

router = Router()
router.include_router(router=echo.router)

