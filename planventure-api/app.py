from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Basic configurations
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Basic model example
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<ExampleModel {self.name}>'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/test-db')
def test_db():
    db.create_all()
    test_entry = ExampleModel(name='Test Entry')
    db.session.add(test_entry)
    db.session.commit()
    return jsonify({"message": "Database test successful", "entry": test_entry.name})

if __name__ == '__main__':
    app.run(debug=True)
