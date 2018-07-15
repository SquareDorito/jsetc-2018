from collections import defaultdict
import matplotlib.pyplot as plt

MIN_COUNT_TO_TRADE = 5 # when do we trust our average?
averageDict = defaultdict(int)
totalCountDict = defaultdict(int)
WINDOW_SIZE = 10
windowDict = defaultdict(list)

EXP_RATIO = .5
expAverageDict = {}

localAverageDict = defaultdict(list)

def average(data, p, test):
    read_data(data, p, test)
    trades = []
    if data['type'] == 'book':
        symbol = data['symbol']
        margin = 10

        if symbol == 'XLK':
            margin = 20

        # if test and symbol == 'BABA':
        #     margin = 10

        if symbol == 'BABA':
            average = get_local_average('BABZ')
        else:
            average = get_local_average(symbol)

        if test:
            average = expAverageDict[symbol]
            if symbol == 'BABA':
                average = expAverageDict['BABZ']

        bids = data['buy']
        for price, size in bids:
            #if price > averageDict[symbol] + MARGIN and totalCountDict[symbol] > MIN_COUNT_TO_TRADE:
            if price > average + margin and totalCountDict[symbol] > MIN_COUNT_TO_TRADE:
                trades.append((symbol, price, size, False))

        asks = data['sell']
        for price, size in asks:
            #if price < averageDict[symbol] - MARGIN and totalCountDict[symbol] > MIN_COUNT_TO_TRADE:
            if price < average - margin and totalCountDict[symbol] > MIN_COUNT_TO_TRADE:
                trades.append((symbol, price, size, True))
                
    return trades

def read_data(
    data,
    p,
    test,
    averageDict=averageDict,
    totalCountDict=totalCountDict,
    windowDict=windowDict,
    valid_symbols=['GOOG','AAPL','BABA','BABZ','MSFT','BOND','XLK']
    ):
    if data['type'] == 'trade':
        symbol = data['symbol']
        if symbol not in valid_symbols:
            return
        price = data['price']

        # average
        num_new = data['size']
        num_old = totalCountDict[symbol]
        new_total = num_new + num_old
        averageDict[symbol] = 1.0 * averageDict[symbol] * num_old / new_total + 1.0 * price * num_new / new_total
        totalCountDict[symbol] = new_total

        # local average
        windowDict[symbol].append(price)
        if len(windowDict[symbol]) > WINDOW_SIZE:
            windowDict[symbol].pop(0)

        # exponential average
        if symbol in expAverageDict:
            expAverageDict[symbol] = expAverageDict[symbol] * EXP_RATIO + price * (1 - EXP_RATIO)
        else:
            expAverageDict[symbol] = price

        localAverageDict[symbol].append(get_local_average(symbol))
        if len(localAverageDict[symbol]) % 50 == 0:
            plt.ylabel('some numbers')
            plt.show()


def get_local_average(symbol, windowDict=windowDict):
    if len(windowDict[symbol]) > 0:
        return 1.0 * sum(windowDict[symbol]) / len(windowDict[symbol])
    return -1

