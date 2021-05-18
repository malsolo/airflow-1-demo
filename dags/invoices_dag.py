from datetime import datetime, timedelta

import json
import os

import logging

import pandas as pd

from sqlalchemy import create_engine

from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.operators.postgres_operator import PostgresOperator


default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 5, 1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "malsolo.com@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

logging.basicConfig(level=logging.INFO)


data_path = f'{json.loads(BaseHook.get_connection("data_path").get_extra()).get("path")}/data.csv'
transformed_path = f'{os.path.splitext(data_path)[0]}-transformed.csv'


def transform_data(*args, **kwargs):
    invoices_data = pd.read_csv(filepath_or_buffer=data_path,
                                sep=',',
                                header=0,
                                usecols=['StockCode', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'],
                                parse_dates=['InvoiceDate'],
                                index_col=0
                                )
    invoices_data.to_csv(path_or_buf=transformed_path)


def store_in_db(*args, **kwargs):
    transformed_invoices = pd.read_csv(transformed_path)
    transformed_invoices.columns = [c.lower() for c in
                                    transformed_invoices.columns]  # postgres doesn't like capitals or spaces

    transformed_invoices.dropna(axis=0, how='any', inplace=True)
    engine = create_engine(
        'postgresql://airflow:airflow@postgres/pluralsight')

    transformed_invoices.to_sql("invoices",
                                engine,
                                if_exists='append',
                                chunksize=500,
                                index=False
                                )


with DAG(dag_id = "invoices_dag", 
         schedule_interval = "@daily",
         template_searchpath=[f"{os.environ['AIRFLOW_HOME']}"],
         default_args = default_args,
         catchup = False) as dag:


    is_new_data_available = FileSensor(
        task_id="is_new_data_available",
        fs_conn_id="data_path",
        filepath="data.csv",
        poke_interval=5,
        timeout=20
    )


    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )


    create_table = PostgresOperator(
        task_id="create_table",
        sql='''CREATE TABLE IF NOT EXISTS invoices (
                stockcode VARCHAR(50) NOT NULL,
                quantity integer NOT NULL,
                invoicedate DATE NOT NULL,
                unitprice decimal NOT NULL,
                customerid integer NOT NULL,
                country VARCHAR (50) NOT NULL
                );''',
        postgres_conn_id='postgres',
        database='pluralsight'
    )

    
    save_into_db = PythonOperator(
        task_id='save_into_db',
        python_callable=store_in_db
    )    


    is_new_data_available >> transform_data
    transform_data >> create_table >> save_into_db



