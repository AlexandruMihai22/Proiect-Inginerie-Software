from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from threading import Thread

import eventlet
import json
import time

import db
import auth
import temperature
import temperature_api
import watering
import wateringIntervals
# import status
# import status_api


# Necessary monkey-patch


eventlet.monkey_patch()

app: Flask
mqtt: Mqtt
socketio: SocketIO
thread = None


def create_app() -> Flask:
    global app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    @app.route('/')
    def hello_world():
        # Here I chose to start the periodic publishing after the root endpoint is called.
        # It's not the best nor cleanest approach, but will have to refactor it.
        # What is important is that the background_thread function is called on
        # a separate thread, so that publishing can happen while simultaneously
        # HTTP endpoints are also functional.

        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
        return "Hello World!"

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(temperature.bp)
    app.register_blueprint(watering.bp)
    app.register_blueprint(wateringIntervals.bp)

    return app


def create_mqtt_app() -> Mqtt:
    global mqtt, socketio

    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    mqtt = Mqtt(app)
    socketio = SocketIO(app, async_mode="eventlet")

    return mqtt


# Start MQTT publishing

# Function that every second publishes a message
def background_thread():
    # count = 0
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps(temperature_api.get_api_temperature(), default=str)
        # Publish
        mqtt.publish('python/mqtt', str.encode(message))


# App will now have to be run with `python app.py` as flask is now wrapped in socketio.
# The following makes sure that socketio is also used
def run_socketio_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)


if __name__ == '__main__':
    run_socketio_app()
