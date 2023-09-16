from sqlalchemy.orm import sessionmaker
from vkbottle.bot import Bot
from bot.handlers import chat_labeler, weather_labeler, traffic_labeler, currency_labeler, afisha_labeler, menu_labeler, \
    update_city_labeler
from config import labeler, api, state_dispenser
from database.database import engine
from database.models import Base

labeler.load(chat_labeler)
labeler.load(weather_labeler)
labeler.load(traffic_labeler)
labeler.load(currency_labeler)
labeler.load(afisha_labeler)
labeler.load(menu_labeler)
labeler.load(update_city_labeler)

bot = Bot(api=api, labeler=labeler, state_dispenser=state_dispenser)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()

if __name__ == "__main__":
    bot.run_forever()
