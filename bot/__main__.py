from aiohttp.web import (
    Application,
    Request,
    RouteTableDef,
    json_response,
    run_app,
)
from src.settings import bot, dispatcher, settings

from .handlers import bot_router


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
            url=settings.DOMAIN.unicode_string() + 'webhook', 
            allowed_updates=['message', 'callback_query'], 
            secret_token=settings.TELEGRAM_SECRET_TOKEN.get_secret_value()
            )
    dispatcher.include_router(router=bot_router)


async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)


app = Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

router = RouteTableDef()


@router.post(path='/webhook')
async def get_webhook(request: Request):
    try:
        # print(await request.json())
        await dispatcher.feed_raw_update(bot=bot, update=await request.json())
    except Exception as e:
        print(e)
    return json_response(data={'status': 'OK'})


app.add_routes(routes=router)


if __name__ == '__main__':
    run_app(
            app=app,
            host='0.0.0.0',
            port=80
            )

