#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// 1. Wi-Fi and MQTT Configuration
const char* ssid = "cs-mtg-room";
const char* password = "bilik703";
const char* mqtt_server = "136.111.182.54"; // Your GCP VM Public IP

// 2. Pin Definitions
const int ldrPin = 34;    // Analog pin for LDR
const int buttonPin = 12; // Digital pin for Button
const int ledPin = 13;    // Digital pin for LED street light

// 3. System Constants
const int THRESHOLD = 750; 

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32_StreetLight_Node")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // Using internal pullup for the button
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 5000) { // Send data every 5 seconds
    lastMsg = now;

    // Read Sensors
    int ldrValue = analogRead(ldrPin);
    bool buttonPressed = (digitalRead(buttonPin) == LOW); // LOW means pressed with PULLUP

    // Smart Street Light Logic
    bool ledStatus = (ldrValue < THRESHOLD) || buttonPressed;
    
    if (ledStatus) {
      digitalWrite(ledPin, HIGH);
    } else {
      digitalWrite(ledPin, LOW);
    }

    // Create JSON Payload
    StaticJsonDocument<200> doc;
    doc["ldr_value"] = ldrValue;
    doc["button_pressed"] = buttonPressed;
    doc["led_status"] = ledStatus;

    char buffer[256];
    serializeJson(doc, buffer);

    // Publish to topic
    Serial.print("Publishing message: ");
    Serial.println(buffer);
    client.publish("iot/sensors", buffer);
  }
}
