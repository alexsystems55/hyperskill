from os import environ, urandom
import sys
from datetime import datetime, timedelta, timezone
from typing import Callable

import requests
from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


class MySQLAlchemy(SQLAlchemy):
    """
    Wrapper for PyCharm to detect imports from SQLAlchemy correctly
    """

    Column: Callable
    Integer: Callable
    String: Callable


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = urandom(16)  # session cookie key
db = MySQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


db.create_all()


def get_part_of_day(timestamp: int, offset: int) -> str:
    """

    :param timestamp: Time (UTC)
    :param offset: Timezone offset in seconds
    :return: Part of day: "day", "night" or "evening-morning"
    """
    time = datetime.fromtimestamp(timestamp, timezone(timedelta(seconds=offset)))
    hour = time.hour
    if 12 < hour < 18:
        return "day"
    if 0 < hour < 5:
        return "night"
    return "evening-morning"


def get_weather_data(city: str) -> dict:
    if "OPEN_WEATHER_KEY" not in environ:
        print("API key is not defined!")
    api_key = environ.get("OPEN_WEATHER_KEY")
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(api_url)
    if response.status_code == 200:  # HTTP response status code
        response_json = response.json()
        if response_json["cod"] == 200:  # API response status code
            return {
                "state": response_json["weather"][0]["main"],
                "temp": response_json["main"]["temp"],
                "time": get_part_of_day(response_json["dt"], response_json["timezone"]),
            }
    return {}


@app.route("/", methods=["GET"])
def index():
    weather_data = {}
    for city in City.query.all():
        weather_data[city.name] = get_weather_data(city.name)
        weather_data[city.name]["city_id"] = city.id
    return render_template("index.html", data=weather_data)


@app.route("/add", methods=["POST"])
def add():
    city_name = request.form["city_name"]
    if get_weather_data(city_name):
        city = City.query.filter_by(name=city_name).first()
        if not city:
            city = City(name=city_name)
            db.session.add(city)
            db.session.commit()
        else:
            print(f"{city_name} already exists.")
            flash("The city has already been added to the list!")
    else:
        print(f"The city '{city_name}' doesn't exist!")
        flash("The city doesn't exist!")
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    city_id = request.form["id"]
    city = City.query.filter_by(id=city_id).first()
    if city:
        db.session.delete(city)
        db.session.commit()
    else:
        print(f"The city with id {city_id} not found.")
        flash("The city doesn't exist!")
    return redirect("/")


# don't change the following way to run flask:
if __name__ == "__main__":
    app.env = "development"
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
