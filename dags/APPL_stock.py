import airflow
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import pymongo
import json
import time
from plugin.jsontomongo import *
from plugin.getRating import *
from plugin.getProfile import *

def get_stock_price():
    urlProfile = "https://financialmodelingprep.com/api/v3/profile/AAPL?'"
    urlRating = "https://financialmodelingprep.com/api/v3/rating/AAPL?'"


    payload = {
        "apikey": "l7azE35y0TuREolwsrTyGE4qAPlxlqbh",
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
    with open('/tmp/data.json', 'w') as f:
        json.dump(data, f)

def save_stock():
    with open('/tmp/data.json', 'r') as f:
        data = json.load(f)

    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    db = client["stock"]
    collection = db["AAPL"]
    collection.insert_one(data)

    #read data
    data = collection.find_one()
    print(data)
    
    return data

args = {
    'id' : 'practice',
    'owner': 'airflow',
    'schedule_interval' : timedelta(minutes=1),
    'start_date': airflow.utils.dates.days_ago(0),
}

dag = DAG(
    dag_id='APPL_Stock',
    default_args=args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(minutes=1),
)

task = GetProfileOperator(
    task_id='get_stock',
    dag=dag,
)

task2 = GetRatingOperator(
    task_id='save_stock',
    dag=dag,
)

task3 = JsonToMongoOperator(
    task_id='save_stock_Profile',
    file_to_load='/tmp/profile.json',
    mongoserver='mongodb://mongodb:27017/',
    mongouser=None,
    mongopass=None,
    dag=dag,
)

task4 = JsonToMongoOperator(
    task_id='save_stock_Rating',
    file_to_load='/tmp/rating.json',
    mongoserver='mongodb://mongodb:27017/',
    mongouser=None,
    mongopass=None,
    dag=dag,
)

task >> task2 >> task3 >> task4