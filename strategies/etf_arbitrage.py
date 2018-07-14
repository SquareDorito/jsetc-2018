from .average import read_data
from collections import defaultdict

MIN_COUNT_TO_TRADE = 5
averageDict = defaultdict(int) # averages from the start
totalCountDict = defaultdict(int) # number of trades
windowDict = defaultdict(int) # last n prices
def etf(data, p, test):
	MARGIN = 30
	valid_symbols = ['xlk', 'goog', 'aapl', 'msft', 'bond']
	read_data(
		data, p, test, 
		averageDict, 
		totalCountDict, 
		windowDict, 
		valid_symbols
	)
	trades = []
	constituents = windowDict['goog'] + windowDict['aapl'] + windowDict['msft'] + 1000
	
	if data['type'] == 'book':
		symbol = data['symbol'].lower()
		if symbol == 'xlk':
			bids = data['buy']
			asks = data['sell']
			for price, size in asks:
				if price - constituents > MARGIN:
					trades.append((symbol, price, size, False))
			for price, size in bids:
				if constituents - price > MARGIN:
					trades.append((symbol, price, size, True))
		
			if abs(10 * data[''] - constituents) > MARGIN:
				
			
			
			
