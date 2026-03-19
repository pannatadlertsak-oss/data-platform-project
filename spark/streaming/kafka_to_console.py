from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from pyspark.sql.avro.functions import from_avro
import requests
import json
import os

# Initialize Spark Session with Kafka & Avro Connectors
# Note: we use 3.5.0 packages for Spark 3.5.0
spark = SparkSession.builder \
    .appName("KafkaAvroStreamingConsole") \
    .getOrCreate() # Packages are passed via spark-submit command line

spark.sparkContext.setLogLevel("ERROR")

# Configuration
TOPIC_NAME = "food_orders"
SCHEMA_REGISTRY_URL = "http://schema-registry:8081"
SUBJECT = f"{TOPIC_NAME}-value"

# Fetch Schema from Schema Registry
try:
    response = requests.get(f"{SCHEMA_REGISTRY_URL}/subjects/{SUBJECT}/versions/latest")
    schema_json = response.json()['schema']
    print(f"Successfully fetched schema for {SUBJECT}")
except Exception as e:
    print(f"Error fetching schema: {e}")
    os._exit(1)

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", TOPIC_NAME) \
    .option("startingOffsets", "earliest") \
    .load()

# Decode Avro Data (skipping 5 magic bytes)
decoded_df = df.select(expr("substring(value, 6)").alias("avro_payload")) \
    .select(from_avro(col("avro_payload"), schema_json).alias("data")) \
    .select("data.*")

# Write to Console
query = decoded_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

print(f"Streaming started from topic '{TOPIC_NAME}'. Monitoring for data...")
query.awaitTermination()
