import RPi.GPIO as GPIO

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    if message.lower() == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED ON")
    elif message.lower() == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED OFF")

client.subscribe("iot/led")
client.on_message = on_message
client.loop_start()
