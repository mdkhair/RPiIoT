import blynklib
import board
import adafruit_dht
import RPi.GPIO as GPIO
import time

# === Setup ===
BLYNK_AUTH = 'YOUR_BLYNK_AUTH_TOKEN'  # Replace with your token
blynk = blynklib.Blynk(BLYNK_AUTH)

# DHT11 Configuration
dht = adafruit_dht.DHT11(board.D4)  # GPIO4

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
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        
        if humidity is not None and temperature is not None:
            blynk.virtual_write(0, temperature)  # V0 = Temperature
            blynk.virtual_write(1, humidity)     # V1 = Humidity
            print(f"🌡️ Temp: {temperature:.1f}°C | 💧 Humidity: {humidity:.1f}%")
        else:
            print("❌ Sensor reading is None")
            
    except RuntimeError as e:
        print(f"❌ DHT sensor error: {e.args[0]}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# === Main Loop ===
try:
    while True:
        blynk.run()
        send_dht_data()
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n👋 Program stopped")
    GPIO.cleanup()
    dht.exit()
