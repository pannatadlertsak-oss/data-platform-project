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
2. Access Airflow UI: `http://localhost:8080` (Default: airflow/airflow)
