from flask import Blueprint, jsonify

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

book1 = Book(1, "Harry Potter", "A story about a magical boy.")
book2 = Book(2, "Another Book", "Another book description")
book3 = Book(3, "A Third Book", "Third Book description")

books = [book1, book2, book3]

books_bp = Blueprint("books", __name__, url_prefix = "/books")

@books_bp.route("", methods = ["GET"])
def get_all_books():
    book_response = [{"id": book.id, "title": book.title, "description": book.description} for book in books]
    return jsonify(book_response)