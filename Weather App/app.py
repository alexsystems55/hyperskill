from flask import Flask, render_template, request
import sys
from random import choice, randint

app = Flask(__name__)

cities_data = {
    "BOSTON": {"time": "night", "temp": 9, "state": "Chilly"},
    "NEW YORK": {"time": "day", "temp": 32, "state": "Sunny"},
    "EDMONTON": {"time": "evening-morning", "temp": -15, "state": "Cold"},
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city_name"].upper()
        cities_data[city] = {
            "time": choice(["day", "night", "evening-morning"]),
            "temp": randint(-30, 30),
            "state": "Ok!",
        }
    return render_template("index.html", data=cities_data)


# don't change the following way to run flask:
if __name__ == "__main__":
    # app.debug = True
    app.env = "development"
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
