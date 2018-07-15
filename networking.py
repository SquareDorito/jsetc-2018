#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function
from bot import Bot
from argparse import ArgumentParser

import sys
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="TEAMJONATHAN"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    return s.makefile('rw', 1)

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

def write_to_exchange(exchange, obj):
        json.dump(obj, exchange)
        exchange.write("\n")

# ~~~~~============== MAIN LOOP ==============~~~~~

class Position():
    def __init__(self):
        self.securities = {
            'usd': 0,
            'goog': 0,
            'aapl': 0,
            'baba': 0,
            'babz': 0,
            'msft': 0,
            'bond': 0,
            'xlk': 0
        }
    def get(self, sym):
        return self.securities[sym.lower()]
    
    def update(self, sym, delta):
        self.securities[sym.lower()] += delta
    
    
    def __repr__(self):
        return str(self.securities)

def main(test_mode, srv):
    # This setting changes which test exchange is connected to.
    # 0 is prod-like
    # 1 is slower
    # 2 is empty
    if test_mode:
        print('IN TEST MODE')
    test_exchange_index=srv

    port=25000 + (test_exchange_index if test_mode else 0)

    exchange = None
    if test_mode:
        exchange = connect('test-exch-' + team_name, port)
    else:
        exchange = connect('production', 25000)
    
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    p = Position()
    b = Bot(exchange, test_mode)
    while True:
        data = read_from_exchange(exchange)
        data_type = data['type']
        while data_type in ['fill', 'ack', 'reject']:
            print(data)
            if data_type == 'fill':
                # check if an xlk order went through
                if b.xlks.get(data['order_id']):
                    b.limits['XLK'][0 if data['dir'] == 'BUY' else 1] -= data['size']

                delta = 1 if data['dir'] == 'SELL' else -1
                sym = data['symbol']
                
                p.update(sym, -1 * delta * data['size'])
                p.update('usd', delta * data['size'] * data['price'])
                print(p)  
            elif data_type == 'reject':
                id = data['order_id']
                if b.conversions.get(id):
                    del b.conversions[id]
                print(p)
            elif data_type == 'ack':
                id = data['order_id']
                if b.conversions.get(id):
                    sym, size, buy = b.conversions[id]
                    d = 1 if buy else -1
                    p.update(sym, d * size)
                    if sym == 'XLK':
                        p.update('goog', d * -2 * size/10)
                        p.update('aapl', d * -2 * size/10)
                        p.update('msft', d * -3 * size/10)
                        p.update('bond', d * -3 * size/10)
                    if sym == 'BABA':
                        p.update('babz', -1 * d * size)
                    del b.conversions[id]

            data = read_from_exchange(exchange)
            data_type = data['type']

        if test_mode:
            print('run')
            b.test_run(data, p)
        else:
            b.run(data, p)
     

if __name__ == "__main__":
    parser = ArgumentParser('etc')
    parser.add_argument('--test', action='store_true', default=False)
    parser.add_argument('--serv', action='store', type=int, default=0)
    args = parser.parse_args()
    main(args.test, args.serv)
