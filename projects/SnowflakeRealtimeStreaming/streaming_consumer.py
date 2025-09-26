"""
Kafka consumer streaming data to Snowflake
"""
from confluent_kafka import Consumer
import snowflake.connector

def load_to_snowflake(data):
    # Placeholder for Snowflake load logic
    print("Loading to Snowflake:", data)

def main():
    conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'snowflake-stream-group', 'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    consumer.subscribe(['snowflake_stream_topic'])
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None or msg.error():
                continue
            # Here, transform and load to Snowflake
            load_to_snowflake(msg.value().decode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main()