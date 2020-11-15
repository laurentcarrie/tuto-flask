from flask_mail import Message
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from logging.handlers import RotatingFileHandler
from flask_moment import Moment
from flask import request
from flask_babel import Babel, lazy_gettext as _l


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
login.login_message = _l("Please log in to access this page")
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)


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


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])
    # return 'fr'


from app import routes, errors  # noqa: E402
