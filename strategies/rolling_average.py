from collections import defaultdict

def rolling_average(data):
    read_data(data)
    trades = []
    if data['type'] == 'book':
        symbol = data['symbol']
        bids = data['buy']
        for price, size in bids:
            rolling_average = get_rolling_average(symbol)
            if price > rolling_average and rolling_average != -1:
                trades.append((symbol, price, size, false))

        asks = data['sell']
        for price, size in asks:
            rolling_average = get_rolling_average(symbol)
            if price < rolling_average and rolling_average != -1:
                trades.append((symbol, price, size, true))
                
    #return trades
    return []

trade_history = defaultdict(list) # SYMBOL : LIST ((PRICE, SIZE))
windows = defaultdict(list)       # SYMBOL : LIST (Last WINDOW_SIZE prices) 
WINDOW_SIZE = 4
MIN_WINDOW_SIZE = 1

def read_data(data):
    if data['type'] == 'trade':
        symbol = data['symbol']
        trade_history[symbol].append((data['price'], data['size']))
        windows[symbol].append(data['price'])
        if len(windows[symbol]) > WINDOW_SIZE:
            windows[symbol].pop(0)
    print(trade_history)
    print(windows)

def get_rolling_average(symbol):
    window = windows[symbol]
    if len(window) < MIN_WINDOW_SIZE:
        return -1
    return 1.0 * sum(window) / len(window)