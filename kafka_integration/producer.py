#!/usr/bin/env python

import os
import sys
import time
import json
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer
import api_main
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

COORDINATES_FILE = os.getenv("cord_abs_path")

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    # Produce data by selecting random values from these lists.
    topics = ["location","current_weather_information"]
    entries = ['entry1','entry2','entry3','entry4','entry5']
    while True:
        try:
            product = api_main.fetch_astronomy_and_forecast_data(COORDINATES_FILE)
            for counter, entry in enumerate(entries, start=0):
                location_json = json.dumps(product[entries[counter]]['location']).encode('utf-8')
                producer.produce(topics[0], key=json.dumps(entry).encode('utf-8'), value=location_json, callback=delivery_callback)
                time.sleep(2)
            time.sleep(3)
            for counter, entry in enumerate(entries, start=0):
                location_json = json.dumps(product[entries[counter]]['current']).encode('utf-8')
                producer.produce(topics[1], key=json.dumps(entry).encode('utf-8'), value=location_json, callback=delivery_callback)
                time.sleep(2)
            time.sleep(30)
        except KeyboardInterrupt:
            print("Received KeyboardInterrupt. Exiting gracefully.")
            # Block until the messages are sent.
            producer.poll(10000)
            producer.flush()