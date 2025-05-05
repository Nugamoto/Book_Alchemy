# 📚 Book Alchemy

Welcome to **Book Alchemy**, a digital library built with **Flask** and **SQLAlchemy**, where you can manage your books and authors — and bring a touch of magic to your collection! ✨

---

## 🚀 Features

- 📖 Add, view, and delete books
- 👩‍💼 Manage authors and their associated books
- 🔍 Search and sort your library
- 🖼️ View book cover images (via Open Library API)
- ✏️ Add or update ratings (1–10) for each book
- 🧾 Export-ready structure for detail views and future extensions

---

## 🔧 Technologies Used

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite**
- **Jinja2**
- **Bootstrap 5**
- **Open Library Covers API** (for cover images)

---

## 💻 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Nugamoto/Book_Alchemy.git
cd Book_Alchemy
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
python app.py
```

Then visit: [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
Book_Alchemy/
├── app.py
├── data_models.py
├── data/
│   └── library.sqlite
├── templates/
│   ├── home.html
│   ├── add_book.html
│   ├── add_author.html
│   ├── book_detail.html
│   └── author_detail.html
└── static/ (optional for CSS/images)
```

---

## ✨ Bonus Features Implemented

- ✅ UI redesign with Bootstrap and ChatGPT assistance
- ✅ Book & author detail pages
- ✅ Author deletion (incl. cascading book deletion)
- ✅ Book rating system (1–10)
- 🔜 [Optional] AI-based recommendation system via ChatGPT API (planned)

---

## 📄 License

MIT – do what you want with it! 😄  
Feel free to fork the project, submit pull requests, or open issues!

---

## 🙌 Acknowledgements

Special thanks to:

- [Open Library](https://openlibrary.org/developers/api) for cover images
- [Conventional Commits](https://www.conventionalcommits.org) for clean commit history
- ChatGPT for pair programming assistance 🤖
