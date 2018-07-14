from collections import defaultdict

def rolling_average(data):
    read_data(data)
    trades = []
    if data['TYPE'] == 'book':
        symbol = data['SYMBOL']
        bids = data['BUY']
        for price, size in bids:
            rolling_average = get_rolling_average(symbol)
            if price > rolling_average && rolling_average != -1:
                trades.append(('SELL', symbol, price, size))

        asks = data['SELL']
        for price, size in asks:
            rolling_average = get_rolling_average(symbol)
            if price < rolling_average && rolling_average != -1:
                trades.append(('BUY', symbol, price, size))
                
    return trades

trade_history = defaultdict(list) # SYMBOL : LIST ((PRICE, SIZE))
windows = defaultdict(list)       # SYMBOL : LIST (Last WINDOW_SIZE prices) 
WINDOW_SIZE = 4
MIN_WINDOW_SIZE = 1

def read_data(data):
    if data['TYPE'] == 'trade':
        symbol = data['SYMBOL']
        trade_history[symbol].append((data['PRICE'], data['SIZE']))
        windows[symbol].append(data['PRICE'])
        if len(windows[symbol]) > WINDOW_SIZE:
            windows[symbol].pop(0)

def get_rolling_average(symbol):
    window = windows[symbol]
    if len(window) < MIN_WINDOW_SIZE:
        return -1
    return 1.0 * sum(window) / len(window)