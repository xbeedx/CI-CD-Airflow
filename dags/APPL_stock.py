import airflow
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import pymongo
import json
import time

def get_stock_price():
    urlProfile = "https://financialmodelingprep.com/api/v3/profile/AAPL?'"
    urlRating = "https://financialmodelingprep.com/api/v3/rating/AAPL?'"


    payload = {
        "apikey": "EpG6rVvce9F8xsIsDA7sfDgROLt4Ogyr",
    }
    responseProfile = requests.get(urlProfile, params=payload)
    dataProfile = responseProfile.json()
    responseRating = requests.get(urlRating, params=payload)
    dataRating = responseRating.json()

    data = {}
    # get timestamp to timestamp format
    data["timestamp"] = time.time()
    data["profile"] = dataProfile
    data["rating"] = dataRating

    print(data)

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock"]
    collection = db["AAPL"]
    collection.insert_one(data)
    
    return data


args = {
    'id' : 'practice',
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'schedule_interval' : timedelta(minutes=1),
}

dag = DAG(
    dag_id='APPL_Stock',
    default_args=args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(minutes=1),
)

task = PythonOperator(
    task_id='get_stock_price',
    python_callable=get_stock_price,
    dag=dag,
)