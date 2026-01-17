# Smart Street Light Monitoring System

This project is a real-time, cloud-integrated solution for smart urban lighting. It uses a **NodeMCU ESP32** to monitor environmental light levels and provide manual control, sending all data to **Google Cloud Platform (GCP)** for storage and live visualization.

---

## 🌟 Overview
In modern urban infrastructure, energy efficiency is key. This system automates street lights using a **Light Dependent Resistor (LDR)** sensor to detect ambient light intensity. It also includes a **Manual Override** feature via a physical push button, allowing operators to turn the light on regardless of environmental conditions for maintenance or emergencies.



### **How it works:**
* **Automation:** The system monitors light intensity. If it falls below the threshold of **750**, the LED "street light" turns ON.
* **Manual Control:** Pressing the physical button will turn the LED ON even if it is bright outside.
* **Cloud Logging:** Data is sent every **5 seconds** via **MQTT** from the ESP32 to a GCP Virtual Machine.
* **Storage & UI:** Telemetry is stored in **Google BigQuery** and visualized on a live **Streamlit** dashboard.

---

## 📂 Repository Structure

* `Assignment2.ino`: Firmware for the NodeMCU ESP32 (Sensing & MQTT Publishing).
* `data.py`: The Gateway/Bridge script that receives MQTT data on the VM and streams it to BigQuery.
* `app.py`: The Streamlit web application for real-time monitoring.

---

## 🛠️ Setup Instructions

### **1. Hardware Configuration**
1. Connect an **LDR** to Analog Pin **34**.
2. Connect a **Push Button** to Digital Pin **12**.
3. Connect an **LED** to Digital Pin **13**.
4. Update the Wi-Fi credentials in `Assignment2.ino` and upload it to your ESP32.

### **2. Google Cloud Setup**
1. Create a **BigQuery** dataset named `iot_data` and a table named `sensor_logs`.
2. Set up a **Service Account** with `BigQuery Data Editor` and `BigQuery User` roles.
3. Download your JSON key and place it on your VM. **(Important: Do not upload this key to GitHub for security reasons)**.

### **3. Running the Application**
1. Activate your virtual environment on the VM: `source ~/iot_env/bin/activate`
2. Start the bridge script to listen for ESP32 data: `python3 data.py`
3. Start the dashboard: `streamlit run app.py --server.port 8501 --server.address 0.0.0.0`

---

## 🔒 Security
Data security is handled via **Identity and Access Management (IAM)** and encrypted API calls to BigQuery. The system utilizes a secure JSON key for authentication and firewall rules to restrict network access to the MQTT broker and the web dashboard.



<img width="1918" height="1078" alt="0 (2)" <img width="1918" height="1020" alt="0" src="https://github.com/user-attachments/assets/0b39c1ee-969a-496a-843f-a1ec4ddb32b2" />
src="https://github.com/user-attachments/assets/b956b610-5364-4b25-be6c-e644009a48fa" /><img width="1908" height="1013" alt="0 (1)" src="https://github.com/user-attachments/assets/25357870-5a00-405e-b16e-10bbc2e836c3" />



