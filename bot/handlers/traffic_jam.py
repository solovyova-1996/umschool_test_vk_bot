from vkbottle.bot import Message, BotLabeler

from bot.keyboards import keyboard_main_menu
from bot.support import get_traffic_jam
from database.crud import UserOperations
from database.database import engine

traffic_labeler = BotLabeler()
traffic_labeler.vbml_ignore_case = True

user_crud = UserOperations(engine)


@traffic_labeler.message(text="Пробка")
async def get_traffic(message: Message):
    city_user = user_crud.get_city_user_by_vk_id(message.from_id)
    traffic_ball = get_traffic_jam(city_user)
    await message.answer(f"Пробки({city_user}):{traffic_ball} баллов", keyboard=keyboard_main_menu)
