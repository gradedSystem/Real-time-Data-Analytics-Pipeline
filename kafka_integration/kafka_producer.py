import os 
import json
import time
import logging
from confluent_kafka import Producer
import sys
from dotenv import load_dotenv
load_dotenv()
print()

sys.path.insert(1,os.getenv("my_path"))
import api_main

KAFKA_TOPIC = "weather_data"
KAFKA_BROKER = "localhost:9092"  # Replace with your Kafka broker address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_producer(broker):
    producer_config = {
        "bootstrap.servers": broker
    }
    producer = Producer(producer_config)
    return producer

def send_data_to_kafka(producer, data):
    try:
        producer.produce(KAFKA_TOPIC, value=data)
        producer.flush()
        logger.info("Data sent to Kafka successfully.")
    except Exception as e:
        logger.error(f"Error sending data to Kafka: {e}")

def main():
    producer = configure_producer(KAFKA_BROKER)
    try:
        while True:
            coordinates = api_main.read_list_of_coordinates(api_main.COORDINATES_FILE)
            astronomy_city_data = api_main.fetch_astronomy_and_forecast_data(coordinates)

            for data_point in astronomy_city_data:
                send_data_to_kafka(producer, data_point)
            
            time.sleep(30 * 60)  # Wait for 30 minutes

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Flushing and closing Kafka producer.")
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main()