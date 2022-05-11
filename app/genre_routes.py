from flask import Blueprint, jsonify, request
from app.models.genre import Genre
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
