import paho.mqtt.client as mqtt
from app.database import SessionLocal
from app.models import Reading
import json


TOPICS = ["temperature", "ph", "turbidity"]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
            print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")
        
    # Subscribe to sensor topics
    for topic in TOPICS:
        topic_filter = f"sensors/+/{topic}"
        client.subscribe(topic_filter)
        print(f"Subscribed to: {topic_filter}")


def on_message(client, userdata, msg):
    """Process incoming MQTT message and save to database"""
    try:
        # Decode and parse JSON
        payload_str = msg.payload.decode('utf-8')
        data = json.loads(payload_str)
        
        # Create database session
        db = SessionLocal()
        
        # Create Reading from message data
        reading = Reading(
            sensor_id=data['sensor_id'],
            value=data['value'],
            unit=data['unit']
        )
        
        # Save to database
        db.add(reading)
        db.commit()
        
        print(f"✓ Saved: {data}")
        
        db.close()
        
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {msg.payload}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        if 'db' in locals():
            db.close()


def start_mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mosquitto", 1883)  # docker service name
    client.loop_start()