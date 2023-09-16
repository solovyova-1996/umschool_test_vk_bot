from vkbottle import Keyboard, KeyboardButtonColor, Text

keyboard_yes_no = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Да"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Нет"), color=KeyboardButtonColor.NEGATIVE)
).get_json()

keyboard_main_menu = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Погода"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Пробка"), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Афиша"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Валюта"), color=KeyboardButtonColor.SECONDARY)

).get_json()
keyboard_today_tomorrow = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Сегодня"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Завтра"), color=KeyboardButtonColor.NEGATIVE)

).get_json()
