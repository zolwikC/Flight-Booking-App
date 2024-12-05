import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

class FlightBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rezerwacja Biletów Lotniczych")
        self.root.geometry("600x800")
        
        self.selected_seat = None
        self.user_data = {}
        self.logged_in_user = None
        self.load_user_data()
        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        title_label = tk.Label(self.root, text="Rezerwacja Biletów Lotniczych", font=("Arial", 18))
        title_label.pack(pady=10)
        
        # Sekcja logowania/rejestracji
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=10)
        
        tk.Label(login_frame, text="Nazwa użytkownika:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="Hasło:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        login_button = tk.Button(login_frame, text="Zaloguj", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        register_button = tk.Button(login_frame, text="Zarejestruj", command=self.register)
        register_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Wybór punktu startowego
        start_label = tk.Label(self.root, text="Punkt startowy:")
        start_label.pack()
        self.start_combobox = ttk.Combobox(self.root, values=["Warszawa", "Kraków", "Gdańsk", "Wrocław"])
        self.start_combobox.pack(pady=5)
        
        # Wybór punktu docelowego
        destination_label = tk.Label(self.root, text="Punkt docelowy:")
        destination_label.pack()
        self.destination_combobox = ttk.Combobox(self.root, values=["Londyn", "Paryż", "Nowy Jork", "Tokio"])
        self.destination_combobox.pack(pady=5)
        
        # Wybór klasy lotu
        class_label = tk.Label(self.root, text="Klasa lotu:")
        class_label.pack()
        self.class_combobox = ttk.Combobox(self.root, values=["Ekonomiczna", "Biznesowa", "Pierwsza"])
        self.class_combobox.pack(pady=5)
        
        # Filtry lotów
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Maksymalna cena (PLN):").grid(row=0, column=0, padx=5, pady=5)
        self.max_price_entry = tk.Entry(filter_frame)
        self.max_price_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Maksymalna liczba przesiadek:").grid(row=1, column=0, padx=5, pady=5)
        self.max_stops_combobox = ttk.Combobox(filter_frame, values=[0, 1, 2, 3, "Bez ograniczeń"])
        self.max_stops_combobox.set("Bez ograniczeń")
        self.max_stops_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        # Przycisk zastosowania filtrów
        apply_filters_button = tk.Button(filter_frame, text="Zastosuj filtry", command=self.apply_filters)
        apply_filters_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Przycisk kalkulacji ceny
        calculate_button = tk.Button(self.root, text="Oblicz cenę", command=self.calculate_price)
        calculate_button.pack(pady=10)
        
        # Etykieta do wyświetlania ceny
        self.price_label = tk.Label(self.root, text="Cena: ")
        self.price_label.pack(pady=5)
        
        # Przycisk wyboru miejsca
        seat_button = tk.Button(self.root, text="Wybierz miejsce", command=self.show_seat_selection)
        seat_button.pack(pady=10)
        
        # Etykieta do wyświetlania wybranego miejsca
        self.seat_label = tk.Label(self.root, text="Wybrane miejsce: Brak")
        self.seat_label.pack(pady=5)
        
        # Przycisk rezerwacji
        book_button = tk.Button(self.root, text="Rezerwuj", command=self.book_flight)
        book_button.pack(pady=20)
        
        # Historia rezerwacji
        self.history_label = tk.Label(self.root, text="Historia rezerwacji: Brak")
        self.history_label.pack(pady=10)

    def load_user_data(self):
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as file:
                self.user_data = json.load(file)
        else:
            self.user_data = {}

    def save_user_data(self):
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.user_data and self.user_data[username]["password"] == password:
            self.logged_in_user = username
            messagebox.showinfo("Sukces", f"Zalogowano jako {username}")
            self.update_history_label()
        else:
            messagebox.showwarning("Błąd", "Nieprawidłowa nazwa użytkownika lub hasło.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.user_data:
            messagebox.showwarning("Błąd", "Użytkownik o tej nazwie już istnieje.")
        else:
            self.user_data[username] = {"password": password, "reservations": []}
            self.save_user_data()
            messagebox.showinfo("Sukces", "Rejestracja zakończona sukcesem.")

    def calculate_price(self):
        start = self.start_combobox.get()
        destination = self.destination_combobox.get()
        flight_class = self.class_combobox.get()
        
        if start and destination and flight_class:
            base_price = 500  # Podstawowa cena bazowa
            distance_factor = {
                ("Warszawa", "Londyn"): 1.2,
                ("Warszawa", "Paryż"): 1.5,
                ("Warszawa", "Nowy Jork"): 3.0,
                ("Warszawa", "Tokio"): 4.0,
                ("Kraków", "Londyn"): 1.3,
                ("Kraków", "Paryż"): 1.4,
                ("Kraków", "Nowy Jork"): 2.8,
                ("Kraków", "Tokio"): 3.8,
                # Dodaj inne kombinacje punktów
            }
            class_multiplier = {
                "Ekonomiczna": 1.0,
                "Biznesowa": 1.5,
                "Pierwsza": 2.5
            }
            
            distance_key = (start, destination)
            if distance_key in distance_factor:
                price = base_price * distance_factor[distance_key] * class_multiplier[flight_class]
                self.price_label.config(text=f"Cena: {price:.2f} PLN")
            else:
                self.price_label.config(text="Cena: N/A")
        else:
            self.price_label.config(text="Proszę wybrać wszystkie opcje.")

    def show_seat_selection(self):
        seat_window = tk.Toplevel(self.root)
        seat_window.title("Wybór miejsca")
        
        rows = 5
        columns = 4
        
        for i in range(rows):
            for j in range(columns):
                seat_number = f"{chr(65+i)}{j+1}"
                seat_button = tk.Button(seat_window, text=seat_number, width=5, command=lambda s=seat_number: self.select_seat(s, seat_window))
                seat_button.grid(row=i, column=j, padx=5, pady=5)

    def select_seat(self, seat_number, seat_window):
        self.selected_seat = seat_number
        self.seat_label.config(text=f"Wybrane miejsce: {seat_number}")
        seat_window.destroy()

    def book_flight(self):
        start = self.start_combobox.get()
        destination = self.destination_combobox.get()
        flight_class = self.class_combobox.get()
        
        if self.logged_in_user is None:
            messagebox.showwarning("Błąd", "Proszę się zalogować.")
            return
        
        if start and destination and flight_class and self.selected_seat:
            reservation = {
                "start": start,
                "destination": destination,
                "class": flight_class,
                "seat": self.selected_seat
            }
            self.user_data[self.logged_in_user]["reservations"].append(reservation)
            self.save_user_data()
            messagebox.showinfo("Rezerwacja", f"Zarezerwowano lot z {start} do {destination} w klasie {flight_class}, miejsce: {self.selected_seat}.")
            self.update_history_label()
        else:
            messagebox.showwarning("Błąd", "Proszę wybrać wszystkie opcje, w tym miejsce.")

    def update_history_label(self):
        if self.logged_in_user and self.user_data[self.logged_in_user]["reservations"]:
            reservations = self.user_data[self.logged_in_user]["reservations"]
            history_text = "Historia rezerwacji:\n" + "\n".join([
                f"Lot z {r['start']} do {r['destination']}, klasa: {r['class']}, miejsce: {r['seat']}"
                for r in reservations
            ])
            self.history_label.config(text=history_text)
        else:
            self.history_label.config(text="Historia rezerwacji: Brak")

    def apply_filters(self):
        max_price = self.max_price_entry.get()
        max_stops = self.max_stops_combobox.get()
        
        filters_text = "Zastosowano filtry:\n"
        if max_price:
            filters_text += f"Maksymalna cena: {max_price} PLN\n"
        if max_stops != "Bez ograniczeń":
            filters_text += f"Maksymalna liczba przesiadek: {max_stops}\n"
        
        messagebox.showinfo("Filtry", filters_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingApp(root)
    root.mainloop()
