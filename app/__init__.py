from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
# Loads values in .env file
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    # Connects to either development or testing DB
    if not test_config:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    
    else:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
        
    # Connects db and migrate to app
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import books_bp
    app.register_blueprint(books_bp)

    from .author_routes import authors_bp
    app.register_blueprint(authors_bp)

    # Makes models visible to our app
    from app.models.book import Book
    from app.models.author import Author

    return app