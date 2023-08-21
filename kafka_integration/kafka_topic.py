from confluent_kafka import Producer

def send_to_kafka_topic(data, topic):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    for record in data:
        producer.produce(topic, value=record)
    producer.flush()

def main():
    # Rest of your code...
    
    # Send data to Kafka topics
    send_to_kafka_topic(astronomy_city_data, 'astronomy_data_topic')
    send_to_kafka_topic(forecast_weather_data, 'forecast_data_topic')

if __name__ == "__main__":
    main()
