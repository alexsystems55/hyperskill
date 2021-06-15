from os import environ
import sys
from datetime import datetime, timedelta, timezone
from typing import Callable

import requests
from flask import Flask, redirect, render_template, request
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
db = MySQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


def get_time(timestamp: int, offset: int) -> str:
    delta = datetime.fromtimestamp(timestamp, timezone(timedelta(seconds=offset)))
    hour = delta.hour
    if 12 < hour < 18:
        return "day"
    if 0 < hour < 5:
        return "night"
    return "evening-morning"


def get_weather_data(city: str) -> dict:
    api_key = environ.get("OPEN_WEATHER_KEY")  # @todo: check for the var existence
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


@app.route("/", methods=["GET"])
def index():
    weather_data = {}
    for city in City.query.all():
        weather_data[city.name] = get_weather_data(city.name)
    return render_template("index.html", data=weather_data)


@app.route("/add", methods=["POST"])
def add():
    city_name = request.form["city_name"].capitalize()
    if city_name:
        city = City(name=city_name)
        db.session.add(city)
        db.session.commit()
    return redirect("/")


@app.route("/delete/<city_id>", methods=["POST"])
def delete():
    return redirect("/")


# don't change the following way to run flask:
if __name__ == "__main__":
    app.env = "development"
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
