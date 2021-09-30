from flask import Flask
from flask_restful import Api, inputs, reqparse, Resource
from flask_sqlalchemy import SQLAlchemy
import sys
from typing import Callable
from datetime import date


class MySQLAlchemy(SQLAlchemy):
    """
    Wrapper for PyCharm to detect imports from SQLAlchemy correctly
    """

    Column: Callable
    Integer: Callable
    String: Callable
    Date: Callable


# Initialization and configuration
app = Flask(__name__)
app.env = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_calendar.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db = MySQLAlchemy(app)

# Request parser
parser = reqparse.RequestParser()
parser.add_argument(
    "date",
    type=inputs.date,
    required=True,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
)
parser.add_argument(
    "event", type=str, required=True, help="The event name is required!"
)


# DB model class
class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()


# REST API class
class WebCalendar(Resource):
    def get(self, event_id: str = ""):
        if event_id == "today":
            today = date.today()
            events = Event.query.filter_by(date=today)
        elif event_id == "":
            events = Event.query.all()
        else:
            try:
                event_id_int = int(event_id)
            except ValueError:
                return "event_id should be integer"
            events = Event.query.filter_by(id=event_id_int)
        return [
            {"event": event.event, "date": str(event.date), "id": event.id}
            for event in events
        ]

    def post(self):
        args = parser.parse_args()
        event = Event(date=args["date"], event=args["event"])
        db.session.add(event)
        db.session.commit()
        return {
            "message": "The event has been added!",
            "event": args["event"],
            "date": str(args["date"].date()),
        }


# Routing
api.add_resource(WebCalendar, "/event", "/event/<event_id>")

# do not change the way you run the program
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
