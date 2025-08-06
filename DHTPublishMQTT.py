import paho.mqtt.client as mqtt
import board
import adafruit_dht
import time

# DHT11 Configuration
dht = adafruit_dht.DHT11(board.D4)  # GPIO4

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_TOPIC = "iot/dht"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        
        if humidity is not None and temperature is not None:
            payload = f"{temperature:.1f},{humidity:.1f}"
            client.publish(MQTT_TOPIC, payload)
            print(f"Sent: {payload}")
        else:
            print("Sensor reading is None")
            
    except RuntimeError as e:
        print(f"Sensor error: {e.args[0]}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(2)
