import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///local.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
