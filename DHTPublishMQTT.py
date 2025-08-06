#!/usr/bin/env python3
# Publish DHT11 readings over MQTT (ASCII-only version)

import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import warnings

# Suppress the Paho-MQTT deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Sensor on GPIO17 -------------------------------------------------
dht = adafruit_dht.DHT11(board.D17)      # BCM pin 17, physical pin 11

# --- MQTT broker settings --------------------------------------------
MQTT_BROKER = "localhost"                # or the broker IP
MQTT_TOPIC  = "iot/dht"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.V5
)
client.connect(MQTT_BROKER, 1883, 60)

# --- Main loop --------------------------------------------------------
while True:
    try:
        temp_c = dht.temperature
        hum_pc = dht.humidity
        if temp_c is not None and hum_pc is not None:
            payload = "{:.1f},{:.1f}".format(temp_c, hum_pc)
            client.publish(MQTT_TOPIC, payload)
            print("Sent:", payload)
        else:
            print("Sensor returned None")
    except RuntimeError as err:
        # Retryable DHT errors
        print("Sensor error:", err)
    except Exception as err:
        # Fatal errors (wrong pin, permissions, etc.)
        print("Fatal error:", err)
        raise
    time.sleep(2)
