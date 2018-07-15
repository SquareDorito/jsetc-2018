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

	if data['type'] == 'book' and data['symbol'] == 'BABA':
		bids=data['buy']
		for price, size in bids:
			if price>get_local_average('BABZ')+MARGIN:
				if p.get('baba')<=-10:
					break
				temp_size=size if p.get('baba')-size>=-10 else p.get('baba')+10
				trades.append(('BABA', price, temp_size, False))
				if p.get('babz')+temp_size<=10:
					trades.append(('BABZ', price, temp_size, True))

		asks=data['sell']
		for price, size in asks:
			if price<get_local_average('BABZ')-MARGIN:
				if p.get('baba')>=10:
					break
				temp_size=size if p.get('baba')+size<=10 else 10-p.get('baba')
				trades.append(('BABA', price, temp_size, True))
				if p.get('babz')-temp_size>=-10:
					trades.append(('BABZ', price, temp_size, False))
	#print(trades)
	return trades
