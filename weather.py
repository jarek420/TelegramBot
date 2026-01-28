import requests

WEATHER_CODES = {
    0:  "☀️ Bezchmurnie",
    1:  "🌤️ Głównie słonecznie",
    2:  "⛅ Częściowe zachmurzenie",
    3:  "☁️ Pochmurno",

    45: "🌫️ Mgła",
    48: "🌫️ Mgła z szronem",

    51: "🌦️ Lekka mżawka",
    53: "🌦️ Umiarkowana mżawka",
    55: "🌧️ Intensywna mżawka",
    56: "🧊🌦️ Marznąca mżawka",
    57: "🧊🌧️ Marznąca mżawka (intensywna)",

    61: "🌧️ Lekki deszcz",
    63: "🌧️ Umiarkowany deszcz",
    65: "🌧️ Intensywny deszcz",
    66: "🧊🌧️ Marznący deszcz",
    67: "🧊🌧️ Marznący deszcz (intensywny)",

    71: "❄️ Lekki śnieg",
    73: "❄️ Umiarkowany śnieg",
    75: "❄️ Intensywny śnieg",
    77: "❄️ Ziarnisty śnieg",

    80: "🌦️ Przelotny deszcz (lekki)",
    81: "🌦️ Przelotny deszcz",
    82: "🌧️ Gwałtowne opady",

    85: "🌨️ Przelotny śnieg",
    86: "🌨️ Intensywny przelotny śnieg",

    95: "⛈️ Burza",
    96: "⛈️ Burza z gradem",
    99: "⛈️ Silna burza z gradem",
}

def decode_weather(code: int) -> str:
    return WEATHER_CODES.get(code, "❓ Nieznany warunek")

def get_weather(coordinates: list):
    lat, lon = coordinates[0], coordinates[1]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    res = requests.get(url).json()
    return res["current_weather"]

def divide_time(time):
    return time[0:10] + " " + time[11:]

def get_weather_message(coordinates: list):
    data = get_weather(coordinates)
    
    message = "        SZCZECIN      \n"
    message += divide_time(data["time"]) + "\n"
    message += str(data['temperature']) + " C\n"
    message += decode_weather(data['weathercode'])
    return message