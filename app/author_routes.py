from flask import Blueprint, jsonify, request, make_response, abort
from app.models.author import Author
from app.models.book import Book
from app import db

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@authors_bp.route("", methods = ["GET"])
def get_all_authors():
    authors = Author.query.all()
    authors_response = [author.to_json() for author in authors]

    return jsonify(authors_response), 200

@authors_bp.route("", methods = ["POST"])
def create_new_author():
    request_body = request.get_json()

    new_author = Author.make_new_author(request_body)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

def validate_author(author_id):
    try:
        author_id = int(author_id)
    except:
        abort(make_response({"message":f"author {author_id} invalid"}, 400))

    author = Author.query.get(author_id)

    if not author:
        abort(make_response({"message":f"author {author_id} not found"}, 404))

    return author

@authors_bp.route("/<author_id>/books", methods = ["POST"])
def create_book(author_id):
    author = validate_author(author_id)
    request_body = request.get_json()

    new_book = Book(title = request_body["title"], 
                    description = request_body["description"], 
                    author = author)
    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods = ["GET"])
def get_book(author_id):
    author = validate_author(author_id)
    books = author.books

    books_response = [book.to_json() for book in books]

    return jsonify(books_response), 200


