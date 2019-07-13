from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "AlgorithmSecretKey"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/stock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = generate_password_hash(password, method="sha256")
        self.admin = admin

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message: ": "token is missing"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({"message: ": "token is not valid!"})

        return f(current_user, *args, **kwargs)

    return decorated


# Routes
@app.route('/users', methods=['GET', 'POST'])
@token_required
def get_all_users(current_user):
    if request.method == 'POST':
        data = request.get_json()

        new_user = User(email=data['email'],password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'Message: ': 'New user created.'})

    users_list = User.query.all()
    users = []

    for user in users_list:
        users.append({'id': user.id, 'email': user.email})

    return jsonify({'Users:': users})

@app.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'Message: ': 'user not found.'})

    user.admin = True
    db.session.commit()

    return jsonify({'Message: ': 'user updated.'})


@app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):

    if not current_user.admin:
        return jsonify({"message: ": "heey! you cannot do this action"}), 401

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'Message: ': 'user not found.'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'Message: ': 'user deleted.'})

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verfiy', 401, {'WWW-Authenticate': "Basic realm='Login required'"})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('could not verfiy', 401, {'WWW-Authenticate': "Basic realm='Login required'"})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"email": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'Token: ' : token.decode('UTF-8')})

    return make_response('could not verfiy', 401, {'WWW-Authenticate': "Basic realm='Login required'"})
