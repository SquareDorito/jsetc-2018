from strategies import strategies, test_strategies
import json

class Bot:
	def __init__(self, exchange, test_mode=True):
		self.exchange = exchange
		self.test = test_mode
		self.conversions = {}
		self.id = 0

	def write_to_exchange(self, obj):
		json.dump(obj, self.exchange)
		self.exchange.write("\n")
	
	def read_from_exchange(self):
		return json.loads(self.exchange.readline())

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
		if self.test:
			print(order)
		self.write_to_exchange(order)
		self.id += 1

	def convert(self, sym, size, buy):
		direction = 'BUY' if buy else 'SELL'
		order = {
			'type': 'convert',
			'order_id': self.id,
			'symbol': sym,
			'dir': direction,
			'size': size
		}
		self.conversions[self.id] = (sym, size, buy)
		self.write_to_exchange(order)
		self.id += 1

	def run(self, data, p):
		if abs(p.get('XLK')) > 90:
			direction = p.get('XLK') < 0
			self.convert('XLK', 30, direction)

		for strategy in strategies:
			trades = strategy(data, p, False)
			for trade in trades:
				if len(trade) == 0:
					continue
				sym, price, size, buy = trade
				self.trade(sym, price, size, buy)
	
	def test_run(self, data, p):
		for strategy in test_strategies:
			trades = strategy(data, p, True)
			for trade in trades:
				if len(trade) == 0:
					continue
				sym, price, size, buy = trade
				self.trade(sym, price, size, buy)

