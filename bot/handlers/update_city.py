from vkbottle.bot import Message, BotLabeler
from bot.keyboards import keyboard_main_menu
from bot.states import UpdateCity

from config import state_dispenser
from database.crud import UserOperations
from database.database import engine

update_city_labeler = BotLabeler()
update_city_labeler.vbml_ignore_case = True

user_crud = UserOperations(engine)


@update_city_labeler.message(text=["/city_update", "изменить город", "сменить город"])
async def update_city_start(message: Message):
    await message.answer(f"Напишите свой город")
    await state_dispenser.set(message.peer_id, UpdateCity.start)


@update_city_labeler.message(state=UpdateCity.start)
async def get_city(message: Message):
    user_crud.update_city(message.from_id, message.text)
    await message.answer(f"Ваш город изменен на {message.text}", keyboard=keyboard_main_menu)
    await state_dispenser.set(message.peer_id, UpdateCity.finish)
