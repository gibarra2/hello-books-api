# Import necessary modules from our Book model
from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, abort, request

# Blueprint instance that groups routes that begin with /books
books_bp = Blueprint("books", __name__, url_prefix = "/books")

# Decorator that uses blueprint to define endpoint and accepted HTTP method
# Function executes whenever matching HTTP request is received
@books_bp.route("", methods = ["POST"])
def make_new_book():
    # Use request object to get json body of HTTP request and hold in variable
    request_body = request.get_json() 
    # Create instance of Book using data from the request body
    new_book = Book(title = request_body["title"], 
                    description = request_body["description"])
    
    # This is how DB collects changes that need to be made. Add new_book to DB
    db.session.add(new_book)
    # Indicate we want the DB to save and commit collected changes
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("", methods = ["GET"])
def get_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title = title_query)
    else:
        books = Book.query.all()
    
    book_response = [book.to_json() for book in books]
    return jsonify(book_response), 200

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"Book {book_id} is invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message": f"Book {book_id} not found"}, 404))

    return book

@books_bp.route("/<book_id>", methods = ["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)

    return jsonify(book.to_json()), 200

@books_bp.route("/<book_id>", methods = ["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    # Get info from request body
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(f"Book {book_id} successfully updated", 200)

@books_bp.route("/<book_id>", methods = ["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book #{book_id} was successfully deleted", 200)


