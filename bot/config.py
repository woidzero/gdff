from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Config:
    TOKEN = getenv("TOKEN")

    DB_FILE = getenv("DB_FILE")
    DB_HOST = getenv("DB_HOST")
    DB_NAME = getenv("DB_NAME")
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_PORT = getenv("DB_PORT")
