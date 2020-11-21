import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).parent

load_dotenv(str(basedir / ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    if DATABASE_HOST is None:
        raise Exception("DATABASE_HOST not defined")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    if DATABASE_USER is None:
        raise Exception("DATABASE_USER not defined")
    DATABASE_DB = os.environ.get("DATABASE_DB")
    if DATABASE_DB is None:
        raise Exception("DATABASE_DB not defined")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    if DATABASE_PASSWORD is None:
        raise Exception("DATABASE_PASSWORD not defined")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = [os.environ.get("ADMINS")]
    LANGUAGES = ["en", "fr", "de"]
    POSTS_PER_PAGE = os.environ.get("POSTS_PER_PAGE") or 25

    ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
    if ELASTICSEARCH_HOST is None:
        ELASTICSEARCH_URL = None
    else:
        ELASTICSEARCH_URL = f"http://{ELASTICSEARCH_HOST}:9200"

    REDIS_URL = os.environ.get('REDIS_URL')
