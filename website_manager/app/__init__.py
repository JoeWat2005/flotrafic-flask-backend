from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("website_manager.app.config.Config")

    # Initialise DB first
    db.init_app(app)

    # Register blueprints
    from website_manager.app.routes import api
    from website_manager.app.admin import admin

    app.register_blueprint(api)
    app.register_blueprint(admin)

    # IMPORTANT: import models ONLY after db is ready
    from website_manager.app.models import Client

    with app.app_context():
        # Create tables
        db.create_all()

        # DEV SEED: create a default client if none exist
        if not Client.query.first():
            test_client = Client(
                name="Test Client",
                email="test@example.com",
                site_id="plumber123",
            )
            db.session.add(test_client)
            db.session.commit()

            print("✅ Seeded default test client: plumber123")

    return app
