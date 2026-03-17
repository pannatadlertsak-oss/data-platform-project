from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from retail_pipeline.extract import extract_data
from retail_pipeline.transform import transform_data
from retail_pipeline.load import load_data

with DAG(
    dag_id="retail_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract_data
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_data
    )

    extract_task >> transform_task >> load_task