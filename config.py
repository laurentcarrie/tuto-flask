import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).parent

load_dotenv(str(basedir / ".env"))


def get_env(name):
    val = os.environ.get(name)
    if val is None:
        print(f"{name} not defined")
        exit(1)
    return val


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    DATABASE_HOST = get_env("DATABASE_HOST")
    DATABASE_HOST = get_env("DATABASE_HOST")
    DATABASE_USER = get_env("DATABASE_USER")
    DATABASE_DB = get_env("DATABASE_DB")
    DATABASE_PASSWORD = get_env("DATABASE_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = get_env("MAIL_SERVER")
    MAIL_PORT = int(get_env("MAIL_PORT") or 25)
    MAIL_USE_TLS = get_env("MAIL_USE_TLS") is not None
    MAIL_USERNAME = get_env("MAIL_USERNAME")
    MAIL_PASSWORD = get_env("MAIL_PASSWORD")
    ADMINS = [get_env("ADMINS")]
    LANGUAGES = ["en", "fr", "de"]
    POSTS_PER_PAGE = int(get_env("POSTS_PER_PAGE"))

    ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
    if ELASTICSEARCH_HOST is None:
        ELASTICSEARCH_URL = None
    else:
        ELASTICSEARCH_URL = f"http://{ELASTICSEARCH_HOST}:9200"

    REDIS_URL = os.environ.get('REDIS_URL')
    if REDIS_URL is None:
        raise Exception("REDIS_URL not defined")
