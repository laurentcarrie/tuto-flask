from flask_mail import Message
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from logging.handlers import RotatingFileHandler

import logging
import os
from logging.handlers import SMTPHandler

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
mail = Mail(app)


# if not app.debug:
if True:

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/microblog.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog startup")

logger = app.logger


def send_msg(text):
    msg = Message(
        "hello flask",
        sender="laurent.carrie@gmail.com",
        recipients=["laurent.carrie.dummy@gmail.com"],
    )
    msg.body = text
    msg.html = f"<h2>{text}</h2>"
    mail.send(msg)


app.sss = send_msg

from app import routes, errors  # noqa: E402
