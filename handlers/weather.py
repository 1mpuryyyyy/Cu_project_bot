from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import StateFilter
from services.weather_service import get_location_key, get_weather_data, get_weather_info

router = Router(name="weather")


# Состояния для FSM
class WeatherFSM(StatesGroup):
    cities = State()
    time = State()


# CallbackData для кнопок выбора дней
class DaysCallback(CallbackData, prefix="days"):
    days: int


# Обработка команды /weather
@router.message(F.text, Command("weather"))
async def weather_start(message: Message, state: FSMContext):
    await message.answer(
        "Введите названия городов (начальный, конечный и, при необходимости, промежуточные) "
        "на отдельных строках. Например:\n\nМосква\nСанкт-Петербург\nВеликий Новгород"
    )
    await state.set_state(WeatherFSM.cities)


# Обработка ввода городов
@router.message(WeatherFSM.cities)
async def process_cities(message: Message, state: FSMContext):
    cities = message.text.split("\n")
    if len(cities) < 2:
        await message.answer("Необходимо ввести хотя бы начальный и конечный города.")
        return

    # Сохраняем города в состояние
    await state.update_data(cities=cities)

    # Создаём инлайн-клавиатуру для выбора количества дней
    builder = InlineKeyboardBuilder()
    for days in range(2, 6):
        builder.row(InlineKeyboardButton(text=f"{days} дня", callback_data=DaysCallback(days=days).pack()))

    await message.answer("Выберите временной интервал прогноза:", reply_markup=builder.as_markup())
    await state.set_state(WeatherFSM.time)


# Обработка выбора времени (дней)
@router.callback_query(DaysCallback.filter(), StateFilter(WeatherFSM.time))
async def process_days(callback: CallbackQuery, callback_data: DaysCallback, state: FSMContext):
    data = await state.get_data()
    cities = data.get("cities")
    days = callback_data.days

    results = []
    for city in cities:
        location_key = get_location_key(city)
        print(f"Location key for {city}: {location_key}")

        if location_key in [None, "401"]:
            results.append(f"Город {city}: Ошибка получения данных.")
            continue

        weather_data = get_weather_data(location_key)
        print(f"Weather data for {city}: {weather_data}")

        if weather_data:
            weather_info = get_weather_info(weather_data)
            forecast = "\n".join(
                f"Дата: {day['date']}\n"
                f"Мин: {day['temperature_min']}°C, Макс: {day['temperature_max']}°C\n"
                f"Ветер: {day['wind_speed']} км/ч\n"
                f"Вероятность осадков: {day['precipitation_probability']}%"
                for day in weather_info[:days]
            )
            results.append(f"Прогноз для {city}:\n{forecast}")
        else:
            results.append(f"Город {city}: Ошибка получения прогноза.")

    # Отправляем результат пользователю
    print("Results to send:", results)
    await callback.message.answer("\n\n".join(results))
    await state.clear()
