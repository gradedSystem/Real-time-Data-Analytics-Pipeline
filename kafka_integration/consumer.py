#!/usr/bin/env python

import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instances
    consumer1 = Consumer(config)
    consumer2 = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topics
    topics = ["location", "current_weather_information"]
    consumer1.subscribe([topics[0]], on_assign=reset_offset)
    consumer2.subscribe([topics[1]], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg1 = consumer1.poll(1.0)
            msg2 = consumer2.poll(1.0)

            # Process messages from consumer1
            if msg1 is None:
                print("Consumer1: Waiting...")
            elif msg1.error():
                print("Consumer1: ERROR: {}".format(msg1.error()))
            else:
                print("Consumer1: Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg1.topic(), key=msg1.key().decode('utf-8'), value=msg1.value().decode('utf-8')))

            # Process messages from consumer2
            if msg2 is None:
                print("Consumer2: Waiting...")
            elif msg2.error():
                print("Consumer2: ERROR: {}".format(msg2.error()))
            else:
                print("Consumer2: Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg2.topic(), key=msg2.key().decode('utf-8'), value=msg2.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer1.close()
        consumer2.close()
