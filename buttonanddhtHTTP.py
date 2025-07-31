from flask import Flask, render_template, jsonify, request
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# DHT11 Setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# LED Setup
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Read sensor
def read_sensor():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return round(temperature, 1), round(humidity, 1)

@app.route('/')
def index():
    return render_template('rest.html')

@app.route('/sensor')
def sensor_data():
    temp, hum = read_sensor()

    # Auto control LED based on temperature
    if temp >= 30:
        GPIO.output(LED_PIN, GPIO.HIGH)
        status = 'ON (Hot)'
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        status = 'OFF (Cool)'

    return jsonify(temp=temp, humidity=hum, led=status)

@app.route('/led/<state>')
def manual_led(state):
    if state == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        return 'LED turned ON manually'
    elif state == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        return 'LED turned OFF manually'
    else:
        return 'Invalid command', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
