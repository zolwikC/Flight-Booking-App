from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
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
    is_admin = db.Column(db.Boolean, default=False)  # Domyślnie użytkownicy nie są administratorami
    phone = db.Column(db.String(15), nullable=True)

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
    is_paid = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), nullable=True)  # Nowa kolumna
    phone = db.Column(db.String(15), nullable=True)   # Nowa kolumna

    # Relacja z tabelą Flight
    flight = db.relationship('Flight', backref='bookings', lazy=True)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    flight = db.relationship('Flight')


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
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Pobranie danych z formularza
        departure_city = request.form.get("departure_city")
        arrival_city = request.form.get("arrival_city")
        date = request.form.get("date")
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")

        # Filtrowanie lotów
        flights = Flight.query
        if departure_city:
            flights = flights.filter(Flight.departure_city.ilike(f"%{departure_city}%"))
        if arrival_city:
            flights = flights.filter(Flight.arrival_city.ilike(f"%{arrival_city}%"))
        if date:
            flights = flights.filter(Flight.date == date)
        if min_price:
            flights = flights.filter(Flight.price >= float(min_price))
        if max_price:
            flights = flights.filter(Flight.price <= float(max_price))
        flights = flights.all()
    else:
        # Wyświetlanie wszystkich lotów domyślnie
        flights = Flight.query.all()

    favorite_ids = []
    if current_user.is_authenticated:
        favorite_ids = [fav.flight_id for fav in Favorite.query.filter_by(user_id=current_user.id).all()]

    return render_template("index.html", flights=flights, favorite_ids=favorite_ids)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Sprawdzenie, czy hasła się zgadzają
        if password != confirm_password:
            return "Passwords do not match!"

        # Sprawdzenie, czy użytkownik już istnieje
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered!"

        # Hashowanie hasła
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Tworzenie nowego użytkownika
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
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

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if not current_user.is_admin:
        return "Access Denied! Only admins can access this page."

    if request.method == "POST":
        try:
            # Pobieranie danych z formularza
            departure_city = request.form.get("departure_city")
            arrival_city = request.form.get("arrival_city")
            date = request.form.get("date")
            price = float(request.form.get("price", 0))  # Domyślnie 0, jeśli brak wartości
            available_seats = int(request.form.get("available_seats", 0))  # Domyślnie 0

            # Walidacja danych
            if not departure_city or not arrival_city or not date or price <= 0 or available_seats <= 0:
                return "All fields are required and must be valid!"

            # Tworzenie nowego lotu
            new_flight = Flight(
                departure_city=departure_city,
                arrival_city=arrival_city,
                date=date,
                price=price,
                available_seats=available_seats
            )
            db.session.add(new_flight)
            db.session.commit()
            return redirect(url_for("admin"))
        except Exception as e:
            return f"An error occurred: {str(e)}"

    flights = Flight.query.all()
    return render_template("admin.html", flights=flights)


@app.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():
    if not current_user.is_admin:
        return "Access Denied! Only admins can access this page."

    if request.method == "POST":
        user_id = int(request.form["user_id"])
        is_admin = request.form.get("is_admin") == "on"

        user = User.query.get(user_id)
        if user:
            user.is_admin = is_admin
            db.session.commit()

    users = User.query.all()
    return render_template("manage_users.html", users=users)


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
        email = request.form["email"]  # Pobieranie emaila
        phone = request.form["phone"]  # Pobieranie numeru telefonu

        if number_of_passengers > flight.available_seats:
            return "Not enough seats available. Please choose fewer seats."

        # Dodanie rezerwacji
        booking = Booking(
            user_id=current_user.id,
            flight_id=flight.id,
            number_of_passengers=number_of_passengers,
            email=email,
            phone=phone
        )
        flight.available_seats -= number_of_passengers
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for("my_bookings"))
    return render_template("book.html", flight=flight)


@app.route("/pay_booking/<int:booking_id>", methods=["POST"])
@login_required
def pay_booking(booking_id):
    """
    Trasa oznaczająca rezerwację jako opłaconą.
    """
    # Pobieranie rezerwacji na podstawie ID
    booking = Booking.query.get_or_404(booking_id)

    # Sprawdzenie, czy rezerwacja należy do aktualnie zalogowanego użytkownika
    if booking.user_id != current_user.id:
        return "Access Denied!"

    # Oznaczenie rezerwacji jako opłaconej
    booking.status = "Paid"
    db.session.commit()
    return redirect(url_for("my_bookings"))

