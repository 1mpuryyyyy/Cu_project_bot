from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router(name='start')

@router.message(F.text, Command('start'))
async def start(message: Message):
    await message.answer('Я могу помочь определить погоду во время поездки.\n'
                         'Нажми /weather, чтобы узнать погоду!')



@router.message(F.text, Command("help"))
async def help(message: Message):
    await message.answer(
        "Список команд:\n"
        "/start - начать работу с ботом\n"
        "/help - получить список команд\n"
        "/weather - получить прогноз погоды\n"
    )
