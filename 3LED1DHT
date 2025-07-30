import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# ========== SETUP ==========
# DHT11 sensor on GPIO4
dht = adafruit_dht.DHT11(board.D4)

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# LED pins
LED_GREEN = 17
LED_YELLOW = 27
LED_RED = 22

# Setup LED pins as output
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

def show_temperature_status(temp):
    # Reset all LEDs first
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_YELLOW, GPIO.LOW)
    GPIO.output(LED_RED, GPIO.LOW)

    if temp < 28:
        GPIO.output(LED_GREEN, GPIO.HIGH)
        print(f"Temperature: {temp}°C - Normal (Green)")
    elif 28 <= temp < 32:
        GPIO.output(LED_YELLOW, GPIO.HIGH)
        print(f"Temperature: {temp}°C - Warning (Yellow)")
    else:
        GPIO.output(LED_RED, GPIO.HIGH)
        print(f"Temperature: {temp}°C - High Alert (Red)")

# ========== MAIN LOOP ==========
try:
    while True:
        try:
            temperature = dht.temperature
            if temperature is not None:
                show_temperature_status(temperature)
            else:
                print("Sensor reading failed.")
        except RuntimeError as e:
            print(f"Runtime error: {e.args[0]}")

        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    GPIO.cleanup()
