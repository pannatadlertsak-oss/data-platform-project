#!/usr/bin/env python
# coding: utf-8

# # Spark Structured Streaming with Avro & Schema Registry
# 
# This notebook handles **Avro-encoded** data from Kafka using Confluent Schema Registry.

# In[1]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from pyspark.sql.avro.functions import from_avro
import requests
import json

# 1. Initialize Spark Session with Kafka & Avro Connectors
spark = SparkSession.builder \
    .appName("KafkaAvroStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-avro_2.12:3.5.0") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("Spark Session Created with Avro support!")


# In[2]:


# 2. Fetch Schema from Schema Registry
TOPIC_NAME = "food_orders"
SCHEMA_REGISTRY_URL = "http://schema-registry:8081"
SUBJECT = f"{TOPIC_NAME}-value"

try:
    response = requests.get(f"{SCHEMA_REGISTRY_URL}/subjects/{SUBJECT}/versions/latest")
    schema_json = response.json()['schema']
    print(f"Successfully fetched schema for {SUBJECT}")
    # print(schema_json) # Uncomment to see the raw schema
except Exception as e:
    print(f"Error fetching schema: {e}")
    print("Make sure schema-registry is running at http://localhost:8081")


# In[3]:


# 3. Read Stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", TOPIC_NAME) \
    .option("startingOffsets", "earliest") \
    .load()

# 4. Decode Avro Data
# Confluent Avro format: [1-byte magic] [4-byte schema id] [Avro data]
# We use expr("substring(value, 6)") to skip the first 5 bytes
decoded_df = df.select(expr("substring(value, 6)").alias("avro_payload")) \
    .select(from_avro(col("avro_payload"), schema_json).alias("data")) \
    .select("data.*")


# In[4]:


# 5. Write to Memory Sink for testing
query = decoded_df.writeStream \
    .queryName("avro_results") \
    .outputMode("append") \
    .format("memory") \
    .start()

print("Streaming started (Avro Decoded). Querying memory table...")


# In[10]:


# 6. View Results
from time import sleep
from IPython.display import display, clear_output

try:
    while True:
        clear_output(wait=True)
        print("Real-time Data from Kafka (Avro Decoded):")
        spark.sql("SELECT * FROM avro_results ORDER BY timestamp DESC LIMIT 20").show(truncate=False)
        sleep(3)
except KeyboardInterrupt:
    print("Stop monitoring.")

