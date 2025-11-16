import requests
import json
import random
import time
from datetime import datetime, timezone
import pyodbc

# -------------------------
# CONFIGURATION
# -------------------------

POWER_BI_URL = "https://api.powerbi.com/beta/2082de46-1afa-4b64-a440-6558f80e9840/datasets/12ca1e37-95a7-4ce1-826f-c2141c2fc60c/rows?experience=power-bi&key=pDybOBTaxgs0lT9qRqZem4A%2FUzTzqr4NVshzAZA%2F7AKcQ1OIgwnR8mqe5RJccnliXpAQQAVgK%2B%2B59y2f9LqVcA%3D%3D"  # <-- paste full push URL

SQL_CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-OQDQ9FN;"
    "Database=DepiProject;"
    "Trusted_Connection=yes;"
)

DEVICE_ID = "Sensor_102"
DEVICE_TYPE = "Temperature"
LOCATION = "Plant 3 - Line B"
ZONE = "Packaging"


# -------------------------
# SQL Connection
# -------------------------

connection = pyodbc.connect(SQL_CONN_STR)
cursor = connection.cursor()

# Create table if not exists
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='IoT_Streaming' AND xtype='U')
CREATE TABLE IoT_Streaming (
    Timestamp datetime,
    DeviceID nvarchar(100),
    DeviceType nvarchar(100),
    Location nvarchar(100),
    Zone nvarchar(100),
    DeviceStatus nvarchar(50),
    Temperature_C float,
    Humidity_pct float,
    Vibration_mms float,
    Power_Watts float,
    AlertLevel int,
    AlertType nvarchar(100)
)
""")
connection.commit()


# -------------------------
# FUNCTION: Generate Fake IoT Data
# -------------------------

def generate_iot_record():
    temp = round(random.uniform(25, 80), 2)
    
    alert_level = 0
    alert_type = ""

    if temp > 70:
        alert_level = 2
        alert_type = "Overheating"
    elif temp > 55:
        alert_level = 1
        alert_type = "High Temperature"

    return {
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "DeviceID": DEVICE_ID,
        "DeviceType": DEVICE_TYPE,
        "Location": LOCATION,
        "Zone": ZONE,
        "DeviceStatus": "Running" if alert_level < 2 else "Warning",
        "Temperature_C": temp,
        "Humidity_pct": round(random.uniform(30, 60), 2),
        "Vibration_mms": round(random.uniform(1.0, 6.0), 2),
        "Power_Watts": round(random.uniform(180, 260), 2),
        "AlertLevel": alert_level,
        "AlertType": alert_type
    }


# -------------------------
# MAIN LOOP
# -------------------------

print("Starting IoT Stream... Press CTRL + C to stop.")

while True:
    # Generate reading
    record = generate_iot_record()

    # SEND TO POWER BI
    requests.post(POWER_BI_URL, json=[record])

    # INSERT INTO SQL
    cursor.execute("""
        INSERT INTO IoT_Streaming VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, 
        record["Timestamp"],
        record["DeviceID"],
        record["DeviceType"],
        record["Location"],
        record["Zone"],
        record["DeviceStatus"],
        record["Temperature_C"],
        record["Humidity_pct"],
        record["Vibration_mms"],
        record["Power_Watts"],
        record["AlertLevel"],
        record["AlertType"]
    )
    connection.commit()

    print(f"Sent: {record}")
    
    time.sleep(2)  # frequency of streaming