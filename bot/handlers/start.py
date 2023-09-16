import vk_api

from vkbottle.bot import Message, BotLabeler

from bot.keyboards import keyboard_yes_no, keyboard_main_menu
from bot.states import AddCity
from config import state_dispenser, storage, token
from database.crud import UserOperations
from database.database import engine

chat_labeler = BotLabeler()
chat_labeler.vbml_ignore_case = True

user_crud = UserOperations(engine)


@chat_labeler.message(text=["начать", "/start", "старт", "ответь"])
async def add_sity_start(message: Message):
    if user_crud.get_user_by_vk_id(message.from_id) is None:
        await state_dispenser.set(message.peer_id, AddCity.start)
        vk = vk_api.VkApi(token=token)
        vk = vk.get_api()
        data = vk.users.get(user_ids=message.from_id, fields='first_name,last_name,sex,city')
        if 'city' in data[0] and 'title' in data[0]['city']:
            await message.answer(f"Привет, твой город {data[0]['city']['title']}?", keyboard=keyboard_yes_no)
            storage.set("city", data[0]['city']['title'])
            await state_dispenser.set(message.peer_id, AddCity.start_city)
        else:
            await message.answer(f"Привет, напиши свой город?")
            await state_dispenser.set(message.peer_id, AddCity.start_city)
    else:
        await message.answer(f"Выбери команду", keyboard=keyboard_main_menu)


@chat_labeler.message(state=AddCity.start_city)
async def start_city(message: Message):
    if message.text == "Да":
        print(storage["city"])
        user_crud.create(vk_id=message.from_id, city=storage["city"])
        await state_dispenser.set(message.peer_id, AddCity.finish)
        await message.answer(f"Город успешно зарегистрирован")
        await message.answer(f"Ты в главном меню:", keyboard=keyboard_main_menu)
    elif message.text == "Нет":
        await message.answer(f"Напиши свой город?")
        await state_dispenser.set(message.peer_id, AddCity.new_city)
    else:
        user_crud.create(vk_id=message.from_id, city=message.text)
        await state_dispenser.set(message.peer_id, AddCity.finish)
        await message.answer(f"Город успешно зарегистрирован")
        await message.answer(f"Ты в главном меню:", keyboard=keyboard_main_menu)


@chat_labeler.message(state=AddCity.new_city)
async def new_city(message: Message):
    user_crud.create(vk_id=message.from_id, city=message.text)
    await state_dispenser.set(message.peer_id, AddCity.finish)
    await message.answer(f"Город успешно зарегистрирован")
    await message.answer(f"Ты в главном меню:", keyboard=keyboard_main_menu)
