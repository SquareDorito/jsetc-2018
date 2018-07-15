from .average import read_data, get_local_average
from collections import defaultdict

averageDict = defaultdict(int) # averages from the start
totalCountDict = defaultdict(int) # number of trades
windowDict = defaultdict(list) # last n prices

MIN_COUNT_TO_TRADE = 5 # when do we trust our average?
MARGIN=5

def adr_pair(data, p, test):
	valid_symbols = ['BABA', 'BABZ']
	read_data(
		data, p, test,
		averageDict,
		totalCountDict,
		windowDict,
		valid_symbols
	)
	trades = []

	buffered_buys=0
	buffered_sells=0

	if data['type'] == 'book' and data['symbol'] == 'BABA':
		bids=data['buy']
		for price, size in bids:
			if price>get_local_average('BABZ')+MARGIN:
				if p.get('baba')<=-10:
					break
				temp_size=size if p.get('baba')-size>=-10 else p.get('baba')+10
				trades.append(('BABA', price, temp_size, False))
				buffered_buys+=temp_size

		asks=data['sell']
		for price, size in asks:
			if price<get_local_average('BABZ')-MARGIN:
				if p.get('baba')>=10:
					break
				temp_size=size if p.get('baba')+size<=10 else 10-p.get('baba')
				trades.append(('BABA', price, temp_size, True))
				buffered_sells+=temp_size


	if data['type'] == 'book' and data['symbol'] == 'BABZ':
		bids=data['buy']
		for price, size in bids:
			if size>buffered_sells:
				trades.append(('BABZ',price,buffered_sells,False))
				break
			else:
				trades.append(('BABZ',price,size,False))
				buffered_sells-=size

		asks=data['sell']
		for price, size in asks:
			if size>buffered_buys:
				trades.append(('BABZ',price,buffered_buys,True))
				break
			else:
				trades.append(('BABZ',price,size,True))
				buffered_buys-=size

	return trades
