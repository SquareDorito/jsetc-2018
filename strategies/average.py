from collections import defaultdict

MIN_COUNT_TO_TRADE = 10 # when do we trust our average?
averageDict = defaultdict(int)
totalCountDict = defaultdict(int)

def average(data):
    read_data(data)
    trades = []
    if data['type'] == 'book':
        symbol = data['symbol']
        bids = data['buy']
        for price, size in bids:
            rolling_average = get_rolling_average(symbol)
            if price > averageDict[symbol] and totalCountDict[symbol] > MIN_COUNT_TO_TRADE:
                trades.append((symbol, price, size, False))

        asks = data['sell']
        for price, size in asks:
            rolling_average = get_rolling_average(symbol)
            if price < averageDict[symbol] and totalCountDict[symbol] > MIN_COUNT_TO_TRADE:
                trades.append((symbol, price, size, True))
                
    #return trades
    return []

def read_data(data):
    if data['type'] == 'trade':
        symbol = data['symbol']
        price = data['price']
        num_new = data['size']
        num_old = totalCountDict[symbol]
        new_total = num_new + num_old
        averageDict[symbol] = 1.0 * averageDict[symbol] * num_old / new_total + 1.0 * price * num_new / new_total
        totalCountDict[symbol] = new_total
        if test:
            print(averageDict)