import blynklib
import Adafruit_DHT
import time

# === Blynk Setup ===
BLYNK_AUTH = 'YOUR_BLYNK_AUTH_TOKEN'  # Replace with your actual token
blynk = blynklib.Blynk(BLYNK_AUTH)

# === DHT11 Sensor Setup ===
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO4

# === Send sensor data every 5 seconds ===
def read_and_send():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        blynk.virtual_write(0, temperature)  # V0 = Temp
        blynk.virtual_write(1, humidity)     # V1 = Humidity
    else:
        print("Sensor failure. Check connection.")

# === Main Loop ===
while True:
    blynk.run()      # Keep connection alive
    read_and_send()  # Read sensor and send
    time.sleep(5)    # Wait 5 seconds (don’t overload)
