import tkinter as tk
from tkinter import ttk

class FlightBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rezerwacja Biletów Lotniczych")
        self.root.geometry("600x400")
        
        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        title_label = tk.Label(self.root, text="Rezerwacja Biletów Lotniczych", font=("Arial", 18))
        title_label.pack(pady=10)
        
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
        
        # Przycisk kalkulacji ceny
        calculate_button = tk.Button(self.root, text="Oblicz cenę", command=self.calculate_price)
        calculate_button.pack(pady=10)
        
        # Etykieta do wyświetlania ceny
        self.price_label = tk.Label(self.root, text="Cena: ")
        self.price_label.pack(pady=5)
        
        # Przycisk rezerwacji
        book_button = tk.Button(self.root, text="Rezerwuj", command=self.book_flight)
        book_button.pack(pady=20)

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

    def book_flight(self):
        start = self.start_combobox.get()
        destination = self.destination_combobox.get()
        flight_class = self.class_combobox.get()
        
        if start and destination and flight_class:
            tk.messagebox.showinfo("Rezerwacja", f"Zarezerwowano lot z {start} do {destination} w klasie {flight_class}.")
        else:
            tk.messagebox.showwarning("Błąd", "Proszę wybrać wszystkie opcje.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingApp(root)
    root.mainloop()
