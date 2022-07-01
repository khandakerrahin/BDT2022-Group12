import sys
import time
import json
import random
from datetime import datetime
from accident_data_generator import generate_accident
from kafka import KafkaProducer
from confluent_kafka import Producer

if __name__ == '__main__':
    # kafka Producer configuration
    topic = ['wbwkos2c-Accidents']
    conf = {
            'bootstrap.servers':  'moped-01.srvs.cloudkafka.com:9094',
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': "wbwkos2c",
            'sasl.password': "N1sfB_RASP_Kg7hd151D2za-orxuIqIO"
            }

    # create the producer
    p = Producer(**conf)

    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            # sys.stderr.write('%% Message delivered to %s [%d]\n' %(msg.topic(), msg.partition()))
            sys.stderr.write('.')

    # Randomized loop - runs until n times
    count = random.randint(1, 15)
    c = 0
    while c<count:
        # Generate a kafka Accident message
        accident_message = generate_accident()

        # Send it to our 'accidents' topic
        # send message to topic in json format
        try:
            # p.produce(topic[0], json.dumps(accident_message).encode('utf-8'))
            p.produce(topic[0], json.dumps(accident_message).encode('utf-8'), callback=delivery_callback)
        except BufferError as e:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                                len(p))
        
        p.poll(0)
        #sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
        p.flush()
        p.poll(0)

        c=c+1
        # Sleep for a random number of seconds
        #   time_to_sleep = random.randint(0, 10)
        #   time.sleep(time_to_sleep)