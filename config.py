import os
from dotenv import load_dotenv
from vkbottle import BuiltinStateDispenser, API, CtxStorage
from vkbottle.bot import BotLabeler

load_dotenv()
weather_token = os.getenv("WEATER_API")
token = os.getenv("VK_API_TOKEN")
currency_api = os.getenv("CURRENCY_API")
storage = CtxStorage()
labeler = BotLabeler()

state_dispenser = BuiltinStateDispenser()
api = API(token=token)
