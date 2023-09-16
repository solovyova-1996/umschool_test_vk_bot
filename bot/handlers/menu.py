from vkbottle.bot import Message, BotLabeler
from bot.keyboards import keyboard_main_menu

menu_labeler = BotLabeler()
menu_labeler.vbml_ignore_case = True


@menu_labeler.message(text=["клавиатура", "меню", "/menu"])
async def menu(message: Message):
    await message.answer(f"Ты в главном меню:", keyboard=keyboard_main_menu)


@menu_labeler.message(text="/help")
async def help(message: Message):
    await message.answer(f"Комманды:\n"
                         f"/menu - для перехода в главное меню\n"
                         f"/city_update - для смены города")
