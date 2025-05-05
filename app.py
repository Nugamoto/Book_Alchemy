"""
Book Alchemy Flask Application.

This Flask app allows users to manage a personal digital library with books and authors.
Users can add, delete, rate, and view details of books and authors, and the app includes
search, sort, and filter functionalities.
"""

import os
from datetime import datetime

from flask import Flask, request, flash, redirect, render_template, url_for
from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError

from data_models import db, Author, Book

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "supersecretpassword123"

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db.init_app(app)


@app.route("/")
def home():
    """
    Display the home page with a list of books.

    Supports sorting by title or author, ascending or descending,
    and filtering by search query.
    """
    sort = request.args.get("sort", "title")
    direction = request.args.get("direction", "asc")
    q = request.args.get("q", "").strip()

    query = Book.query.join(Author)

    if q:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{q}%"),
                Author.name.ilike(f"%{q}%")
            )
        )

    if sort == "author":
        order = asc(Author.name) if direction == "asc" else desc(Author.name)
    else:
        order = asc(Book.title) if direction == "asc" else desc(Book.title)

    books = query.order_by(order).all()
    return render_template("home.html", books=books, sort=sort, direction=direction)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Display and handle the form to add a new author.

    Validates date fields and commits to the database.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        try:
            birth_date = datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d").date()
            dod_str = request.form.get("date_of_death", "").strip()
            date_of_death = datetime.strptime(dod_str, "%Y-%m-%d").date() if dod_str else None

            author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(author)
            db.session.commit()
            flash("Author successfully added!")
            return redirect(url_for("add_author"))
        except ValueError:
            flash("Please enter valid dates in YYYY-MM-DD format.")
        except SQLAlchemyError:
            db.session.rollback()
            flash("Database error: unable to add author.")
    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Display and handle the form to add a new book.

    Validates all input fields including ISBN, publication year, author, and rating.
    """
    if request.method == "POST":
        try:
            isbn = request.form.get("isbn", "").strip()
            if len(isbn) not in (10, 13):
                flash("ISBN must be 10 or 13 characters long.")
                raise ValueError("Invalid ISBN length.")

            title = request.form.get("title", "").strip()
            publication_year = int(request.form.get("publication_year", "").strip())
            current_year = datetime.now().year
            if publication_year < 1400 or publication_year > current_year:
                flash("Publication year must be between 1400 and the current year.")
                raise ValueError("Invalid publication year.")

            author_id = int(request.form.get("author_id", "").strip())
            if not Author.query.get(author_id):
                flash("Selected author does not exist.")
                raise ValueError("Invalid author ID.")

            rating_raw = request.form.get("rating", "").strip()
            if rating_raw:
                if rating_raw.isdigit() and 1 <= int(rating_raw) <= 10:
                    rating = int(rating_raw)
                else:
                    flash("Rating must be a number between 1 and 10.")
                    raise ValueError("Invalid rating value.")
            else:
                rating = None

            book = Book(
                isbn=isbn,
                title=title,
                publication_year=publication_year,
                author_id=author_id,
                rating=rating
            )
            db.session.add(book)
            db.session.commit()
            flash("Book successfully added!")
            return redirect(url_for("add_book"))

        except ValueError:
            flash("Please correct the highlighted errors and try again.")
        except SQLAlchemyError:
            db.session.rollback()
            flash("Database error: could not add the book.")

    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Delete a book from the database.

    Also deletes the author if the book was their only one.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()
    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f"Book and author '{author.name}' deleted.")
    else:
        flash(f"Book '{book.title}' deleted.")
    return redirect(url_for("home"))


@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    """
    Delete an author and all their associated books from the database.
    """
    author = Author.query.get_or_404(author_id)
    for book in author.books:
        db.session.delete(book)
    db.session.delete(author)
    db.session.commit()
    flash(f"Author '{author.name}' and all their books have been deleted.")
    return redirect(url_for("home"))


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    """
    Display a detail page for a specific book.
    """
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)


@app.route("/author/<int:author_id>")
def author_detail(author_id):
    """
    Display a detail page for a specific author.
    """
    author = Author.query.get_or_404(author_id)
    return render_template("author_detail.html", author=author)


@app.route("/book/<int:book_id>/rating", methods=["GET", "POST"])
def rate_book(book_id):
    """
    Display and handle form to rate or update the rating of a book.

    Only accepts values between 1 and 10.
    """
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        rating = request.form.get("rating", "").strip()
        if rating.isdigit() and 1 <= int(rating) <= 10:
            try:
                book.rating = int(rating)
                db.session.commit()
                flash(f"Rating for '{book.title}' was updated to {book.rating}/10.")
                return redirect(url_for("home"))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Database error: could not update rating.")
        else:
            flash("Please enter a valid rating from 1 to 10.")
    return render_template("rate_book.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)
