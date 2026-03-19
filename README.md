# Data Platform Project

This project is a local development data platform using Apache Airflow, Kafka, and Spark.

## Infrastructure

The platform consists of the following services (managed by Docker Compose):

- **Airflow**: Workload orchestration.
- **Kafka**: Event streaming platform.
- **Kafka UI**: Web interface for managing and viewing Kafka topics/messages.
- **Zookeeper**: Centralized service for maintaining configuration information for Kafka.
- **PostgreSQL**: Metadata database for Airflow.
- **Redis**: Message broker for Airflow Celery executor.

## Apache Kafka Configuration

Kafka is configured with two listeners:
- **Internal (Docker Network)**: `kafka:29092` (Used by other containers like Spark).
- **External (Host Machine)**: `localhost:9092` (Used by external tools like n8n).

### Connecting to Kafka
To connect from your local machine (e.g., n8n, Python script):
- **Bootstrap Server**: `localhost:9092`

### Viewing Data (Kafka UI)
A web interface is available to view topics and messages:
- **URL**: `http://localhost:8090`

## Getting Started

1. Start all services:
   ```bash
   docker-compose up -d
   ```
2. Access Airflow UI: `http://localhost:8080` (Default: `airflow`/`airflow`)

## Apache Spark & Jupyter Lab

We use a custom Spark cluster with Jupyter Lab for development.

- **Spark Master UI**: [http://localhost:8091](http://localhost:8091)
- **Spark Worker UI**: [http://localhost:8092](http://localhost:8092)
- **Jupyter Lab**: [http://localhost:8888](http://localhost:8888) (Token: `data-platform-secret`)

### Running Spark Streaming Jobs

To run the streaming job from the terminal (using the custom built image):

```bash
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-avro_2.12:3.5.0 \
  /opt/spark/app/streaming/kafka_to_console.py
```

### Converting Notebooks to Scripts

If you develop in Jupyter and want to run it via `spark-submit`:

```bash
docker exec -it jupyter jupyter nbconvert --to python /home/jovyan/work/streaming_test.ipynb
```

## Service Ports Summary

| Service | Internal Port | External Port | URL |
| :--- | :--- | :--- | :--- |
| **Airflow Webserver** | 8080 | 8080 | [http://localhost:8080](http://localhost:8080) |
| **Kafka UI** | 8080 | 8090 | [http://localhost:8090](http://localhost:8090) |
| **Spark Master UI** | 8080 | 8091 | [http://localhost:8091](http://localhost:8091) |
| **Spark Worker UI** | 8081 | 8092 | [http://localhost:8092](http://localhost:8092) |
| **Jupyter Lab** | 8888 | 8888 | [http://localhost:8888](http://localhost:8888) |
| **Schema Registry** | 8081 | 8081 | [http://localhost:8081](http://localhost:8081) |
| **Kafka (External)** | 9092 | 9092 | `localhost:9092` |
| **Zookeeper** | 2181 | 2181 | `localhost:2181` |

## Development Setup

1. **Rebuild Spark Image** (if dependencies change in `requirements.txt`):
   ```bash
   docker-compose up -d --build spark-master spark-worker
   ```
2. **Persistence**: Data for Kafka and Zookeeper is stored in `./data/kafka` and `./data/zookeeper`.
