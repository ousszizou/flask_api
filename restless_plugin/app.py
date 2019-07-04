from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)

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

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Book, url_prefix='/api/v2', collection_name='livre', methods=['GET', 'POST', 'PUT', 'DELETE'])
