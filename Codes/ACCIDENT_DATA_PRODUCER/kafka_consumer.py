import json 
from kafka import KafkaConsumer


if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'accident_kafka_topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        print("CONSUMER MESSAGES: ", json.loads(message.value))