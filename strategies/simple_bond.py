def simple_bond(data, p, test):
    trades = []
    if data['type'] == 'book' and data['symbol'] == 'BOND':
        bids = data['buy']
        # print('bids: ', data['buy'])
        for price, size in bids:
            if price > 1000:
                trades.append(('BOND', price, size, False))

        asks = data['sell']
        # print('asks: ', data['sell'])
        for price, size in asks:
            if price < 1000:
                trades.append(('BOND', price, size, True))

    if len(trades) > 0:
        print('trades: ', trades)
    return trades