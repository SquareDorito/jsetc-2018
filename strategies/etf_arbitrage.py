from .average import read_data, get_local_average
from collections import defaultdict

MIN_COUNT_TO_TRADE = 5
averageDict = defaultdict(int) # averages from the start
totalCountDict = defaultdict(int) # number of trades
windowDict = defaultdict(list) # last n prices

def etf(data, p, test):
	MARGIN = 30
	valid_symbols = ['XLK', 'GOOG', 'AAPL', 'MSFT', 'BOND']
	read_data(
		data, p, test, 
		averageDict=averageDict, 
		totalCountDict=totalCountDict, 
		windowDict=windowDict, 
		valid_symbols=valid_symbols
	)
	trades = []
	constituents = get_local_average('GOOG', windowDict) + get_local_average('AAPL', windowDict) + get_local_average('MSFT', windowDict) + 1000
	
	if data['type'] == 'book':
		
		symbol = data['symbol']
		bids = data['buy']
		asks = data['sell']

		if symbol == 'XLK':
			for price, size in asks:
				if price - constituents > MARGIN and totalCountDict['XLK'] > MIN_COUNT_TO_TRADE:
					trades.append((symbol, price, size, False))
					# XLK_HEDGE += size

			for price, size in bids:
				if constituents - price > MARGIN and totalCountDict['XLK'] > MIN_COUNT_TO_TRADE:
					trades.append((symbol, price, size, True))
					# XLK_HEDGE -= size
	return trades

		

				
			
			
			
