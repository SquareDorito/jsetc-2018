from strategies import strategies, test_strategies
import json

class Bot:
	def __init__(self, exchange, test_mode=True):
		self.exchange = exchange
		self.test = test_mode
		self.conversions = {}
		self.limits = {'XLK': [0, 0], 'BABA': [0, 0], 'BABZ': [0, 0]}
		self.xlks={}
		self.adr_fills_buys=[]
		self.adr_fills_sells=[]
		self.id = 0

	def write_to_exchange(self, obj):
		json.dump(obj, self.exchange)
		self.exchange.write("\n")

	def read_from_exchange(self):
		return json.loads(self.exchange.readline())

	def trade(self, sym, price, size, buy):
		if sym == 'XLK':
			if self.limits[sym][0 if buy else 1] + size > 100:
				# rejects orders that block
				return
			else:
				self.limits[sym][0 if buy else 1] += size
				self.xlks[self.id] = True
		elif sym == 'BABA':
			if self.limits[sym][0 if buy else 1] + size > 10:
				# rejects orders that block
				return
			else:
				self.limits[sym][0 if buy else 1] += size
				self.xlks[self.id] = True
		elif sym == 'BABZ':
			if self.limits[sym][0 if buy else 1] + size > 10:
				# rejects orders that block
				return
			else:
				self.limits[sym][0 if buy else 1] += size
				self.xlks[self.id] = True

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
		if len(self.conversions) > 0:
			print('excess conversions')
			return
		direction = 'BUY' if buy else 'SELL'
		order = {
			'type': 'convert',
			'order_id': self.id,
			'symbol': sym,
			'dir': direction,
			'size': size
		}
		if self.test:
			print(order)
		self.conversions[self.id] = (sym, size, buy)
		self.write_to_exchange(order)
		self.id += 1

	def run(self, data, p):
		if abs(p.get('BABA')) + abs(p.get('BABZ'))==20:
			direction = p.get('BABA')<0
			self.convert('BABA',10, direction)

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
		if abs(p.get('BABA'))+abs(p.get('BABZ'))==20:
			direction = p.get('BABA')<0
			self.convert('BABA',10, direction)

		#print(p.get('XLK'))
		if abs(p.get('XLK')) > 90:
			print('over limit')
			direction = p.get('XLK') < 0
			self.convert('XLK', 30, direction)

		for strategy in test_strategies:
			#print(strategy)
			trades = strategy(data, p, True)
			# print(trades)
			for trade in trades:
				if len(trade) == 0:
					continue
				sym, price, size, buy = trade
				self.trade(sym, price, size, buy)
