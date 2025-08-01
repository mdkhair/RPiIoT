import paho.mqtt.client as mqtt
import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
MQTT_BROKER = "localhost"
MQTT_TOPIC = "iot/dht"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        payload = f"{temperature:.1f},{humidity:.1f}"
        client.publish(MQTT_TOPIC, payload)
        print(f"Sent: {payload}")
    time.sleep(2)
