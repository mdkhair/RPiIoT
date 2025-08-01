import blynklib
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# === Setup ===
BLYNK_AUTH = 'YOUR_BLYNK_AUTH_TOKEN'  # Replace with your token
blynk = blynklib.Blynk(BLYNK_AUTH)

# DHT11 Configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO4

# LED Configuration
LED_PIN = 17  # GPIO17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Virtual pin handler: Button control from Blynk
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    if value[0] == '1':
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("💡 LED ON (via Blynk)")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("💡 LED OFF (via Blynk)")

# Function to send DHT11 data to Blynk
def send_dht_data():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        blynk.virtual_write(0, temperature)  # V0 = Temperature
        blynk.virtual_write(1, humidity)     # V1 = Humidity
        print(f"🌡️ Temp: {temperature:.1f}°C | 💧 Humidity: {humidity:.1f}%")
    else:
        print("❌ Failed to read from DHT11 sensor")

# === Main Loop ===
while True:
    blynk.run()
    send_dht_data()
    time.sleep(5)
