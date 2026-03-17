import pandas as pd

def transform_data(**context):

    ti = context["ti"]

    data = ti.xcom_pull(task_ids="extract_task")

    df = pd.read_json(data)

    df["total"] = df["price"] * df["quantity"]

    print("Transformed data")
    print(df)

    return df.to_json()