import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book


@pytest.fixture
def app():
    # Create app object (as defined in app/__init__.py)
    # Dictionary represent test_config object
    app = create_app({"TESTING": True})

    # Function below will be exectued when a request is completed
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        # Creates new DB session to ensure changes were persisted in DB
        db.session.remove()

    # At the stare of each test, recreate all tables needed for models
    with app.app_context():
        db.create_all()
        yield app
    # Get rid of all tables, deleting any data that was generated during test
    with app.app_context():
        db.drop_all()

# Test client which will make requests to server for us
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    ocean_book = Book(title="Ocean Book",
                    description = "watr 4evr")
    mountain_book = Book(title = "Mountain Book", 
                        description = "i luv 2 climb rocks")
    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()