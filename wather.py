import requests
from pprint import pprint

wather_token = "6e8d79779a0c362f14c60a1c7f363e29"


def get_wather(city, wather_token):
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={wather_token}&units=metric")
        data = r.json()
        pprint(data)
    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите название города: ")
    get_wather(city, wather_token)


if __name__ == '__main__':
    main()