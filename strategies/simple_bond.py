def simple_bond(data):
    trades = []
    if data['TYPE'] == 'book' and data['SYMBOL'] == 'BOND':
        bids = data['BUY']
        for price, size in bids:
            if price > 1000:
                trades.append(('SELL', 'BOND', price, size))

        asks = data['SELL']
        for price, size in asks:
            if price < 1000:
                trades.append(('BUY', 'BOND', price, size))
                
    return trades
