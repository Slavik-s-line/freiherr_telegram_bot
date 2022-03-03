import logging
import requests
import datetime
from aiogram import Bot, Dispatcher, executor, types
from tg_info import info
from bs4 import BeautifulSoup

weather_token = "6e8d79779a0c362f14c60a1c7f363e29"
API_TOKEN = "5158040057:AAEtt8ByoaJdYMy09MpupqpNAxiCAQnGj-0"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привіт!\n")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_row1 = ["Погода\U0001F30D", "Курс UAH\U0001F3E6"]
    buttons_row2 = ["Covid-19\U0001f9a0", "Офіційні джерела\U00002139"]
    keyboard.add(*buttons_row1)
    keyboard.add(*buttons_row2)
    await message.answer("Обери одну з функцій внизу: ", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Погода\U0001F30D")
async def name_city(message: types.Message):
    await message.reply("Введіть назву міста: ")

    @dp.message_handler(lambda message: message.text != "Курс UAH\U0001F3E6"
                                        and message.text != "Covid-19\U0001f9a0"
                                        and message.text != "Офіційні джерела\U00002139")
    async def without_puree(message: types.Message):
        try:
            r1 = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric")
            data = r1.json()
            city = data["name"]
            temperature = round(data["main"]["temp"])
            humidity = round(data["main"]["humidity"])
            wind = round(data["wind"]["speed"])
            await message.reply(f"***{datetime.datetime.now().strftime('%b %d %Y %H:%M')}***\n"
                                f"Погода в місті: {city}\n\U0001F321Температура: {temperature} C°\n"
                                f"\U0001F4A7Вологість повітря: {humidity} %\n"
                                f"\U0001F32AВітер: {wind} м/с\n ")
        except:
            await message.reply("\U0001F3D9 Провірте назву міста \U0001F3D9")


@dp.message_handler(lambda message: message.text == "Курс UAH\U0001F3E6")
async def name_city(message: types.Message):
    url = 'https://minfin.com.ua/ua/currency/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    nby = soup.find_all('span', class_='mfcur-nbu-full-wrap')
    buy = soup.find_all('td', class_='mfm-text-nowrap')
    sell = soup.find_all('td', class_='mfm-text-nowrap')
    await message.reply(f"\U0001F4B5 USD:\n НБУ: {nby[0].text[1:8]} Купівля: {buy[1].text[1:8]} Продаж:{sell[1].text[14:20]}\n\n"
                        f"\U0001F4B6 EUR:\n НБУ: {nby[1].text[1:8]} Купівля: {buy[3].text[1:8]} Продаж:{sell[3].text[14:20]}\n\n"
                        f"\U000020BD RUB:\n НБУ: {nby[2].text[1:8]} Купівля: {buy[5].text[1:7]} Продаж:{sell[5].text[13:19]}")


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


@dp.message_handler(lambda message: message.text == "Офіційні джерела\U00002139")
async def name_city(message: types.Message):
    await message.reply(info)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
