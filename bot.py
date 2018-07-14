from strategies import strategies
import json

class Bot:

    def __init__(self, exchange):
        self.exchange = exchange
        self.id = 0

    def write_to_exchange(self, obj):
        json.dump(obj, self.exchange)
        self.exchange.write("\n")
    
    def trade(self, sym, price, size, buy):
        direction = 'BUY' if buy else 'SELL'
        order = {
            'type': 'add',
            'order_id': self.id,
            'symbol': sym,
            'dir': direction,
            'price': price,
            'size': size,
        }
        self.write_to_exchange(order)
        self.id += 1


    def run(self, data):
        for strategy in strategies:
            trades = strategy(data)
            for trade in trades:
                sym, price, size, buy = trade
                self.trade(sym, price, size, buy)
