import os
from datetime import datetime

from flask import Flask, request, flash, redirect, render_template, url_for
from sqlalchemy import asc, desc, or_

from data_models import db, Author, Book

app = Flask(__name__)
app.secret_key = "supersecretpassword123"

# absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

db.init_app(app)


@app.route("/")
def home():
    sort = request.args.get("sort", "title")
    direction = request.args.get("direction", "asc")
    q = request.args.get("q", "").strip()

    # Query starten mit Join
    query = Book.query.join(Author)

    # Suche nach Titel ODER Autorname
    if q:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{q}%"),
                Author.name.ilike(f"%{q}%")
            )
        )

    # Sortierung anwenden
    if sort == "author":
        order = asc(Author.name) if direction == "asc" else desc(Author.name)
        query = query.order_by(order)
    else:
        order = asc(Book.title) if direction == "asc" else desc(Book.title)
        query = query.order_by(order)

    books = query.all()

    return render_template("home.html", books=books, sort=sort, direction=direction)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date = datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d").date()
        dod_str = request.form.get("date_of_death", "").strip()
        date_of_death = datetime.strptime(dod_str, "%Y-%m-%d").date() if dod_str else None

        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()

        flash("Author successfully added!")
        return redirect(url_for("add_author"))

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year = int(request.form.get("publication_year", "").strip())
        author_id = int(request.form.get("author_id", "").strip())
        book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)

        db.session.add(book)
        db.session.commit()
        flash("Book successfully added!")
        return redirect(url_for("add_book"))

    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


if __name__ == "__main__":
    app.run(debug=True)
