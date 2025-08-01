import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

LED_PIN = 17  # BCM numbering

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# MQTT Callback when message received
def on_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"Received: {payload}")
    if payload.lower() == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED ON")
    elif payload.lower() == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED OFF")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("iot/led")

client.on_message = on_message

print("Listening for MQTT messages on topic 'iot/led'...")
client.loop_forever()
