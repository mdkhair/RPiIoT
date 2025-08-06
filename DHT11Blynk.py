import blynklib
import board
import adafruit_dht
import time

# === Blynk Setup ===
BLYNK_AUTH = 'YOUR_BLYNK_AUTH_TOKEN'  # Replace with your actual token
blynk = blynklib.Blynk(BLYNK_AUTH)

# === DHT11 Sensor Setup ===
dht = adafruit_dht.DHT11(board.D4)  # GPIO4

# === Send sensor data every 5 seconds ===
def read_and_send():
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        
        if humidity is not None and temperature is not None:
            print(f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
            blynk.virtual_write(0, temperature)  # V0 = Temp
            blynk.virtual_write(1, humidity)     # V1 = Humidity
        else:
            print("Sensor reading is None. Retrying...")
            
    except RuntimeError as e:
        print(f"Sensor error: {e.args[0]}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# === Main Loop ===
while True:
    blynk.run()      # Keep connection alive
    read_and_send()  # Read sensor and send
    time.sleep(5)    # Wait 5 seconds (don't overload)
