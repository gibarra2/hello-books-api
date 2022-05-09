from flask import Blueprint, jsonify, request, make_response
from app.models.author import Author
from app import db

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@authors_bp("", methods = ["GET"])
def get_all_authors():
    authors = Author.query.all()
    authors_response = [author.to_json() for author in authors]

    return jsonify(authors_response), 200

@authors_bp("", methods = ["POST"])
def create_new_author():
    request_body = request.get_json()

    new_author = Author.make_new_author(request_body)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)