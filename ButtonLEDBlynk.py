#!/usr/bin/env python3
"""
Raspberry Pi LED Control with Blynk IoT
Control an LED connected to your Raspberry Pi using the Blynk app
Using blynklib package
"""

import blynklib
import RPi.GPIO as GPIO
import time

# Blynk Authentication Token
# Get this from the Blynk App project settings
BLYNK_AUTH = 'YOUR_AUTH_TOKEN_HERE'

# GPIO pin where LED is connected
LED_PIN = 17  # GPIO17 (Physical pin 11)

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Start with LED off

# Virtual Pin for LED control (V0 in Blynk app)
LED_VPIN = 0

# Register virtual pin handler for V0
@blynk.handle_event('write V{}'.format(LED_VPIN))
def write_virtual_pin_handler(pin, value):
    """
    Handler for virtual pin V0
    value[0] will be '1' for ON and '0' for OFF
    """
    print(f"V{pin} value: {value}")
    
    if int(value[0]) == 1:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")
        # Optional: Send confirmation back to app
        blynk.virtual_write(LED_VPIN, 1)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")
        # Optional: Send confirmation back to app
        blynk.virtual_write(LED_VPIN, 0)

# Optional: Read handler if you want to sync state
@blynk.handle_event('read V{}'.format(LED_VPIN))
def read_virtual_pin_handler(pin):
    """
    Handler for reading virtual pin V0
    """
    # Read current LED state
    led_state = GPIO.input(LED_PIN)
    blynk.virtual_write(pin, led_state)
    print(f"Read V{pin}, LED state: {led_state}")

# Connection handler
@blynk.handle_event("connect")
def connect_handler():
    """
    Called when connected to Blynk
    """
    print("Connected to Blynk!")
    # Sync current LED state with app
    led_state = GPIO.input(LED_PIN)
    blynk.virtual_write(LED_VPIN, led_state)

# Disconnection handler
@blynk.handle_event("disconnect")
def disconnect_handler():
    """
    Called when disconnected from Blynk
    """
    print("Disconnected from Blynk")

def main():
    """
    Main loop
    """
    print("Starting Blynk LED Control...")
    print(f"LED connected to GPIO{LED_PIN}")
    print("Connecting to Blynk...")
    
    try:
        while True:
            blynk.run()
            # You can add other non-blocking code here if needed
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup GPIO on exit
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()
