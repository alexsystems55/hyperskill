from flask import Flask
from flask_restful import Api, inputs, reqparse, Resource
import sys

app = Flask(__name__)
api = Api(app)

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


class WebCalendar(Resource):
    def get(self):
        return {"data": "There are no events for today!"}

    def post(self):
        args = parser.parse_args()
        return {
            "message": "The event has been added!",
            "event": args["event"],
            "date": str(args["date"].date())
        }


api.add_resource(WebCalendar, "/event", "/event/today")

# do not change the way you run the program
if __name__ == "__main__":
    app.env = "development"
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(":")
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
