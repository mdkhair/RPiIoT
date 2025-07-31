from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
import random
import time

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Background task to emit data every 2 seconds
def generate_sensor_data():
    while True:
        temp = round(random.uniform(25, 35), 2)
        humidity = round(random.uniform(40, 60), 2)
        socketio.emit('sensor_data', {'temp': temp, 'humidity': humidity})
        time.sleep(2)

# Start background thread after server starts
@socketio.on('connect')
def connected():
    print("Client connected.")
    socketio.start_background_task(generate_sensor_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
 
