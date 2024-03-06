import requests
import pymongo
import datetime

# get Apple's stock price as well as rating from FMP
def get_stock_price():
    url = ("https://financialmodelingprep.com/api/v3/quote/AAPL?'")
    payload = {
        "apikey": "",
    }
    response = requests.get(url, params=payload)
    data = response.json()
    return data

print(get_stock_price())