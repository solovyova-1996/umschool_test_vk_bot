from vkbottle.bot import Message, BotLabeler
from bot.keyboards import keyboard_today_tomorrow, keyboard_main_menu
from bot.states import Afisha
from bot.support import get_afisha
from config import state_dispenser
from database.crud import UserOperations
from database.database import engine

afisha_labeler = BotLabeler()
afisha_labeler.vbml_ignore_case = True

user_crud = UserOperations(engine)


@afisha_labeler.message(text="Афиша")
async def afisha_start(message: Message):
    await message.answer(f"Выбери день", keyboard=keyboard_today_tomorrow)
    await state_dispenser.set(message.peer_id, Afisha.start)


@afisha_labeler.message(state=Afisha.start)
async def start_city(message: Message):
    city_user = user_crud.get_city_user_by_vk_id(message.from_id)
    if message.text.lower() in ["отмена", "хватит", "стоп"]:
        await state_dispenser.set(message.peer_id, Afisha.finish)
        await message.answer(f"Ты в главном меню:", keyboard=keyboard_main_menu)
    elif message.text == "Сегодня" or message.text == "Завтра":
        if city_user is not None:
            afisha_res = get_afisha(city_user, message.text)
            await message.answer(afisha_res, keyboard=keyboard_main_menu)
            await state_dispenser.set(message.peer_id, Afisha.finish)
        else:
            await message.answer("Произошла ошибка, попробуйте позже")
            await state_dispenser.set(message.peer_id, Afisha.finish)
    else:
        await message.answer("Произошла ошибка, попробуйте позже")
        await state_dispenser.set(message.peer_id, Afisha.finish)
