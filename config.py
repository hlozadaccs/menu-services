# app/config.py
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:password@127.0.0.1:5432/menu-services",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
