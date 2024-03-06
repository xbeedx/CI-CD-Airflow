import requests
import pymongo
import datetime
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# get Apple's stock price as well as rating from FMP
def get_stock_price():
    url = "https://financialmodelingprep.com/api/v3/quote/AAPL?'"

    apikey = os.environ.get("API_FMP")  # Retrieve the apikey from the environment variable

    payload = {
        "apikey": apikey,
    }
    response = requests.get(url, params=payload)
    data = response.json()
    return data

print(get_stock_price())