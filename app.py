from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # type: ignore
from flask_login import LoginManager, login_user, logout_user, UserMixin,login_required, current_user # type: ignore
import os

# Tworzenie aplikacji Flask
app = Flask(__name__)

# Absolutna ścieżka do bazy danych
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')

# Tworzenie folderu na bazę danych, jeśli nie istnieje
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(DB_DIR, 'flights.db')}"
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Modele bazy danych
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Flask-Login properties
    @property
    def is_active(self):
        """All users are active by default."""
        return True

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
    status = db.Column(db.String(100), default="Confirmed")

    # Relacja z tabelą Flight
    flight = db.relationship('Flight', backref='bookings', lazy=True)


@app.route("/add_sample_flights_sql")
def add_sample_flights_sql():
    db.session.execute("""
        INSERT INTO flight (departure_city, arrival_city, date, price, available_seats)
        VALUES ('Warsaw', 'Berlin', '2024-12-10', 100.0, 50),
               ('Paris', 'London', '2024-12-11', 120.0, 40),
               ('New York', 'Los Angeles', '2024-12-12', 300.0, 60)
    """)
    db.session.commit()
    return "Sample flights added using raw SQL!"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Automatyczne tworzenie bazy danych, jeśli nie istnieje
db_path = os.path.join(DB_DIR, 'flights.db')
if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()
        print("Baza danych została utworzona.")
else:
    print("Baza danych już istnieje.")

# Trasy aplikacji
@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            return "Invalid email or password"
    return render_template("login.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



@app.route("/book/<int:flight_id>", methods=["GET", "POST"])
@login_required
def book_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    if request.method == "POST":
        number_of_passengers = int(request.form["passengers"])
        if number_of_passengers > flight.available_seats:
            return "Not enough seats available. Please choose fewer seats."

        # Dodanie rezerwacji
        booking = Booking(
            user_id=current_user.id,
            flight_id=flight.id,
            number_of_passengers=number_of_passengers
        )
        flight.available_seats -= number_of_passengers
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for("my_bookings"))
    return render_template("book.html", flight=flight)


@app.route("/my_bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("my_bookings.html", bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True)
