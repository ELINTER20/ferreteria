import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SECRET_KEY:
        raise RuntimeError("Falta la variable de entorno SECRET_KEY.")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("Falta la variable de entorno DATABASE_URL.")
