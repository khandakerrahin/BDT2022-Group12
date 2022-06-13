# Dockerfile, Image, Container
FROM python:3.9

ADD data_generator.py .
ADD kafka_consumer.py .
ADD kafka_producer.py .

RUN pip install requests kafka-python

CMD [ "python", "./kafka_producer.py" ]