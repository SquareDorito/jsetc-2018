from .average import read_data, get_local_average
from collections import defaultdict

averageDict = defaultdict(int) # averages from the start
totalCountDict = defaultdict(int) # number of trades
windowDict = defaultdict(int) # last n prices

MIN_COUNT_TO_TRADE = 5 # when do we trust our average?
MARGIN=10

def adr_pair(data, p, test):
	read_data(
		data, p, test,
		averageDict,
		totalCountDict,
		windowDict,
		valid_symbols
	)
	trades = []

    #baba is adr, babz is liquid

	# if data['type'] == 'fill' and data['symbol'] == 'BABA':
	# 	if data['dir']=='BUY':
	# 		trades.append()
	# 	elif data['dir']=='SELL':
	# 		trades.append()


	if data['type'] == 'book' and data['symbol'] == 'BABA':
		bids=data['buy']
		for price, size in bids:
			if price>get_local_average('BABZ'):
				if p.get('babz')<=-10:
					break
				temp_size=size if p.get('babz')-size>=-10 else p.get('babz')+10
				trades.append(('BABZ', price, temp_size, False))
				trades.append(('BABA', price, temp_size, True))

		asks=data['sell']
		for price, size in asks:
			if price<get_local_average('BABZ'):
				if p.get('babz')>=10:
					break
				temp_size=size if p.get('babz')+size<=10 else 10-p.get('babz')
				trades.append(('BABZ', price, temp_size, True))
				trades.append(('BABA', price, temp_size, False))

    return trades
