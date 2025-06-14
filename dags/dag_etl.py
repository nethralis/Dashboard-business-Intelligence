from airflow import DAG
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime
import pandas as pd
import os

dag_path = os.path.dirname(__file__)


def extract():
    csv_path = os.path.join(dag_path, 'data_buin.csv')  # ganti ke nama file Anda
    df = pd.read_csv(csv_path, sep=';')

    # Bersihkan dan buat kolom waktu
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    df.to_csv('/tmp/tes_data.csv', index=False)


def transform_transaction_report():
    df = pd.read_csv('/tmp/tes_data.csv')
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    result = df.groupby(['Year', 'Month', 'Transaction_Type'])['Transaction_Amount'].sum().reset_index()
    result.to_csv('/tmp/fact_transaction_report.csv', index=False)


def transform_transaction_status():
    df = pd.read_csv('/tmp/tes_data.csv')
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    result = df.groupby(['Transaction_Type', 'Transaction_Status']).size().reset_index(name='Count')
    result.to_csv('/tmp/fact_transaction_status.csv', index=False)


def transform_transaction_period():
    df = pd.read_csv('/tmp/tes_data.csv')
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    result = df[['Transaction_ID', 'Sender_Account_ID', 'Receiver_Account_ID',
                 'Timestamp', 'Transaction_Type']]
    result.to_csv('/tmp/fact_transaction_period.csv', index=False)


def transform_fraud_check():
    df = pd.read_csv('/tmp/tes_data.csv')
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    result = df[['Transaction_ID', 'Sender_Account_ID', 'Receiver_Account_ID',
                 'Transaction_Amount', 'Transaction_Type', 'Fraud_Flag']]
    result.to_csv('/tmp/fact_fraud_check.csv', index=False)


def load():
    # Gabungkan semua hasil transform ke satu output
    output_path = os.path.join(dag_path, 'BUIN_data')
    os.makedirs(output_path, exist_ok=True)

    pd.read_csv('/tmp/fact_transaction_report.csv').to_csv(os.path.join(output_path, 'transaction_report.csv'), index=False)
    pd.read_csv('/tmp/fact_transaction_status.csv').to_csv(os.path.join(output_path, 'transaction_status.csv'), index=False)
    pd.read_csv('/tmp/fact_transaction_period.csv').to_csv(os.path.join(output_path, 'transaction_period.csv'), index=False)
    pd.read_csv('/tmp/fact_fraud_check.csv').to_csv(os.path.join(output_path, 'fraud_check.csv'), index=False)


with DAG(
    dag_id='dag_etl',
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['example', 'etl']
) as dag:

    t1 = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    t2a = PythonOperator(
        task_id='transform_transaction_report',
        python_callable=transform_transaction_report
    )

    t2b = PythonOperator(
        task_id='transform_transaction_status',
        python_callable=transform_transaction_status
    )

    t2c = PythonOperator(
        task_id='transform_transaction_period',
        python_callable=transform_transaction_period
    )

    t2d = PythonOperator(
        task_id='transform_fraud_check',
        python_callable=transform_fraud_check
    )

    t3 = PythonOperator(
        task_id='load',
        python_callable=load
    )

    # Alur DAG: extract >> semua transformasi >> load
    t1 >> [t2a, t2b, t2c, t2d] >> t3
