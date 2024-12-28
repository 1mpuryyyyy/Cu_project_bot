import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.start import router as start_router
from handlers.weather import router as weather_router

TOKEN = 'YOR_KEY'


async def run():
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage, bot=bot)
    dp.include_router(start_router)
    dp.include_router(weather_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
