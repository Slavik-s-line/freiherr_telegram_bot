import logging
import requests
import datetime
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import os

weather_token = os.environ['OPENWEATHER_TOKEN']
API_TOKEN = os.environ['TG_API_TOKEN_FREIHERR']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_date(timezone):
    tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
    return datetime.datetime.now(tz = tz).strftime('%b %d %Y %H:%M')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привіт!\n")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_row1 = ["Погода\U0001F30D", "Курс UAH\U0001F3E6"]
    buttons_row2 = ["Covid-19\U0001f9a0", "Веб-сайт\U0001F310"]
    keyboard.add(*buttons_row1)
    keyboard.add(*buttons_row2)
    await message.answer("Обери одну з функцій внизу: ", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Погода\U0001F30D")
async def name_city(message: types.Message):
    await message.reply("Введіть назву міста: ")

    @dp.message_handler(lambda message: message.text not in ["Погода\U0001F30D", "Курс UAH\U0001F3E6", "Covid-19\U0001f9a0", "Веб-сайт\U0001F310"])
    async def without_puree(message: types.Message):
        try:
            r1 = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric")
            data = r1.json()
            city = data["name"]
            temperature = round(data["main"]["temp"])
            humidity = round(data["main"]["humidity"])
            wind = round(data["wind"]["speed"])
            pressure = round(data["main"]["pressure"])
            await message.answer(f"Погода в місті: {city}\n"
                                 f"\U0001F321Температура: {temperature} C°\n"
                                 f"\U0001F4A7Вологість повітря: {humidity} %\n"
                                 f"\U0001F32AВітер: {wind} м/с\n"
                                 f"🌀Тиск: {pressure}  Па\n"
                                 f"🕰️Місцевий час: {get_date(data['timezone'])}")
        except:
            await message.reply("\U0001F3D9 Провірте назву міста \U0001F3D9")


@dp.message_handler(lambda message: message.text == "Курс UAH\U0001F3E6")
async def name_city(message: types.Message):
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5'
    response = requests.get(url)
    data = response.json()
    await message.reply(f"\U0001F4B5 USD:\nКупівля: {round(float(data[1]['buy']), 2)}\n"
                        f"Продаж:{round(float(data[1]['sale']), 2)}\n\n"
                        f"\U0001F4B6 EUR:\nКупівля: {round(float(data[0]['buy']), 2)}\n"
                        f"Продаж:{round(float(data[0]['sale']), 2)}\n\n")


@dp.message_handler(lambda message: message.text == "Covid-19\U0001f9a0")
async def name_city(message: types.Message):
    url = 'https://index.minfin.com.ua/ua/reference/coronavirus/geography/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    info = soup.find_all('td', class_='bg-total')
    await message.reply(f"Статистака Covid-19 у світі на сьогодні: "
                        f"{datetime.datetime.now().strftime('%b %d %Y %H:%M')}\n\n"
                        f"\U0001f637Захворіли: {info[2].text}\n"
                        f"\U0001f600Одужали: {info[6].text}\n"
                        f"\U0001f494Померли: {info[4].text}\n")


@dp.message_handler(lambda message: message.text == "Веб-сайт\U0001F310")
async def name_city(message: types.Message):
    await message.reply("164.92.165.232")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)