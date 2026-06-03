from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///animals.db"
    app.config["UPLOAD_FOLDER"] = "app/static/images"
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
