from app import db

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    books = db.relationship("Book", secondary = "book_genre", back_populates = "genres")

    def to_json(self):
        return {"id": self.id, 
                "name": self.name}