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
MQTT_TOPIC_TEMP = "iot/dht/temperature"  # Separate topic for temperature
MQTT_TOPIC_HUM  = "iot/dht/humidity"     # Separate topic for humidity

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.connect(MQTT_BROKER, 1883, 60)

# --- Main loop --------------------------------------------------------
while True:
    try:
        temp_c = dht.temperature
        hum_pc = dht.humidity
        
        if temp_c is not None and hum_pc is not None:
            # Publish temperature and humidity to separate topics
            client.publish(MQTT_TOPIC_TEMP, str(temp_c))
            client.publish(MQTT_TOPIC_HUM, str(hum_pc))
            
            print("Sent: Temperature={:.1f}C to {}".format(temp_c, MQTT_TOPIC_TEMP))
            print("Sent: Humidity={:.1f}% to {}".format(hum_pc, MQTT_TOPIC_HUM))
            print("-" * 40)
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
