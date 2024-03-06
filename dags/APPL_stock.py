import airflow
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from AFP import get_stock_price

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0),
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'stock_price',
    default_args=default_args,
    description='Get stock price of Apple Inc. every minute',
    schedule_interval=timedelta(minutes=1),
)

task = PythonOperator(
    task_id='get_stock_price',
    python_callable=get_stock_price,
    dag=dag,
)