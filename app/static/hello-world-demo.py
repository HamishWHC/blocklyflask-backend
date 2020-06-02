from flask import Flask, Blueprint

app = Flask(__name__)


default = Blueprint("default", "default", "/")


@default.route("/", methods=["GET"])
@default.route("/hello-world/", methods=["GET"])
def hello_world():
    return "Hello world!", 200


if __name__ == "__main__":
    app.run(debug=True)
