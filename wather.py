import logging
import requests
import datetime
from aiogram import Bot, Dispatcher, executor, types

weather_token = "6e8d79779a0c362f14c60a1c7f363e29"
API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="5158040057:AAEtt8ByoaJdYMy09MpupqpNAxiCAQnGj-0")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет!\nНапиши мне название города и я сообщу погоду там!\n")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric")
        data = r.json()
        city = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        await message.reply(f"***{datetime.datetime.now().strftime('%b %d %Y %H:%M')}***\n"
                            f"Погода в городе {city}\nТемпература {temperature} C°\n"
                            f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст.\n"
                            f"Ветер: {wind} м/с\n ")
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
