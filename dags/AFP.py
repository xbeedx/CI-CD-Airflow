import requests
import pymongo
import time
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# get Apple's stock price as well as rating from FMP
def get_stock_price():
    urlProfile = "https://financialmodelingprep.com/api/v3/profile/AAPL?'"
    urlRating = "https://financialmodelingprep.com/api/v3/rating/AAPL?'"

    apikey = os.environ.get("API_FMP")  # Retrieve the apikey from the environment variable

    payload = {
        "apikey": apikey,
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

    with open('data.json', 'w') as f:
        json.dump(data, f)

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["stock"]
    collection = db["AAPL"]
    collection.insert_one(data)
    
    return data

print(get_stock_price())