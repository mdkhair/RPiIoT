import blynklib
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# === Blynk Setup ===
BLYNK_AUTH = 'YOUR_BLYNK_AUTH_TOKEN'  # Replace with your actual token
blynk = blynklib.Blynk(BLYNK_AUTH)

# === GPIO Setup ===
LED_PIN = 17       # GPIO17
BUTTON_PIN = 18    # GPIO18
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4        # GPIO4 for DHT11

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(LED_PIN, GPIO.LOW)

# === Virtual Button Handler ===
@blynk.handle_event('write V2')
def blynk_led_control(pin, value):
    if value[0] == '1':
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED ON (via Blynk)")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED OFF (via Blynk)")
    
    sync_led_to_blynk()

# === LED Feedback to Blynk ===
def sync_led_to_blynk():
    state = GPIO.input(LED_PIN)
    blynk.virtual_write(3, state)       # V3 = LED widget
    blynk.virtual_write(2, state)       # V2 = Sync switch

# === Send DHT11 Sensor Data ===
def send_dht_data():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temp: {temperature:.1f}°C |  Humidity: {humidity:.1f}%")
        blynk.virtual_write(0, temperature)  # V0 = Temp
        blynk.virtual_write(1, humidity)     # V1 = Humidity

# === Main Loop ===
prev_button_state = False

while True:
    blynk.run()

    # Detect button press/release
    button_state = GPIO.input(BUTTON_PIN)
    if button_state and not prev_button_state:
        print("Button Pressed - LED ON")
        GPIO.output(LED_PIN, GPIO.HIGH)
        sync_led_to_blynk()

    elif not button_state and prev_button_state:
        print("Button Released - LED OFF")
        GPIO.output(LED_PIN, GPIO.LOW)
        sync_led_to_blynk()

    prev_button_state = button_state

    # Send sensor data periodically
    send_dht_data()
    time.sleep(2)
