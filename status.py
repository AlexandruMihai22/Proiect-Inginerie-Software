from db import get_db
from weather import get_humidity_from_weather_api, get_precipitation_from_weather_api


def get_ideal_parameters(humidity, precipitation, soil_moisture, system_temperature):
    ideal_temperature = 20
    ideal_moisture = 50
    if precipitation is None:
        precipitation = 0
    if soil_moisture is None or soil_moisture >= ideal_moisture or precipitation > 4:
        return 0.0
    water_quantity = (ideal_moisture - soil_moisture) * 100
    if system_temperature and (system_temperature - ideal_temperature > 5):
        water_quantity += 50
    if humidity and humidity < 100:
        water_quantity += 50

    return water_quantity


def get_status():
    soil_moisture = get_db().execute(
        'SELECT id, timestamp, value FROM soil_moisture ORDER BY timestamp DESC'
    ).fetchone()

    if soil_moisture:
        soil_moisture = soil_moisture['value']

    system_temperature = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if system_temperature:
        system_temperature = system_temperature['value']

    humidity = get_humidity_from_weather_api()['data']['humidity']
    precipitation = get_precipitation_from_weather_api()['data']['precipitation']

    water_quantity = get_ideal_parameters(humidity, precipitation, soil_moisture, system_temperature)

    if water_quantity:
        db = get_db()
        db.execute(
            'INSERT INTO watering (water_quantity) VALUES (?)',
            water_quantity
        )
        db.commit()
    else:
        water_quantity = 0.0
    return {
        'status': 'The plant was successfully watered',
        'data': {
            'water_quantity': water_quantity
            }
        }
