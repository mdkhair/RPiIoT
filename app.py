from flask import Flask, render_template
from flask_socketio import SocketIO
import board
import adafruit_dht
import eventlet
import time

# Enable cooperative threading
eventlet.monkey_patch()

# Flask app and SocketIO setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# DHT11 sensor setup with new library
dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO4

@app.route('/')
def index():
    return render_template('index.html')

# Background task to read from DHT11 and emit data
def read_dht_sensor():
    while True:
        try:
            # Read temperature and humidity
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            if temperature is not None and humidity is not None:
                socketio.emit('sensor_data', {
                    'temp': round(temperature, 1),
                    'humidity': round(humidity, 1)
                })
                print("Temp: {:.1f}C, Humidity: {:.1f}%".format(temperature, humidity))
            else:
                print("Sensor reading was None")
                
        except RuntimeError as error:
            # DHT sensors can be finicky, continue on errors
            print("Reading error: {}".format(error.args[0]))
        except Exception as error:
            print("Unexpected error: {}".format(error))
            dhtDevice.exit()
            raise error
            
        socketio.sleep(2)  # Use socketio.sleep for better async handling

# Start background thread when client connects
@socketio.on('connect')
def on_connect():
    print("Client connected.")
    # Only start one background task
    if not hasattr(app, 'dht_task_started'):
        app.dht_task_started = True
        socketio.start_background_task(read_dht_sensor)

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected.")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
