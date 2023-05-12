from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pages = db.Column(db.Integer, default=1)
    is_read = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, nullable=False, default=func.now())

    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id", ondelete="SET NULL"))
    genre = relationship("Genre", back_populates="books")

    def __repr__(self):
        return f'Name of book {self.title}'


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100), nullable=False, unique=True)

    books = relationship("Books", back_populates="genre")

    def __repr__(self):
        return f'{self.genre}'

