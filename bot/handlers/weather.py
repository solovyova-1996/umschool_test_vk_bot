from vkbottle.bot import Message, BotLabeler
from bot.keyboards import keyboard_today_tomorrow, keyboard_main_menu
from bot.states import Weather
from bot.support import get_weather, weather_tomorrow, parse_weather
from config import state_dispenser
from database.crud import UserOperations
from database.database import engine

weather_labeler = BotLabeler()
weather_labeler.vbml_ignore_case = True

user_crud = UserOperations(engine)


@weather_labeler.message(text="Погода")
async def weather_start(message: Message):
    await message.answer(f"Выбери день", keyboard=keyboard_today_tomorrow)
    await state_dispenser.set(message.peer_id, Weather.start)


@weather_labeler.message(state=Weather.start)
async def start_city(message: Message):
    city_user = user_crud.get_city_user_by_vk_id(message.from_id)
    if message.text.lower() in ["отмена", "хватит", "стоп"]:
        await state_dispenser.set(message.peer_id, Weather.finish)
        await message.answer(f"Ты в главном меню:", keyboard=keyboard_main_menu)
    elif message.text == "Сегодня":
        if city_user is not None:
            weather = get_weather(city_user)
            if weather is not None:
                await message.answer(
                    f"Погода сегодня ({city_user}) -  {weather['weather'][0]['description']}\n Температура: {weather['main']['temp']} °C \nОщущается как {weather['main']['feels_like']} °C",
                    keyboard=keyboard_main_menu)
                await state_dispenser.set(message.peer_id, Weather.finish)
            else:
                await message.answer("Произошла ошибка, попробуйте позже")
                await state_dispenser.set(message.peer_id, Weather.finish)
        else:
            await message.answer("Произошла ошибка, попробуйте позже")
            await state_dispenser.set(message.peer_id, Weather.finish)
    elif message.text == "Завтра":
        if city_user is not None:
            weather = weather_tomorrow(city_user)
            if weather is not None:
                await message.answer(parse_weather(weather, city_user), keyboard=keyboard_main_menu)
                await state_dispenser.set(message.peer_id, Weather.finish)
            else:
                await message.answer("Произошла ошибка, попробуйте позже")
                await state_dispenser.set(message.peer_id, Weather.finish)
    else:
        await message.answer("Произошла ошибка, попробуйте позже")
        await state_dispenser.set(message.peer_id, Weather.finish)
