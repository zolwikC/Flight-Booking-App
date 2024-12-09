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
    const cities = [
        { name: "Warsaw", coords: [52.2297, 21.0122] },
        { name: "Berlin", coords: [52.5200, 13.4050] },
        { name: "Paris", coords: [48.8566, 2.3522] },
        { name: "London", coords: [51.5074, -0.1278] },
        { name: "New York", coords: [40.7128, -74.0060] },
        { name: "Los Angeles", coords: [34.0522, -118.2437] },
        { name: "Madrid", coords: [40.4168, -3.7038] },
        { name: "Rome", coords: [41.9028, 12.4964] },
        { name: "Tokyo", coords: [35.6895, 139.6917] },
        { name: "Osaka", coords: [34.6937, 135.5023] },
        { name: "Barcelona", coords: [41.3851, 2.1734] },
        { name: "Amsterdam", coords: [52.3676, 4.9041] },
        { name: "Munich", coords: [48.1351, 11.5820] },
        { name: "Vienna", coords: [48.2082, 16.3738] },
        { name: "Prague", coords: [50.0755, 14.4378] },
        { name: "Moscow", coords: [55.7558, 37.6173] },
        { name: "Saint Petersburg", coords: [59.9343, 30.3351] },
        { name: "Dubai", coords: [25.276987, 55.296249] },
        { name: "Abu Dhabi", coords: [24.4539, 54.3773] },
        { name: "New Delhi", coords: [28.6139, 77.2090] },
        { name: "Mumbai", coords: [19.0760, 72.8777] },
        { name: "Sydney", coords: [-33.8688, 151.2093] },
        { name: "Melbourne", coords: [-37.8136, 144.9631] },
        { name: "Beijing", coords: [39.9042, 116.4074] },
        { name: "Shanghai", coords: [31.2304, 121.4737] },
        { name: "Rio de Janeiro", coords: [-22.9068, -43.1729] },
        { name: "Sao Paulo", coords: [-23.5505, -46.6333] },
        { name: "Cairo", coords: [30.0444, 31.2357] },
        { name: "Alexandria", coords: [31.2156, 29.9553] },
        { name: "San Francisco", coords: [37.7749, -122.4194] },
        { name: "Seattle", coords: [47.6062, -122.3321] },
        { name: "Boston", coords: [42.3601, -71.0589] },
        { name: "Chicago", coords: [41.8781, -87.6298] },
        { name: "Bangkok", coords: [13.7563, 100.5018] },
        { name: "Phuket", coords: [7.8804, 98.3923] },
        { name: "Hong Kong", coords: [22.3193, 114.1694] },
        { name: "Singapore", coords: [1.3521, 103.8198] },
        { name: "Istanbul", coords: [41.0082, 28.9784] },
        { name: "Ankara", coords: [39.9208, 32.8541] },
        { name: "Toronto", coords: [43.651070, -79.347015] },
        { name: "Vancouver", coords: [49.2827, -123.1207] },
        { name: "Cape Town", coords: [-33.9249, 18.4241] },
        { name: "Johannesburg", coords: [-26.2041, 28.0473] },
        { name: "Lagos", coords: [6.5244, 3.3792] },
        { name: "Abuja", coords: [9.0765, 7.3986] },
        { name: "Kuala Lumpur", coords: [3.1390, 101.6869] },
        { name: "Jakarta", coords: [-6.2088, 106.8456] },
    ];

    // Dodawanie markerów na mapę
    cities.forEach((city) => {
        const marker = L.marker(city.coords)
            .addTo(map)
            .bindPopup(`<b>${city.name}</b>`)
            .on("click", function () {
                handleCityClick(city.name);
            });
    });

    // Funkcja obsługująca kliknięcia na marker
    function handleCityClick(cityName) {
        const departureInput = document.getElementById("departure-city");
        const arrivalInput = document.getElementById("arrival-city");

        if (!departureInput.value) {
            departureInput.value = cityName;
        } else if (!arrivalInput.value) {
            arrivalInput.value = cityName;
        } else {
            departureInput.value = cityName;
            arrivalInput.value = "";
        }
    }

    console.log("Mapa została poprawnie załadowana z miastami.");
});
