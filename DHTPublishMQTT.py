import paho.mqtt.client as mqtt
import board
import adafruit_dht
import time
import sys

# DHT11 Configuration
dht = None

try:
    # Initialize DHT11 on GPIO4
    dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)
except Exception as e:
    print(f"Failed to initialize DHT sensor: {e}")
    sys.exit(1)

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_TOPIC = "iot/dht"

# Updated callback for MQTT Client (API v2)
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message {mid} published.")

# Create MQTT client with callback API version 2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()  # Start the loop in a separate thread
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    if dht:
        dht.exit()
    sys.exit(1)

print("Starting sensor readings...")

try:
    while True:
        try:
            # Read from sensor
            temperature = dht.temperature
            humidity = dht.humidity
            
            if humidity is not None and temperature is not None:
                payload = f"{temperature:.1f},{humidity:.1f}"
                result = client.publish(MQTT_TOPIC, payload)
                
                if result.rc == 0:
                    print(f"Sent: Temperature={temperature:.1f}°C, Humidity={humidity:.1f}%")
                else:
                    print(f"Failed to send message, error code: {result.rc}")
            else:
                print("Sensor reading is None - retrying...")
                
        except RuntimeError as e:
            # DHT sensors can be unreliable, this is normal
            print(f"Sensor reading error (this is normal): {e.args[0]}")
            continue
        except Exception as e:
            print(f"Unexpected error reading sensor: {e}")
            
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    # Clean shutdown
    client.loop_stop()
    client.disconnect()
    if dht:
        dht.exit()
    print("Cleanup complete")
