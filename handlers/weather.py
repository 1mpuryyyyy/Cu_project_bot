from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from weather_service import

router = Router(name='weather_start_city')


class WeatherFSM(StatesGroup):
    city = State()
    time = State()



class DaysCallback(CallbackData, prefix="days"):
    days: int


@router.message(F.text, Command('weather'))
async def city(message: Message, state: FSMContext):
    await message.answer('Введи названия городов на отдельных строках: ')
    await state.set_state(WeatherFSM.city)


@router.message(WeatherFSM.city)
async def city_input(message: Message, state: FSMContext):
    if len(message.text.split('\n')) < 2:
        await message.answer('Введите не менее 2х городов')
        return
    await state.update_data(...)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='2 дня',
                                     callback_data=DaysCallback(days=2).pack()))
    builder.row(InlineKeyboardButton(text='3 дня',
                                     callback_data=DaysCallback(days=3).pack()))
    builder.row(InlineKeyboardButton(text='4 дня',
                                     callback_data=DaysCallback(days=4).pack()))
    builder.row(InlineKeyboardButton(text='5 дней',
                                     callback_data=DaysCallback(days=5).pack()))
    await message.answer('Выберите временной интервал', reply_markup=builder.as_markup())
    await state.set_state(WeatherFSM.time)


@router.message(WeatherFSM.time)
async def time(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Погода')
    await state.clear()