import arrow
import requests


def get_api_temperature():
    # Get first hour of today
    start = arrow.utcnow()

    # Get last hour of today
    end = arrow.utcnow()

    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': 58.7984,
            'lng': 17.8081,
            'params': ','.join(['waveHeight', 'airTemperature']),
            'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            'end': end.to('UTC').timestamp(),  # Convert to UTC timestamp
            'source': "noaa"
        },
        headers={
            'Authorization': '4be6d91a-4583-11ec-b6c4-0242ac130002-4be6d9b0-4583-11ec-b6c4-0242ac130002'
        }
    )

    json_data = response.json()
    return json_data
