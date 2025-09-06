import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV")
VERSION = os.getenv("VERSION")

SQLITE_URL = os.getenv("SQLITE_URL")

