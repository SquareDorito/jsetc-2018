def execute(data):
    trades = []
    if data['type'] == 'book' and data['symbol'] == 'BOND':
        bids = data['BUY']
        for price, size in bids:
            if price > 1000:
                trades.append(('SELL', 'BOND', price, size))

        asks = data['sell']
        for price, size in asks:
            if price < 1000:
                trades.append(('BUY', 'BOND', price, size))

    return trades
