import yfinance as yf

# stock = yf.Ticker("NVDA")
# info = stock.info
# print(type(info))

# print(info.keys())
# print(len(info))
# print(info['shortName'])
# print(info['longName'])
# print(info['currentPrice'])

# print(info['longBusinessSummary'])

# print(info['longBusinessSummary'].split())
# print('iphone' in info['longBusinessSummary'])

# print(info['city'])
# info['city'][0] = 'c'
# info['city'] = 'Wellesley'
# print(info['city'])

# info['founder'] = 'Robert'
# print(info['founder'])

tickers = ['NVDA', 'AAPL', 'MSFT']
prices = {}
for t in tickers:
    prices[t] = yf.Ticker(t).info['currentPrice']

print(prices)

print(sorted(prices))
print(sorted(prices.keys()))
print(sorted(prices.values(), reverse=True))

prices = {'AAPL': [252.53, 300], 'MSFT': [299.35, 350], 'NVDA': [195.25, 250]}
# print(sum(prices.values()))

total = 0
for price in prices.values():
    total += price[1]
print(total)
