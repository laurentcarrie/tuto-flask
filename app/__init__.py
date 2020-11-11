from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# pylint:disable=E0401
from flask_migrate import Migrate
# pylint:enable=E0401

from config import Config
from app import routes

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
