from flask import Flask, render_template, request, redirect
from sqlalchemy import desc

from database import db, Books, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookshelf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#
#     genres = ['Literary Fiction', 'Mystery', 'Thriller', 'Horror', 'Historical', 'Romance', 'Fantasy', 'Detective']
#
#     for i in genres:
#         db.session.add(Genre(genre=i))
#
#         try:
#             db.session.commit()
#         except:
#             'Error'


@app.route('/genres')
def check_genres():
    genres = Genre.query.all()
    return render_template('genres.html', genres=genres)


@app.route('/')
def index():
    books = Books.query.order_by(desc('date_added')).limit(15)
    return render_template('index.html', books=books)


@app.route('/all_books')
def all_books():
    books = Books.query.all()
    return render_template('index.html', books=books)


@app.route('/add_book', methods=['POST', 'GET'])
def add_new_book():
    if request.method == 'POST':
        title = request.form['title']
        name_of_genre = request.form['genre']
        genre = Genre.query.filter(Genre.genre == name_of_genre).first()
        description = request.form['description']

        new_book = Books(title=title, genre=genre, description=description)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'

    else:
        return render_template('add_book.html')


@app.route('/is_read/<int:id>')
def is_read(id):
    book = Books.query.get(id)
    book.is_read = not book.is_read

    try:
        db.session.commit()
        return redirect(request.referrer)
    except:
        return 'Error'


@app.route('/book/<int:id>', methods=['POST', 'GET'])
def book(id):
    book = Books.query.get(id)
    genres = Genre.query.all()

    if request.method == 'POST':
        book.title = request.form['title']
        name_of_genre = request.form['genre']
        book.genre = Genre.query.filter(Genre.genre == name_of_genre).first()
        book.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'

    else:
        return render_template('book.html', book=book, genres=genres)


@app.route('/book/<int:id>/del')
def book_delete(id):
    book = Books.query.get(id)
    try:
        db.session.delete(book)
        db.session.commit()
        return redirect(request.referrer)
    except:
        return 'Error'


@app.route('/book/<int:id>/del_book')
def book_delete_from_bookinfo(id):
    book = Books.query.get(id)
    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error'


@app.route('/books/<string:genre>')
def genre_page(genre):
    books = Books.query.join(Genre).where(Genre.genre == genre)
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
