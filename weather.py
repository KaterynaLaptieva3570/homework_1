from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "AD5ZDK96SSRHNKALGAWPEYDR9"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
API_TOKEN = "123"  

def authenticate_token(token):
    return token == API_TOKEN

def get_weather(requester_name, location, date):
    url = base_url
    headers = {
        'X-Api-Key': API_KEY
    }
    params = {
        'location': location,
        'date': date,
        'unitGroup': 'metric',
        'key': API_KEY,
        'contentType': 'json'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == requests.codes.ok:
        weather_data = response.json()
        formatted_weather = {
            "requester_name": requester_name,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "location": f"{location}",
            "date": date,
            "weather": {
                "temp_c": weather_data['days'][0]['tempmax'],
                "wind_kph": weather_data['days'][0]['windspeed'],
                "pressure_mb": weather_data['days'][0]['pressure'],
                "humidity": weather_data['days'][0]['humidity']
            }
        }
        return formatted_weather
    else:
        return None

@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    token = data.get('token')
    name = data.get('name')
    location = data.get('location')
    date = data.get('date')

    if not token or not authenticate_token(token):
        return jsonify({"error": "Invalid or missing token."}), 401

    if not name or not location or not date:
        return jsonify({"error": "Name, location, and date are required."}), 400

    weather_info = get_weather(name, location, date)
    if weather_info:
        return jsonify(weather_info), 200
    else:
        return jsonify({"error": "Failed to retrieve weather information."}), 500

