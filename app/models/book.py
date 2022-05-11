from sqlalchemy import ForeignKey
from app import db

class Book(db.Model):
    # Creates id, title, and description attributes which map to columns of table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, ForeignKey("author.id"))
    author = db.relationship("Author", back_populates = "books")
    genre = db.relationship("Genre", secondary = "book_genre", back_populates = "books")


    def to_json(self):
        return {"id": self.id, 
                "title": self.title, 
                "description": self.description}