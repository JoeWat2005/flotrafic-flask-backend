from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("website_manager.app.config.Config")

    db.init_app(app)

    from website_manager.app.routes import api
    from website_manager.app.admin import admin

    app.register_blueprint(api)
    app.register_blueprint(admin)

    # Import models so SQLAlchemy knows about them
    from website_manager.app.models import Client, Enquiry

    return app