@app.route("/cancel_booking/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    """
    Trasa anulująca rezerwację.
    """
    # Pobieranie rezerwacji na podstawie ID
    booking = Booking.query.get_or_404(booking_id)

    # Sprawdzenie, czy rezerwacja należy do aktualnie zalogowanego użytkownika
    if booking.user_id != current_user.id:
        return "Access Denied!"

    # Anulowanie rezerwacji
    if booking.status != "Cancelled":
        booking.status = "Cancelled"
        booking.flight.available_seats += booking.number_of_passengers
        db.session.commit()

    return redirect(url_for("my_bookings"))
@app.route("/search", methods=["GET", "POST"])
def search_flights():
    if request.method == "POST":
        departure_city = request.form.get("departure_city")
        arrival_city = request.form.get("arrival_city")
        date = request.form.get("date")
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")

        # Filtruj loty
        flights = Flight.query
        if departure_city:
            flights = flights.filter(Flight.departure_city.ilike(f"%{departure_city}%"))
        if arrival_city:
            flights = flights.filter(Flight.arrival_city.ilike(f"%{arrival_city}%"))
        if date:
            flights = flights.filter(Flight.date == date)
        if min_price:
            flights = flights.filter(Flight.price >= float(min_price))
        if max_price:
            flights = flights.filter(Flight.price <= float(max_price))
        
        flights = flights.all()
        return render_template("search_results.html", flights=flights)

    return render_template("search.html")

@app.route("/edit_flight/<int:flight_id>", methods=["GET", "POST"])
@login_required
def edit_flight(flight_id):
    if not current_user.is_admin:
        return "Access Denied! Only admins can edit flights."

    flight = Flight.query.get_or_404(flight_id)  # Pobierz lot lub zwróć błąd 404

    if request.method == "POST":
        # Zaktualizuj dane lotu
        flight.departure_city = request.form["departure_city"]
        flight.arrival_city = request.form["arrival_city"]
        flight.date = request.form["date"]
        try:
            flight.price = float(request.form["price"])
            flight.available_seats = int(request.form["available_seats"])
        except ValueError:
            return "Invalid input! Price and seats must be valid numbers."

        db.session.commit()  # Zapisz zmiany w bazie danych
        return redirect(url_for("admin"))  # Przekieruj do panelu admina

    return render_template("edit_flight.html", flight=flight)  # Przekaż dane lotu do formularza

@app.route("/delete_flight/<int:flight_id>", methods=["POST"])
@login_required
def delete_flight(flight_id):
    if not current_user.is_admin:
        return "Access Denied! Only admins can delete flights."

    flight = Flight.query.get_or_404(flight_id)  # Pobierz lot lub zwróć błąd 404
    db.session.delete(flight)  # Usuń lot z bazy danych
    db.session.commit()  # Zapisz zmiany
    return redirect(url_for("admin"))  # Przekieruj do panelu admina

@app.route("/admin/reports")
@login_required
def admin_reports():
    if not current_user.is_admin:
        return "Access Denied! Only admins can access this page."

    # Statystyki
    total_users = User.query.count()
    total_bookings = Booking.query.count()

    # Liczba rezerwacji dla każdego lotu
    flight_stats = db.session.query(
        Flight.departure_city,
        Flight.arrival_city,
        Flight.date,
        db.func.count(Booking.id).label("booking_count")
    ).join(Booking, Booking.flight_id == Flight.id, isouter=True) \
     .group_by(Flight.id) \
     .all()

    # Przygotowanie danych do wykresu
    labels = [f"{stat.departure_city} → {stat.arrival_city}" for stat in flight_stats]
    data = [stat.booking_count for stat in flight_stats]

    # Render szablonu
    return render_template(
        "admin_reports.html",
        total_users=total_users,
        total_bookings=total_bookings,
        flight_stats=flight_stats,
        labels=labels,
        data=data
    )



@app.route("/my_bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("my_bookings.html", bookings=bookings)


@app.route("/download_bookings")
@login_required
def download_bookings():
    import csv
    from io import StringIO

    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Departure", "Arrival", "Date", "Passengers", "Status"])
    for b in bookings:
        writer.writerow([
            b.flight.departure_city,
            b.flight.arrival_city,
            b.flight.date,
            b.number_of_passengers,
            b.status,
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=bookings.csv"},
    )


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")
        current_user.phone = request.form.get("phone")
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("profile.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if not bcrypt.check_password_hash(current_user.password, current_password):
            return "Current password incorrect"
        if new_password != confirm_password:
            return "Passwords do not match"
        current_user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("change_password.html")


@app.route("/toggle_favorite/<int:flight_id>", methods=["POST"])
@login_required
def toggle_favorite(flight_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, flight_id=flight_id).first()
    if favorite:
        db.session.delete(favorite)
    else:
        db.session.add(Favorite(user_id=current_user.id, flight_id=flight_id))
    db.session.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/favorites")
@login_required
def favorites():
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    flights = [f.flight for f in favs]
    return render_template("favorites.html", flights=flights)


@app.route("/api/flights")
def api_flights():
    flights = Flight.query.all()
    return jsonify([
        {
            "id": f.id,
            "departure_city": f.departure_city,
            "arrival_city": f.arrival_city,
            "date": f.date,
            "price": f.price,
            "available_seats": f.available_seats,
        }
        for f in flights
    ])

if __name__ == "__main__":
    app.run(debug=True)
