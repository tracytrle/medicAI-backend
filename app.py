from flask import Flask, request, jsonify, session
from config import ApplicationConfig
from models import db, User
from flask_bcrypt import Bcrypt
from flask import abort
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)
server_session = Session(app)
cors = CORS(app, supports_credentials=True)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
  return "Hello, World!"

#return current loggin user infor
@app.route('/auth', methods=["GET"])
def get_current_user():
    user_id = session.get('user_id') 
    
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route('/register', methods=["POST"]) # This route will be used to register a new user.
def register_user():
    email = request.json['email']
    password = request.json['password']

    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        abort(409, description="User already exists")
    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id
    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "session_id": session.sid
    })

@app.route('/login', methods=["POST"]) # This route will be used to log in an existing user.
def login_user():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session['user_id'] = user.id
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route('/logout', methods=["POST"]) # This route will be used to log out the current user.
def logout_user():
    session.pop('user_id', None)
    return "200"      

if __name__ == "__main__":
    app.run(debug=True)