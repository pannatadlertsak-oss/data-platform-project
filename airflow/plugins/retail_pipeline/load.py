import pandas as pd

def load_data(**context):

    ti = context["ti"]

    data = ti.xcom_pull(task_ids="transform_task")

    df = pd.read_json(data)

    df.to_csv("/opt/airflow/data/sales_output.csv", index=False)

    print("Saved output file")