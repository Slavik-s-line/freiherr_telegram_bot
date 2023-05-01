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
    buttons_row2 = ["Втрати росії у війні🚷", "Веб-сайт\U0001F310"]
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


@dp.message_handler(lambda message: message.text == "Втрати росії у війні🚷")
async def name_city(message: types.Message):
    # main stats
    url = 'https://russianwarship.rip/api/v2/statistics/latest'
    response = requests.get(url).json()
    date = response["data"]["date"]
    day = response["data"]["day"]
    personnel_units = response["data"]["stats"]["personnel_units"]
    tanks = response["data"]["stats"]["tanks"]
    armoured_fighting_vehicles = response["data"]["stats"]["armoured_fighting_vehicles"]
    artillery_systems = response["data"]["stats"]["artillery_systems"]
    mlrs = response["data"]["stats"]["mlrs"]
    aa_warfare_systems = response["data"]["stats"]["aa_warfare_systems"]
    planes = response["data"]["stats"]["planes"]
    helicopters = response["data"]["stats"]["helicopters"]
    vehicles_fuel_tanks = response["data"]["stats"]["vehicles_fuel_tanks"]
    warships_cutters = response["data"]["stats"]["warships_cutters"]
    cruise_missiles = response["data"]["stats"]["cruise_missiles"]
    uav_systems = response["data"]["stats"]["uav_systems"]
    special_military_equip = response["data"]["stats"]["special_military_equip"]

    # increase by last day
    day_personnel_units = response["data"]["increase"]["personnel_units"]
    day_tanks = response["data"]["increase"]["tanks"]
    day_armoured_fighting_vehicles = response["data"]["increase"]["armoured_fighting_vehicles"]
    day_artillery_systems = response["data"]["increase"]["artillery_systems"]
    day_mlrs = response["data"]["increase"]["mlrs"]
    day_aa_warfare_systems = response["data"]["increase"]["aa_warfare_systems"]
    day_planes = response["data"]["increase"]["planes"]
    day_helicopters = response["data"]["increase"]["helicopters"]
    day_vehicles_fuel_tanks = response["data"]["increase"]["vehicles_fuel_tanks"]
    day_warships_cutters = response["data"]["increase"]["warships_cutters"]
    day_cruise_missiles = response["data"]["increase"]["cruise_missiles"]
    day_uav_systems = response["data"]["increase"]["uav_systems"]
    day_special_military_equip = response["data"]["increase"]["special_military_equip"]

    await message.reply(f"*День війни №* {day}\n\n"
                        f"*Знищено:*\n\n"
                        f"🪖*Особового складу:* {personnel_units}(+{day_personnel_units})\n"
                        f"🚜*Танків:* {tanks}(+{day_tanks})\n"
                        f"🛡️*Бойових броньованих машин:* {armoured_fighting_vehicles}(+{day_armoured_fighting_vehicles})\n"
                        f"🎯*Артилерійських систем:* {artillery_systems}(+{day_artillery_systems})\n"
                        f"🏹*РСЗВ:* {mlrs}(+{day_mlrs})\n"
                        f"📡*Засобів ППО:* {aa_warfare_systems}(+{day_aa_warfare_systems})\n"
                        f"🛩️*Літаків:* {planes}(+{day_planes})\n"
                        f"🚁*Гелікоптерів:* {helicopters}(+{day_helicopters})\n"
                        f"🚚*Автомобільної техніки та цистерн з ПММ:* {vehicles_fuel_tanks}(+{day_vehicles_fuel_tanks})\n"
                        f"🚤*Кораблів/катерів:* {warships_cutters}(+{day_warships_cutters})\n"
                        f"🚀*Крилатих ракет:* {cruise_missiles}(+{day_cruise_missiles})\n"
                        f"🛸*БПЛА:* {uav_systems}(+{day_uav_systems})\n"
                        f"🦽*Спеціальної техніки:* {special_military_equip}(+{day_special_military_equip})", parse_mode= 'Markdown')


@dp.message_handler(lambda message: message.text == "Веб-сайт\U0001F310")
async def name_city(message: types.Message):
    await message.reply("164.92.165.232")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)