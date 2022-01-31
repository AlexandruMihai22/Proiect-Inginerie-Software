from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

import json
import time
import db
import auth
import watering
import wateringIntervals
import weather_bp
import system_temperature_bp
import soil_moisture_bp
import status_bp
import status

from gevent import monkey
monkey.patch_all(ssl=False)

app: Flask | None = None
mqtt: Mqtt | None = None
socketio: SocketIO | None = None
thread: Thread | None = None


def create_app(testing=False, db_path='flaskr.sqlite'):
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_PATH=db_path
    )
    app.config['TESTING'] = testing
    app.config['LOGIN_DISABLED'] = testing

    @app.route('/')
    def home():
        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
        return 'Hello World'

    if not testing:
        db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(watering.bp)
    app.register_blueprint(wateringIntervals.bp)
    app.register_blueprint(weather_bp.bp)
    app.register_blueprint(system_temperature_bp.bp)
    app.register_blueprint(soil_moisture_bp.bp)
    app.register_blueprint(status_bp.bp)

    return app


def create_mqtt_app():
    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = '127.0.0.1'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt, socketio
    mqtt = Mqtt(app)
    socketio = SocketIO(app, async_mode='eventlet')

    return mqtt


# Start MQTT publishing

# Function that every second publishes a message
def background_thread():
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps(status.get_status(), default=str)
            # Publish
            mqtt.publish('python/mqtt', str.encode(message))


# App will now have to be run with `python app.py` as flask is now wrapped in socketio.
# The following makes sure that socketio is also used

def run_socketio_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False, debug=True)


if __name__ == '__main__':
    run_socketio_app()
