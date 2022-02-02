import arrow
import requests
from dotenv import load_dotenv
import os
# env variables
load_dotenv()


def call_weather_api(params):
    # Get first hour of today
    start = arrow.utcnow()

    # Get last hour of today
    end = arrow.utcnow()

    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': 58.7984,
            'lng': 17.8081,
            'params': ','.join(params),
            'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            'end': end.to('UTC').timestamp(),  # Convert to UTC timestamp
            'source': "noaa"
        },
        headers={
            'Authorization': os.getenv('API_KEY')
        }
    )

    json_data = response.json()
    return json_data


def get_temperature_from_weather_api():
    json_data = call_weather_api(['airTemperature'])
    temperature = json_data['hours'][0]['airTemperature']['noaa']
    time = json_data['hours'][0]['time']
    return {
        'data': {
            'temperature': temperature,
            'time': time
        }
    }


def get_humidity_from_weather_api():
    json_data = call_weather_api(['humidity'])
    humidity = json_data['hours'][0]['humidity']['noaa']
    time = json_data['hours'][0]['time']
    return {
        'data': {
            'humidity': humidity,
            'time': time
        }
    }


def get_precipitation_from_weather_api():
    json_data = call_weather_api(['precipitation'])
    precipitation = json_data['hours'][0]['precipitation']['noaa']
    time = json_data['hours'][0]['time']
    return {
        'data': {
            'precipitation': precipitation,
            'time': time
        }
    }


# print(get_humidity_from_weather_api())
