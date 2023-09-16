from vkbottle.bot import Message, BotLabeler

from bot.keyboards import keyboard_main_menu
from bot.support import get_currency

currency_labeler = BotLabeler()
currency_labeler.vbml_ignore_case = True


@currency_labeler.message(text="Валюта")
async def get_currency_handler(message: Message):
    message_answer = get_currency()
    await message.answer(message_answer, keyboard=keyboard_main_menu)
