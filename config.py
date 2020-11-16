import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).parent

load_dotenv(str(basedir / ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + str(
        basedir / "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["your-email@example.com"]
    LANGUAGES = ["en", "fr", "de"]
    POSTS_PER_PAGE = os.environ.get("POSTS_PER_PAGE") or 25
