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

# Register virtual pin handler
@blynk.on("V{}".format(LED_VPIN))
def v0_write_handler(value):
    """
    Handler for virtual pin V0
    value[0] will be '1' for ON and '0' for OFF
    """
    if int(value[0]) == 1:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")

# Optional: Send LED status to Blynk app
@blynk.on("connected")
def blynk_connected():
    """
    Sync virtual pins when connected
    """
    print("Raspberry Pi connected to Blynk!")
    # You can sync the current LED state if needed
    # blynk.sync_virtual(LED_VPIN)

@blynk.on("disconnected")
def blynk_disconnected():
    """
    Handle disconnection
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
