from datetime import datetime, timedelta, timezone
import sys
from flask import Flask, render_template, request
import requests


app = Flask(__name__)


def get_time(timestamp: int, offset: int) -> str:
    delta = datetime.fromtimestamp(timestamp, timezone(timedelta(seconds=offset)))
    hour = delta.hour
    if 12 < hour < 18:
        return "day"
    if 0 < hour < 5:
        return "night"
    return "evening-morning"


def get_weather_data(city: str, api_key: str) -> dict:
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(api_url)
    if response.status_code == 200:
        response_json = response.json()
        return {
            "state": response_json["weather"][0]["main"],
            "temp": response_json["main"]["temp"],
            "time": get_time(response_json["dt"], response_json["timezone"]),
        }
    return {}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city_name"].capitalize()
        if city:
            cities_data[city] = get_weather_data(city, key)
    return render_template("index.html", data=cities_data)


# don't change the following way to run flask:
if __name__ == "__main__":
    with open("api_key.txt", "r") as key_file:
        key = key_file.read().strip()
    cities_data = {
        city: get_weather_data(city, key)
        for city in ("Omsk", "Volgograd", "Saint Petersburg")
    }
    # app.debug = True
    app.env = "development"
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
