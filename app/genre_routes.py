from flask import Blueprint, jsonify
from app.models.genre import Genre

genre_bp = Blueprint("genres", __name__, url_prefix = "/genres")

@genre_bp.route("", methods = ["GET"])
def get_all_genres():
    genres = Genre.query.all()

    genre_response = [genre.to_json() for genre in genres]

    return jsonify(genre_response), 200

@genre_bp.route("", methods = ["POST"])
def make_new_genre():
    pass