from flask import Flask, render_template
from flask_socketio import SocketIO
import Adafruit_DHT
import eventlet
import time

# Enable cooperative threading
eventlet.monkey_patch()

# Flask app and SocketIO setup
app = Flask(__name__)
socketio = SocketIO(app)

# DHT11 sensor setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Use your GPIO pin here

@app.route('/')
def index():
    return render_template('index.html') 

# Background task to read from DHT11 and emit data
def read_dht_sensor():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            socketio.emit('sensor_data', {
                'temp': round(temperature, 1),
                'humidity': round(humidity, 1)
            })
        else:
            print("Failed to retrieve data from DHT11 sensor")
        time.sleep(2)

# Start background thread when client connects
@socketio.on('connect')
def on_connect():
    print("Client connected.")
    socketio.start_background_task(read_dht_sensor)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
