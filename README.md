# BDT2022-Group12

**Big Data Technologies Project 2022 - Group 12**

The aim of this big data project is to design and implement a big data system that can provide real-time context-aware recommendations to drivers on the level of possible danger. 

#
**Live Demo:** [Click here](https://bdt2022group12.pythonanywhere.com/)
#
Technologies used: 
- Kafka
- Apache Spark
- Cassandra
- Flask
- Folium
- Leaflet
- MySQL
#
Web Hosts: 
- [Amazon Web Server](https://aws.amazon.com/)
- [Cloud Karafka](https://cloudkarafka.com)
- [Cassandra Astra DB](https://astra.datastax.com/)
- [PythonAnywhere](https://www.pythonanywhere.com/)
#

**Prerequisites:**
- Python >= 3.7
- Spark >= 3.0.3
- Cassandra >= 3.0.19
- Python packages: confluent_kafka, datetime, json, random, pyspark, folium, flask, time, csv, mysql.connector

#
**Dataset source**: 
[Open Data Trentino](https://dati.trentino.it/dataset/incidenti-open-data)


#
**How to run the Project**
- run the "kafka_accident_producer.py" (preferably in Crontab)
  - python3 kafka_accident_producer.py
- run the StreamHandler
  - spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.2,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 /opt/apps/spark_stream_handler.py
- run the Flask webapp
  - python3 webapp.py


