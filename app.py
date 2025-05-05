import os
from datetime import datetime

from flask import Flask, request, flash, redirect, render_template, url_for

from data_models import db, Author

app = Flask(__name__)
app.secret_key = "supergeheimespasswort123"

# absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

db.init_app(app)


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


if __name__ == "__main__":
    app.run(debug=True)
