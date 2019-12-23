import os
import config
from logging.config import dictConfig
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# Logs configuration
dictConfig({
    "version": 1,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
        },
        "file": {
            "format": ("[%(asctime)s] [%(levelname)s] %(pathname)s - "
                       "line %(lineno)d: \n%(message)s\n")
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "console"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.getenv("LOGS_FILE", default="queue.log"),
            "formatter": "file"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
})


app = Flask(__name__)

app.config.from_object(config.Config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from counter import Counter
from number import Number
from key_manager import generate_random_key

try:
    # Setup counter in database
    COUNTER = Counter.query.one_or_none()
    if COUNTER is None:
        COUNTER = Counter()
        db.session.add(COUNTER)
        db.session.commit()
except Exception as err:
    app.logger.error(err)


@app.route("/")
def index():
    return "https://www.github.com/daleal/queue"


@app.route("/number", methods=["GET"])
def get_next():
    """Generates a new number with a key and returns the information."""
    try:
        data = request.get_json(force=True)

        if "key" not in data:
            app.logger.info(f"No key present in request body")
            return jsonify({
                "success": False,
                "message": "No key present in request body"
            }), 401

        key = data["key"]

        if os.getenv("KEY") != key:
            app.logger.info(f"Invalid key {key} for retrieving queue number")
            return jsonify({
                "success": False,
                "message": "Invalid key"
            }), 401

        app.logger.info(f"Generating number...")

        number_key = generate_random_key()
        number = Number(COUNTER.get(), number_key)

        # Increment counter
        COUNTER.increment()

        # Save Number in the database
        db.session.add(number)
        db.session.commit()

        app.logger.info(
            f"Number {number.position} generated with key {number_key}"
        )

        return jsonify({
            "success": True,
            "number": number.position,
            "key": number_key
        }), 200

    except Exception as err:
        app.logger.error(err)
        return jsonify({"success": False}), 500


@app.route("/number/<int:position>", methods=["POST"])
def check_number(position):
    """Checks if number and plain key match."""
    try:
        data = request.get_json(force=True)

        if "key" not in data:
            app.logger.info(f"No key present in request body")
            return jsonify({
                "success": False,
                "message": "No key present in request body"
            }), 401

        key = data["key"]

        if os.getenv("KEY") != key:
            app.logger.info(f"Invalid key {key} for retrieving queue number")
            return jsonify({
                "success": False,
                "message": "Invalid key"
            }), 401

        if set(["key", "plain_key"]) != set(data.keys()):
            app.logger.info(f"Invalid request body keys {data.keys()}")
            return jsonify({
                "success": False,
                "message": "Invalid request body"
            }), 400

        if position >= COUNTER.get():
            # Number has not been emmited yet
            app.logger.info(
                f"Number {position} tried to be accessed. Last number created "
                f"was {COUNTER.get() - 1}"
            )
            return jsonify({
                "success": False,
                "message": "Invalid number"
            }), 404

        plain_key = data["plain_key"]
        number = Number.query.filter_by(position=position).first()

        if not number.check_plain_key(plain_key):
            app.logger.info(
                f"Number {position} tried to be accessed with incorrect key "
                f"{plain_key}"
            )
            return jsonify({
                "success": False,
                "message": "Invalid number key"
            }), 401

        return jsonify({"success": True}), 200

    except Exception as err:
        app.logger.error(err)
        return jsonify({"success": False}), 500
