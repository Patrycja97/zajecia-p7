import os.path
import requests
import json
from datetime import datetime, timedelta

if os.path.exists("cache.json"):
    with open("cache.json", "r") as f:
        cache = json.load(f)
else:
    cache = {}

def get_weather_info(date, latitude=52.23, longitude=21.01):
    if date in cache:
        print("Pobieram dane z cache")
        return cache[date]

    print("Pobieram dane z API")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            rain_sum = data["daily"]["rain_sum"][0]
        except (KeyError, IndexError):
            rain_sum = None

        if rain_sum is None or rain_sum < 0:
            wynik = "Nie wiem"
        elif rain_sum == 0.0:
            wynik = "Nie będzie padać"
        else:
            wynik = "Będzie padać"

        cache[date] = wynik

        with open("cache.json", "w") as f:
            json.dump(cache, f, indent=4, ensure_ascii=False)

        return wynik
    else:
        print("Błąd połączenia")
        return "Nie wiem"


while True:
    date_input = input("Podaj datę (YYYY-mm-dd) lub naciśnij Enter dla jutra (wpisz 'koniec' by przerwać): ")

    if date_input.lower() == "koniec":
        break

    if date_input == "":
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print("Niepoprawny format daty. Spróbuj ponownie.")
            continue

    wynik = get_weather_info(date)
    print(f"Pogoda na dzień {date}: {wynik}")