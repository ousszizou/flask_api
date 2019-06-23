
# API => application programming interface

# web services apis { REST }, respresentational state transfer

# CRUD => create - read - update - delete

# HTTP methods :

    # GET /books             => get list of books (READ)
    # GET /books/:id         => get a book by its ID (READ)
    # POST /book            => create a new book (CREATE)
    # PUT /books/:id        => update an existing book (UPDATE)
    # DELETE /books/:id      => delete an existing book (DELETE)

# example :

    # https://reqres.in/api/users

    # client == ( request to server ) ==> server
        # request : https://api.website.com/v1/api/getUsersProfile?userID=1
            # REST API endpoint : https://api.website.com/v1/api/
            # API method : getUsersProfile
            # params : userID

    # client <== ( response to client ) == server
        # response : JSON / XML ....

# HTTP STATUS CODE :

    # 200 OK: This means the request was successful
    # 201 Created: This means the resource has been created
    # 400 Bad Request: The request cannot be processed because of bad request syntax
    # 404 Not Found: This says the server wasn't able to find the requested page

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/stock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(250), nullable=False)

    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

# http://localhost:5000/books
@app.route('/books', methods=['GET', 'POST'])
def add_get_books():
    if request.method == 'POST':
        book_title = request.json['title']
        book_author = request.json['author']
        book_genre = request.json['genre']

        new_book = Book(book_title,book_author,book_genre)

        db.session.add(new_book)
        db.session.commit()

        return 'created', 201


    books_list = Book.query.all()
    books = []

    for book in books_list:
        books.append({'title': book.title, 'author': book.author, 'genre': book.genre})

    return jsonify({'Books:': books})

# http://localhost:5000/books/3 (GET)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):

    book_obj = Book.query.filter_by(id=book_id).first()

    book = {'title': book_obj.title , 'author': book_obj.author, 'genre': book_obj.genre}

    return jsonify({'Book :': book})

# http://localhost:5000/books/3 (PUT)
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):

    book_title = request.json['title']
    book_author = request.json['author']
    book_genre = request.json['genre']

    Book.query.filter_by(id=book_id).update({'title': book_title, 'author': book_author, 'genre': book_genre})

    db.session.commit()

    return 'updated', 200


# http://localhost:5000/books/3 (DELETE)
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):

    Book.query.filter_by(id=book_id).delete()

    db.session.commit()

    return 'deleted', 200
