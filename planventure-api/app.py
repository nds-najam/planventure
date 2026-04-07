from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from password_utils import hash_password, verify_password
from jwt_utils import generate_tokens
from email_validation import is_valid_email, is_valid_password

load_dotenv()

app = Flask(__name__)
CORS(app)

# Basic configurations
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour in seconds

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    trips = db.relationship('Trip', backref='user', lazy=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = hash_password(password)
    
    def check_password(self, password):
        """Verify a password against the stored hash."""
        return verify_password(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    itinerary = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Trip {self.destination} for user_id={self.user_id}>'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/auth/register', methods=['POST'])
def register():
    """Register a new user with email validation."""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing required fields: username, email, password"}), 400
    
    username = data.get('username').strip()
    email = data.get('email').strip()
    password = data.get('password')
    
    # Validate email format
    if not is_valid_email(email):
        return jsonify({"msg": "Invalid email format"}), 400
    
    # Validate password strength
    if not is_valid_password(password):
        return jsonify({"msg": "Password must be at least 8 characters with uppercase, lowercase, and digits"}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 409
    
    # Create new user
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "msg": "User registered successfully",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Registration failed: {str(e)}"}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT tokens."""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401
    
    tokens = generate_tokens(user.id, {'id': user.id, 'username': user.username})
    
    return jsonify({
        "msg": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "tokens": tokens
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
