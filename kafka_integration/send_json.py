import os
import time
import signal
import json
from dotenv import load_dotenv
load_dotenv()
from confluent_kafka import Producer
from api_main import fetch_astronomy_and_forecast_data

boostrap_server = os.getenv("boostrap_server")
topic = "Kafka_test"

# Producer configuration
conf = {
    "bootstrap.servers": boostrap_server,
    "security.protocol": "ssl",
    "client.id": "python-producer"
}

# Create a Kafka producer instance
producer = Producer(conf)

def close_producer(signal, frame):
    print("Closing Kafka producer...")
    producer.flush()  # Ensure any buffered messages are sent
    print("Kafka producer closed.")
    exit(0)

# Register a signal handler to catch Ctrl+C
signal.signal(signal.SIGINT, close_producer)

try:
    while True:
        # Fetch data from the API
        real_time_data = fetch_astronomy_and_forecast_data(os.getenv("cord_abs_path"))
        
        # Send fetched data to Kafka
        for data in real_time_data:
            message = json.dumps(data)
            producer.produce(topic, message.encode("utf-8"))
        
        # Wait for any outstanding messages to be delivered and delivery reports to be received
        producer.flush()

        # Sleep for 30 minutes before fetching data again
        time.sleep(30 * 60)  # 30 minutes in seconds

except KeyboardInterrupt:
    close_producer(None, None)
