#To run: 
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.2,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 /opt/apps/spark_stream_handler.py


import random
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, TimestampType, DoubleType
from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.functions import col, rand, when
from pyspark.sql.functions import *

# import AstraDB_connection
import json

KAFKA_TOPIC = "wbwkos2c-Accidents"
KAFKA_SERVER = "moped-01.srvs.cloudkafka.com:9094"

# creating an instance of SparkSession
spark = SparkSession.builder \
  .appName('SparkCassandraApp') \
  .config('spark.cassandra.connection.host', '172a25cb-993d-42f0-b035-f382d55499c7-europe-west1.db.astra.datastax.com') \
  .config('spark.cassandra.connection.port', '29042') \
 .config("spark.cassandra.auth.username","XOsLEOoeawEZrZbWztghdatC")\
  .config("spark.cassandra.auth.password","q1LviFk7Mu0mdNgNYzrwUsZGqcmmIe56vPzAtyco,_0MRNLwp9Ebi+EWAZdnUbPiSYDtBodnHXlzDQwzLIzfhbtzQwxa6PzNzDgnoxIUZpLJdgaRsoFuGWXEmep3Zx9I") \
  .getOrCreate()
 
#To avoid unncessary logs
spark.sparkContext.setLogLevel("WARN")
spark.catalog.clearCache()

#Define a schema for the kafka data
schema = StructType() \
        .add("id", DoubleType(), True) \
        .add("latitude", StringType(), True) \
        .add("longitude", StringType(),True) \
        .add("level", StringType(),True)\
        .add("duration", StringType(),True)\
        .add("time", TimestampType(),True)\

# Subscribe to the kafka topic
topic = "wbwkos2c-Accidents"

# define the spark dataframe
# read all the kafka streams of the topic "wbwkos2c-Accidents"
df = (spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", KAFKA_SERVER)
  .option("kafka.security.protocol", "SASL_SSL")
  .option("kafka.sasl.jaas.config", "org.apache.kafka.common.security.scram.ScramLoginModule required username='{}' password='{}';".format("wbwkos2c", "N1sfB_RASP_Kg7hd151D2za-orxuIqIO"))
  .option("kafka.ssl.endpoint.identification.algorithm", "https")
  .option("kafka.sasl.mechanism", "SCRAM-SHA-256")
  .option("subscribe", topic)
  .option("startingOffsets", "latest")
  .option("failOnDataLoss", "false")
  .load().select(from_json(col("value").cast("string"), schema).alias("value")).select("value.*"))
print("Printing Schema of transaction_detail_df: ")
df.printSchema()


# Write on cassandra
CASSANDRA_KEYSPACE = 'accident_keyspace'
CASSANDRA_TABLE = 'accidents'

# generating primary key column
df_with_id = df.withColumn("id",rand())

# Writing to stream
query = df_with_id.writeStream \
      .outputMode('append')\
      .trigger(processingTime='5 seconds')\
      .format("org.apache.spark.sql.cassandra")\
      .option("checkpointLocation", 'checkpoint')\
      .option("keyspace", CASSANDRA_KEYSPACE)\
      .option("table", CASSANDRA_TABLE)\
      .start()

query.awaitTermination()

''''
this is to output on the spark console, just in case you need to check the connection beteweeen kafka and spark 

      query = df.writeStream \
      .outputMode('update')\
      .trigger(processingTime='5 seconds')\
      .format("console")\
      .start()
'''