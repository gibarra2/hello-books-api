from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)

    def to_json(self):
        return {"id": self.id,
                "name": self.name}
    @classmethod
    def make_new_author(cls, request_body):
        new_author = cls(name = request_body["name"])

        return new_author