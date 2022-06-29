#To run: spark-submit -spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.2,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 /home/ciro/Desktop/BDT/Kafka-Spark/kafka-spark.py-packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 (your path to the file, e.g. home/ciro/Desktop/BDT/Kafka-Spark/kafka-spark.py )
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.2,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 /home/ciro/Desktop/BDT/Kafka-Spark/kafka-spark.py


from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType
from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.functions import *
import AstraDB_connection


KAFKA_TOPIC = "Accidents"
KAFKA_SERVER = "localhost:9092"

# creating an instance of SparkSession
spark = SparkSession.\
        builder.\
        config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2").\
        config("spark.jars.packages", "org.apache.spark:spark-token-provider-kafka-0-10_2.13:3.1.2").\
        config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0").\
        config("spark.cassandra.connection.host", "127.0.0.1").\
        appName("StreamingApp").\
        getOrCreate()

        

#To avoid unncessary logs
spark.sparkContext.setLogLevel("WARN")


#Define a schema for the kafka data
schema = StructType() \
        .add("user_id", StringType(), True) \
        .add("random_recipient_id", StringType(),True) \
        .add("message", StringType(),True)\

# Subscribe to the kafka topic
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load().select(from_json(col("value").cast("string"), schema).alias("value")).select("value.*")

print("Printing Schema of transaction_detail_df: ")
df.printSchema()


# Write on cassandra
CASSANDRA_KEYSPACE = 'test'
CASSANDRA_TABLE = 'tableaccidents'


query = df.writeStream \
      .outputMode('Append')\
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