#To run: spark-submit -spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.2,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 /home/ciro/Desktop/BDT/Kafka-Spark/kafka-spark.py-packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 (your path to the file, e.g. home/ciro/Desktop/BDT/Kafka-Spark/kafka-spark.py )
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
  .config('spark.cassandra.connection.host', CASSANDRA_HOST) \
  .config('spark.cassandra.connection.port', CASSANDRA_PORT) \
 .config("spark.cassandra.auth.username", CASSANDRA_USERNAME)\
  .config("spark.cassandra.auth.password", CASSANDRA_PASSWORD) \
  .getOrCreate()
 
# df = sqlContext.read.format("org.apache.spark.sql.cassandra").options(table, keyspace).load()
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
  .option("kafka.sasl.jaas.config", "org.apache.kafka.common.security.scram.ScramLoginModule required username='{}' password='{}';".format(KAFKA_USERNAME, KAFKA_PASSWORD))
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

def generate_id():
  return random.randint(0, 4)

#(generate_id() if col("id") is None else col("id"))
df_with_id = df.withColumn("id",rand())
#df_with_id = df.withColumn("id",when(col("id").isNull() ,generate_id()).otherwise(generate_id()))
# df_with_id = df.withColumn("id",col("id").cast("Integer"))
# df_with_id2 = df_with_id.withColumn("id",col("id")*2)

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
