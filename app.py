import streamlit as st
from google.cloud import bigquery
import os

# Use your uploaded key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/nitiyahselvan2003/cpc357-484615-990d2cd74b3b.json"

st.title("💡 Smart Street Light Monitoring")

# Connect to BigQuery
client = bigquery.Client(project="cpc357-484615", location="US")

# Fetch latest data
query = "SELECT * FROM `cpc357-484615.iot_data.sensor_logs` ORDER BY timestamp DESC LIMIT 20"
df = client.query(query).to_dataframe()

# Display Latest Status
latest = df.iloc[0]
col1, col2, col3 = st.columns(3)
col1.metric("LDR Value", latest['ldr_value'])
col2.metric("Button Pressed", "Yes" if latest['button_pressed'] else "No")
col3.metric("LED Status", "ON" if latest['led_status'] else "OFF")

# Plot LDR Trend
st.subheader("Light Intensity Over Time")
st.line_chart(df.set_index('timestamp')['ldr_value'])