from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    TOKEN = getenv("TOKEN")
    