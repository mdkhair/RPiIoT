from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import board
import adafruit_dht
from threading import Thread
import time

# Flask app setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# DHT11 sensor setup
dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO4

# Global variable to control the background thread
sensor_thread = None
thread_running = False

@app.route('/')
def index():
    return render_template('index.html')

def read_sensor_data():
    """Background thread function to read sensor data"""
    global thread_running
    while thread_running:
        try:
            # Read temperature and humidity
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            if temperature is not None and humidity is not None:
                # Emit data to all connected clients
                socketio.emit('sensor_data', {
                    'temp': round(temperature, 1),
                    'humidity': round(humidity, 1)
                })
                print("Temp: {:.1f}C, Humidity: {:.1f}%".format(temperature, humidity))
            else:
                print("Sensor reading was None")
                
        except RuntimeError as error:
            print("Reading error: {}".format(error.args[0]))
        except Exception as error:
            print("Unexpected error: {}".format(error))
            
        time.sleep(2)

@socketio.on('connect')
def handle_connect():
    global sensor_thread, thread_running
    print("Client connected")
    
    # Start the background thread if it's not running
    if sensor_thread is None or not sensor_thread.is_alive():
        thread_running = True
        sensor_thread = Thread(target=read_sensor_data)
        sensor_thread.daemon = True
        sensor_thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        thread_running = False
        if dhtDevice:
            dhtDevice.exit()
        print("\nProgram stopped")
