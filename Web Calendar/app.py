from flask import Flask, abort
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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///event.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db = MySQLAlchemy(app)


# DB model class
class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"{self.event} - {self.date}"


db.create_all()


# REST API class
class WebCalendar(Resource):
    def get(self, event_id: str = ""):
        if event_id == "today":
            today = date.today()
            events = Event.query.filter_by(date=today)
            if not events:
                return {"data": "There are no events for today!"}
        elif event_id == "":
            app.logger.warning("Empty event_id!")
            # Request parser
            parser = reqparse.RequestParser()
            parser.add_argument(
                "start_time",
                type=inputs.date,
                location="args",
                required=False,
                help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
            )
            parser.add_argument(
                "end_time",
                type=inputs.date,
                location="args",
                required=False,
                help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
            )
            args = parser.parse_args()
            start_time = args["start_time"]
            end_time = args["end_time"]
            if start_time is None and end_time is None:
                app.logger.warning("All events!")
                events = Event.query.all()
            else:
                app.logger.warning("Events between %s and %s!" % (start_time, end_time))
                events = Event.query.filter(
                    Event.date > start_time, Event.date < end_time
                )
        else:
            app.logger.warning("Not empty and not today!")
            try:
                event_id_int = int(event_id)
            except ValueError:
                app.logger.warning("Value error!")
                abort(404, "The event doesn't exist!")
                return {"message": "The event doesn't exist!"}
            event = Event.query.get(event_id_int)
            if not event:
                app.logger.warning("No events")
                abort(404, "The event doesn't exist!")
                return {"message": "The event doesn't exist!"}
            else:
                return {"event": event.event, "date": str(event.date), "id": event.id}
        for event in events:
            app.logger.warning("Event filtered: %s" % event)
        return [
            {"event": event.event, "date": str(event.date), "id": event.id}
            for event in events
        ]

    def post(self):
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
        args = parser.parse_args()
        event = Event(date=args["date"], event=args["event"])
        db.session.add(event)
        db.session.commit()
        return {
            "message": "The event has been added!",
            "event": args["event"],
            "date": str(args["date"].date()),
        }

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if event is None:
            app.logger.warning("DELETE 404")
            abort(404, "The event doesn't exist!")
            return {"message": "The event doesn't exist!"}
        else:
            app.logger.warning("DELETE 200")
            db.session.delete(event)
            db.session.commit()
            return {"message": "The event has been deleted!"}


# Routing
api.add_resource(WebCalendar, "/event", "/event/<event_id>")

# do not change the way you run the program
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
