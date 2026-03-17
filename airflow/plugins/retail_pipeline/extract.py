import pandas as pd

def extract_data(**context):

    df = pd.read_excel("/opt/airflow/data/sales_sample_data.xlsx")

    print("Extracted data")
    print(df.head())

    return df.to_json()