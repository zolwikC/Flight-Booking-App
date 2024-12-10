document.addEventListener("DOMContentLoaded", function () {
    const mapElement = document.getElementById("map");
    if (!mapElement) {
        console.error("Element #map nie został znaleziony. Upewnij się, że istnieje w pliku HTML.");
        return;
    }

    // Inicjalizacja mapy
    const map = L.map("map").setView([20.0, 0.0], 2);

    // Dodanie warstwy mapy
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Lista miast z współrzędnymi
    const cities = {
        "Warsaw": [52.2297, 21.0122],
        "Berlin": [52.5200, 13.4050],
        "Paris": [48.8566, 2.3522],
        "London": [51.5074, -0.1278],
        "New York": [40.7128, -74.0060],
        "Los Angeles": [34.0522, -118.2437],
        "Madrid": [40.4168, -3.7038],
        "Rome": [41.9028, 12.4964],
        "Tokyo": [35.6895, 139.6917],
        "Osaka": [34.6937, 135.5023],
        "Barcelona": [41.3851, 2.1734],
        "Amsterdam": [52.3676, 4.9041],
        "Munich": [48.1351, 11.5820],
        "Vienna": [48.2082, 16.3738],
        "Prague": [50.0755, 14.4378],
        "Moscow": [55.7558, 37.6173],
        "Saint Petersburg": [59.9343, 30.3351],
        "Dubai": [25.276987, 55.296249],
        "Abu Dhabi": [24.4539, 54.3773],
        "New Delhi": [28.6139, 77.2090],
        "Mumbai": [19.0760, 72.8777],
        "Sydney": [-33.8688, 151.2093],
        "Melbourne": [-37.8136, 144.9631],
        "Beijing": [39.9042, 116.4074],
        "Shanghai": [31.2304, 121.4737],
        "Rio de Janeiro": [-22.9068, -43.1729],
        "Sao Paulo": [-23.5505, -46.6333],
        "Cairo": [30.0444, 31.2357],
        "Alexandria": [31.2156, 29.9553],
        "San Francisco": [37.7749, -122.4194],
        "Seattle": [47.6062, -122.3321],
        "Boston": [42.3601, -71.0589],
        "Chicago": [41.8781, -87.6298],
        "Bangkok": [13.7563, 100.5018],
        "Phuket": [7.8804, 98.3923],
        "Hong Kong": [22.3193, 114.1694],
        "Singapore": [1.3521, 103.8198],
        "Istanbul": [41.0082, 28.9784],
        "Ankara": [39.9208, 32.8541],
        "Toronto": [43.651070, -79.347015],
        "Vancouver": [49.2827, -123.1207],
        "Cape Town": [-33.9249, 18.4241],
        "Johannesburg": [-26.2041, 28.0473],
        "Lagos": [6.5244, 3.3792],
        "Abuja": [9.0765, 7.3986],
        "Kuala Lumpur": [3.1390, 101.6869],
        "Jakarta": [-6.2088, 106.8456],
    };

    let currentRoute;

    // Funkcja do rysowania trasy
    function drawRoute(from, to) {
        if (currentRoute) {
            map.removeLayer(currentRoute);
        }

        const fromCoords = cities[from];
        const toCoords = cities[to];

        if (!fromCoords || !toCoords) {
            alert("Nie znaleziono współrzędnych dla wybranego miasta.");
            return;
        }

        currentRoute = L.polyline([fromCoords, toCoords], { color: "red" }).addTo(map);
        map.fitBounds(currentRoute.getBounds());

        const distance = calculateDistance(fromCoords, toCoords);
        const estimatedTime = calculateFlightTime(distance);
        alert(`Odległość: ${distance.toFixed(2)} km\nPrzewidywany czas lotu: ${estimatedTime.toFixed(2)} godzin`);
    }

    // Funkcja do obliczania odległości między dwoma punktami (w km)
    function calculateDistance(from, to) {
        const R = 6371; // Promień Ziemi w km
        const dLat = (to[0] - from[0]) * (Math.PI / 180);
        const dLon = (to[1] - from[1]) * (Math.PI / 180);

        const lat1 = from[0] * (Math.PI / 180);
        const lat2 = to[0] * (Math.PI / 180);

        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    // Funkcja do obliczania przewidywanego czasu lotu (zakładając średnią prędkość 800 km/h)
    function calculateFlightTime(distance) {
        const averageSpeed = 800; // km/h
        return distance / averageSpeed;
    }

    // Obsługa kliknięcia w tabeli
    const flightRows = document.querySelectorAll(".flight-row");
    flightRows.forEach((row) => {
        row.addEventListener("click", function () {
            const from = row.getAttribute("data-departure");
            const to = row.getAttribute("data-arrival");
            drawRoute(from, to);
        });
    });
});
