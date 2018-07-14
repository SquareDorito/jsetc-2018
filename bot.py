from strategies import strategies

class Bot:

    def __init__(self):
        pass

    def run(self, data):
        for strategy in strategies:
            strategy(data)
