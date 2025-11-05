from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import joblib
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning
db = SQLAlchemy(app)

# Load ML model
try:
    model = joblib.load('rabies_model.pkl')
except FileNotFoundError:
    print("Error: rabies_model.pkl not found. Ensure the model file exists.")
    exit(1)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Prediction history model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    inputs = db.Column(db.String(500), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main'))  # Redirect logged-in users to main page
    return redirect(url_for('signup'))

@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Ensure only logged-in users access main page
    return render_template('main.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Basic validation
            if User.query.filter_by(username=username).first():
                return render_template('signup.html', error='Username already exists')
            if User.query.filter_by(email=email).first():
                return render_template('signup.html', error='Email already exists')

            hashed_password = generate_password_hash(password)
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return render_template('signup.html', error=f'Error: {str(e)}')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session.permanent = True
                return redirect(url_for('main'))  # Redirect to main page after login
            return render_template('login.html', error='Invalid credentials')
        except Exception as e:
            return render_template('login.html', error=f'Error: {str(e)}')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Validate and collect form data
            data = {
                'Age': int(request.form['age']),
                'Location_Risk': request.form['location_risk'],
                'Animal_Type': request.form['animal_type'],
                'Bite_Severity': request.form['bite_severity'],
                'Vaccination_Status': request.form['vaccination_status'],
                'PEP': request.form['pep'],
                'Time_Since_Exposure': float(request.form['time_since_exposure']),
                'Wound_Location': request.form['wound_location'],
                'Animal_Vaccination': request.form['animal_vaccination']
            }

            # Validate inputs
            if data['Age'] < 0 or data['Age'] > 100:
                return render_template('predict.html', error='Age must be between 0 and 100')
            if data['Time_Since_Exposure'] < 0 or data['Time_Since_Exposure'] > 720:
                return render_template('predict.html', error='Time since exposure must be between 0 and 720 hours')

            # Make prediction
            df = pd.DataFrame([data])
            probs = model.predict_proba(df)[0]
            risk_levels = model.classes_
            max_prob_idx = probs.argmax()
            risk = risk_levels[max_prob_idx]
            percentage = probs[max_prob_idx] * 100

            # Limit percentage to 98% for saving in database
            if percentage > 98:
                saved_percentage = 98
            else:
                saved_percentage = percentage

            # Store prediction
            prediction = Prediction(
                user_id=session['user_id'],
                inputs=str(data),
                risk_level=risk,
                probability=saved_percentage,  # Use limited percentage here
                created_at=datetime.utcnow()
            )
            db.session.add(prediction)
            db.session.commit()

            return render_template('predict.html', risk=risk, percentage=percentage)
        except ValueError as e:
            return render_template('predict.html', error='Invalid input. Please check your data.')
        except Exception as e:
            return render_template('predict.html', error=f'Error: {str(e)}')
    
    return render_template('predict.html')

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        predictions = Prediction.query.filter_by(user_id=session['user_id']).order_by(Prediction.created_at.desc()).all()
        return render_template('history.html', predictions=predictions)
    except Exception as e:
        return render_template('history.html', error=f'Error: {str(e)}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)