from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/stock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book Model
class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(250), nullable=False)

    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

@api.route('/books')
class BooksResource(Resource):

    def get(self):

        books_list = Book.query.all()
        books = []

        for book in books_list:
            books.append({'title': book.title,'author': book.author,'genre': book.genre})

        return jsonify({'Books ': books})

    def post(self):
        parser.add_argument('title', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('genre', type=str)

        args = parser.parse_args()

        new_book = Book(args['title'],args['author'],args['genre'])

        db.session.add(new_book)
        db.session.commit()

        return jsonify({"message": "Book added to DB."})

@api.route('/books/<int:id>')
class BookResource(Resource):

    def get(self, id):

        book_obj = Book.query.filter_by(id=id).first()

        book = {'title': book_obj.title,'author': book_obj.author,'genre': book_obj.genre}

        return jsonify({'Book ': book})

    def put(self, id):
        parser.add_argument('title', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('genre', type=str)

        args = parser.parse_args()

        Book.query.filter_by(id=id).update({'title':args['title'],'author':args['author'],'genre':args['genre']})

        db.session.commit()

        return jsonify({"message": "Book updated."})

    def delete(self, id):

        Book.query.filter_by(id=id).delete()

        db.session.commit()

        return jsonify({"message": "Book deleted."})
