def simple_bond(data):
    trades = []
    if data['type'] == 'book' and data['symbol'] == 'BOND':
        bids = data['buy']
        print(f"bids: {data['buy']}")
        for price, size in bids:
            if price > 1000:
                trades.append(('SELL', 'BOND', price, size))

        asks = data['sell']
        print(f"asks: {data['sell']}")
        for price, size in asks:
            if price < 1000:
                trades.append(('BUY', 'BOND', price, size))

    if len(trades) > 0:
        print('trades: ',)
        print(trades)
    return trades