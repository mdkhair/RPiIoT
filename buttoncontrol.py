from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO

app = Flask(__name__)
socketio = SocketIO(app)

# GPIO Setup
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

@app.route('/')
def index():
    return render_template('button.html')

# Handle message from client (e.g., button press)
@socketio.on('led_control')
def handle_led(data):
    if data == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")
    elif data == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
