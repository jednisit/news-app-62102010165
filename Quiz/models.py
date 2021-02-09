from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    genre = db.Column(db.String())
    heigh = db.Column(db.Integer())
    publisher = db.Column(db.String())

    def __repr__(self):
        return f"{self.id}:{self.title}:{self.author}:{self.genre}:{self.heigh}:{self.publisher}"
