"""
Database models for the Book Alchemy Flask application.

Defines the SQLAlchemy models for authors and books, including relationships.
"""

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance used throughout the app
db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the digital library.

    Attributes:
        id (int): Primary key, unique ID for the author.
        name (str): Full name of the author.
        birth_date (date): Date of birth (required).
        date_of_death (date, optional): Date of death.
        books (list): Relationship to Book instances written by the author.
    """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    # One-to-many relationship: One author has many books
    books = db.relationship('Book', backref='author', lazy=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"


class Book(db.Model):
    """
    Represents a book in the digital library.

    Attributes:
        id (int): Primary key, unique ID for the book.
        isbn (str): ISBN number of the book (10 or 13 digits).
        title (str): Title of the book.
        publication_year (int): Year the book was published.
        rating (int, optional): User-provided rating (1–10).
        author_id (int): Foreign key linking to an author.
    """
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Book id={self.id} title='{self.title}'>"
