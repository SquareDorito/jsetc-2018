from .average import read_data
from collections import defaultdict

averageDict = defaultdict(int) # averages from the start
totalCountDict = defaultdict(int) # number of trades
windowDict = defaultdict(int) # last n prices
def etf(data, p, test):
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
			return
			
