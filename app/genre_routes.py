from distutils.command import check
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.genre import Genre
from app.models.book import Book
from app import db

genre_bp = Blueprint("genres", __name__, url_prefix = "/genres")

@genre_bp.route("", methods = ["GET"])
def get_all_genres():
    genres = Genre.query.all()

    genre_response = [genre.to_json() for genre in genres]

    return jsonify(genre_response), 200

@genre_bp.route("", methods = ["POST"])
def make_new_genre():
    request_body = request.get_json()

    new_genre = Genre(name = request_body["name"])

    db.session.add(new_genre)
    db.session.commit()

    return jsonify({"name": new_genre.name}), 200

def check_genre_exists(genre_id):
    genre = Genre.query.get(genre_id)

    if not genre:
        abort(make_response(f"Genre {genre.id} not found"), 404)
    
    return genre


@genre_bp.route("/<genre_id>/books", methods = ["POST"])
def make_new_book(genre_id):
    genre = check_genre_exists(genre_id)
    request_body = request.get_json()

    # Make new instance of book
    new_book = Book(title = request_body["title"], 
                    description = request_body["description"],
                    author_id = request_body["author_id"],
                    genres = [genre])
    # Add book to DB
    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@genre_bp.route("/<genre_id>/books", methods = ["GET"])
def get_books(genre_id):
    genre = check_genre_exists(genre_id)

    books_response = []
    for book in genre.books:
        books_response.append(book.to_json())
    
    return jsonify(books_response), 200
