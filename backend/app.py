from flask import Flask, url_for, request, redirect, render_template, flash, jsonify, session
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, logout_user, login_user, current_user, UserMixin, login_required
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from uuid import uuid4



app = Flask(__name__)



app.config['SECRET_KEY']= 'your_secret_key'
app.config['SQLALCHEMY_DATBASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TEST_MODICIATION'] = False


db = SQLAlchemy(app)
migrate= Migrate(db,app)
bcrypt = Bcrypt(app)
CORS(app,supports_credentials=True)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

def get_uuid():
    return uuid4().hex

class User(db.Model, UserMixin):
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    email= db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20, nullable=True))
    location = db.Column(db.String(200), nullable=True)
    school = db.Column(db.String(200), nullable=True)
    year = db.Column(db.String(10, nullable=True))
    experience = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)
    user_type = db.Column(db.String(150), default='student')

    def __repr__(self):
        return f"<User{self.email}>"
    


class Opportunities(db.Model):
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)


@login_manager.user_loader

def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"Email": "Unauthorized Access"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    login_user(user)

    return jsonify({
        id: user.id, 
        email: user.email,

    })

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json["email"]
    password = request.json["password"]

    if User.query.filter_by(email=email).first():
        return jsonify({"Email": "Unauthorized Access"}), 401
    
    hashed_password = bcrypt.generate_hashed_password(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)

    db.session(new_user)
    db.commit()

    login_user(new_user)
    return jsonify({
        id: new_user.id, 
        email: new_user.email,

    })
    
@app.route('/logout', methods=['GET'])
def logout():
    logout_user

@app.route('/api/user/<user_id>/phone', methods=['GET'])
@login_required
def get_phone(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"phone": user.phone or "Not Provided"})

@app.route('/api/user/<user_id>/email', methods=['GET'])
@login_required
def get_email(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"email": user.email})

@app.route('api/user/<user_id>/location')
@login_required
def get_location(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"Location": user.location})

@app.route('api/user/<user_id>/school')
@login_required
def get_school(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"school": user.school or "Not Provided"})

@app.route('api/user/<user_id>/year')
@login_required
def get_year(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"Year": user.year or "Not Provided"})

@app.route
@login_required
def get_experience(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"Experience": user.experience or "Not Provided"})


