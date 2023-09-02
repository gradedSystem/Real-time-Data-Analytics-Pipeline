# Real-time Data Analytics Pipeline

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Stars](https://img.shields.io/github/stars/gradedSystem/Real-time-Data-Analytics-Pipeline)
![Watchers](https://img.shields.io/github/watchers/gradedSystem/Real-time-Data-Analytics-Pipeline)
![Forks](https://img.shields.io/github/forks/gradedSystem/Real-time-Data-Analytics-Pipeline)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yedige%20Ashmet-blue?logo=linkedin)](https://www.linkedin.com/in/yedige2000/)

Develop a streaming data pipeline that retrieves data from an API in the English language. Produce this data in real-time to an Apache Kafka topic. Finally, build a Spark Streaming application to consume the records from Kafka and calculate the number of words in each record in real-time.

<p align="center">
  <img src="https://github.com/gradedSystem/Real-time-Data-Analytics-Pipeline/raw/main/images/Kafka_project.png" alt="Kafka Project">
</p>

| ![Kafka Logo](https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-ar21.svg) | ![Confluent Logo](https://github.com/gradedSystem/Real-time-Data-Analytics-Pipeline/raw/main/images/confluent-logos-idT3RAPQdd.svg) | ![Python Logo](https://www.vectorlogo.zone/logos/python/python-ar21.svg) | ![AWS S3 Logo](https://www.vectorlogo.zone/logos/amazon_aws/amazon_aws-ar21.svg) |
|:---:|:---:|:---:|:---:|
| Apache Kafka | Confluent | Python | AWS S3 |

This repository contains a real-time data analytics pipeline built using Apache Kafka.

## Technologies Used

- **Apache Kafka**: A distributed event streaming platform used for building real-time data pipelines and streaming applications.

- **Virtualenv**: A tool to create isolated Python environments.

- **Confluent Kafka Python Client**: A Python client for Apache Kafka provided by Confluent.

## Confluent Setup

Before running the Kafka producers and consumers, you need to set up your Confluent environment.

1. Create a virtual environment and activate it:

    ```shell
    virtualenv env
    source env/bin/activate
    ```

2. Install the Confluent Kafka Python client:

    ```shell
    pip install confluent-kafka
    ```

3. Configure your `file.ini` with your Confluent Cloud API keys and cluster settings:

    ```ini
    [default]
    bootstrap.servers=<BOOTSTRAP SERVER>
    security.protocol=SASL_SSL
    sasl.mechanisms=PLAIN
    sasl.username=<CLUSTER API KEY>
    sasl.password=<CLUSTER API SECRET>

    [consumer]
    group.id=python_example_group_1

    auto.offset.reset=earliest
    ```

## How to Run

To run the Kafka producers and consumers, follow these steps:

### For Producer

1. Make the producer script executable:

    ```shell
    chmod u+x producer.py
    ```

2. Run the producer script with your `file.ini`:

    ```shell
    ./producer.py file.ini
    ```

### For Consumer

1. Make the consumer script executable:

    ```shell
    chmod u+x consumer.py
    ```

2. Run the consumer script with your `file.ini`:

    ```shell
    ./consumer.py file.ini
    ```

Make sure to run producers and consumers in separate git bash instances.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Apache Kafka and Confluent communities for their excellent tools and documentation.
