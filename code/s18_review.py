# import yfinance as yf
# from pprint import pprint

# tickers = ['AAPL', 'NVDA', 'MSFT', 'META', 'GOOG']
# stocks = {}

# for t in tickers:
#     stocks[t] = yf.Ticker(t).info['currentPrice']

#print(stocks)

# print('After sorting ...')
# print(sorted(stocks.items()))

import requests

response = requests.get(
    'https://oim.108122.xyz/words/random',
    headers={'X-Token': 'SparkSpark'},  # your first name x2
)
print(response.json())