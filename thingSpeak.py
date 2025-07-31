import time
import requests
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

THINGSPEAK_API_KEY = 'YOUR_WRITE_API_KEY_HERE'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        payload = {
            'api_key': THINGSPEAK_API_KEY,
            'field1': temperature,
            'field2': humidity
        }
        try:
            response = requests.post(THINGSPEAK_URL, params=payload, timeout=5)
            print(f"Sent -> Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}% | Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending to ThingSpeak: {e}")
    else:
        print("❗ Sensor read failed")

    time.sleep(15)  # Must wait at least 15s between uploads (ThingSpeak limit)
