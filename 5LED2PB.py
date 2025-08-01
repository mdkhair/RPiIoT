import RPi.GPIO as GPIO

# ===== GPIO PIN SETUP =====
buttonA = 5  # Button to increment
buttonB = 6  # Button to decrement
led_pins = [17, 18, 27, 22, 23]  # LEDs from 1 to 5

# ===== INITIALIZATION =====
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup LED pins
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setup button pins
GPIO.setup(buttonA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ===== STATE VARIABLES =====
current_index = -1  # -1 means all LEDs are off
buttonA_pressed = False
buttonB_pressed = False

# ===== HELPER FUNCTION =====
def update_leds(index):
    for i, pin in enumerate(led_pins):
        GPIO.output(pin, GPIO.HIGH if i == index else GPIO.LOW)

# ===== MAIN LOOP =====
try:
    while True:
        # Handle Button A (increment)
        if GPIO.input(buttonA) == GPIO.LOW:
            if not buttonA_pressed:
                if current_index < len(led_pins) - 1:
                    current_index += 1
                    update_leds(current_index)
                    print(f"LED {current_index + 1} ON")
                buttonA_pressed = True
        else:
            buttonA_pressed = False

        # Handle Button B (decrement)
        if GPIO.input(buttonB) == GPIO.LOW:
            if not buttonB_pressed:
                if current_index > -1:
                    current_index -= 1
                    update_leds(current_index)
                    if current_index >= 0:
                        print(f"LED {current_index + 1} ON")
                    else:
                        print("All LEDs OFF")
                buttonB_pressed = True
        else:
            buttonB_pressed = False

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    GPIO.cleanup()
