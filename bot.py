import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = ''


async def run():
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage, bot=bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
