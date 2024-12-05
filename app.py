from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # type: ignore
from flask_login import LoginManager # type: ignore


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/flights.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Modele bazy danych
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    number_of_passengers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), default="Pending")

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/register", methods=["GET", "POST"])
def register():
    # Rejestracja użytkownika
    pass

@app.route("/login", methods=["GET", "POST"])
def login():
    # Logowanie użytkownika
    pass

@app.route("/flight/<int:flight_id>")
def flight_details(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    return render_template("flights.html", flight=flight)

@app.route("/book/<int:flight_id>", methods=["GET", "POST"])
def book_flight(flight_id):
    # Rezerwacja lotu
    pass
