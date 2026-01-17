#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from google.cloud import bigquery
import json
import os
import time

# 1. Google Cloud Configuration
# Replace the path below with your actual key file path if needed
KEY_PATH = "/home/nitiyahselvan2003/cpc357-484615-990d2cd74b3b.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

PROJECT_ID = "cpc357-484615"
DATASET_ID = "iot_data"
TABLE_ID = "sensor_logs"

# 2. Initialize BigQuery Client
client_bq = bigquery.Client(project=PROJECT_ID, location="US")
table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# 3. MQTT Callback: This runs whenever data is received from the ESP32
def on_message(client, userdata, message):
    try:
        # Decode the JSON payload from the ESP32 hardware
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)
        
        # Add a server-side timestamp for accurate logging
        data["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert the actual hardware data into BigQuery
        errors = client_bq.insert_rows_json(table_id, [data])
        
        if not errors:
            print(f"Hardware Data Forwarded: LDR={data['ldr_value']} | "
                  f"Button={data['button_pressed']} | LED={data['led_status']}")
        else:
            print(f"BigQuery Ingestion Error: {errors}")
            
    except Exception as e:
        print(f"Error processing message: {e}")

# 4. MQTT Connection Callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the topic your ESP32 is publishing to
        client.subscribe("iot/sensors")
    else:
        print(f"Connection failed with code {rc}")

# 5. Main Execution Logic
# Initialize the MQTT client using the Version 1 API
client_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

# Connect to the local broker on the VM
print("Starting Data Bridge... Waiting for ESP32 data.")
client_mqtt.connect("localhost", 1883, 60)

# Keep the script running to listen for incoming hardware messages
client_mqtt.loop_forever()