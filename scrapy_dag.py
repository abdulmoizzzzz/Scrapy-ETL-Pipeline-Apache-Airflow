from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum
import os
import csv
import json

# Defining the paths to your Scrapy projects
SCRAPY_PROJECT_PATH1 = '/home/ubuntu/airflow/dags/FidelityUk'
SCRAPY_PROJECT_PATH2 = '/home/ubuntu/airflow/dags/Motleyfooluk'
SCRAPY_PROJECT_PATH3 = '/home/ubuntu/airflow/dags/SharesMagazine'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 10, tzinfo=pendulum.timezone('Asia/Karachi')),
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


## The Dad instance 
with DAG(
    'UK_Stockexchange_spiders_dag', ##This is the unique id for the dag
    default_args=default_args,
    description='A DAG to run Scrapy spiders daily and store the data on mongodb collections.',
    # schedule_interval='*/20 * * * *',  
    catchup=False
) as dag:

    # Task1
    run_spider1 = BashOperator(
        task_id='run_fidelity_spider',
        bash_command=f'cd {SCRAPY_PROJECT_PATH1} && scrapy crawl fidelity_spider -O "{SCRAPY_PROJECT_PATH1}/newsfidelity_data.json"',
    )
    # Task2
    run_spider2 = BashOperator(
        task_id='run_Motley_spider',
        bash_command=f'cd {SCRAPY_PROJECT_PATH2} && scrapy crawl Motley_spider -O "{SCRAPY_PROJECT_PATH2}/newsMotley_data.json"',
    )
    # Task3
    run_spider3 = BashOperator(
        task_id='run_SharesMagazine_spider',
        bash_command=f'cd {SCRAPY_PROJECT_PATH3} && scrapy crawl shares_spider -O "{SCRAPY_PROJECT_PATH3}/newsSharesMagazine_data.json"',
    )

    run_spider1 >> run_spider2 >> run_spider3


if __name__ == "__main__":
    dag.cli()
