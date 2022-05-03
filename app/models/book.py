from app import db

class Book(db.Model):
    # Creates id, title, and description attributes which map to columns of table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    def to_json(self):
        return {"id": self.id, 
                "title": self.title, 
                "description": self.description}