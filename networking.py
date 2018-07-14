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

def main(test_mode, srv):
    # This setting changes which test exchange is connected to.
    # 0 is prod-like
    # 1 is slower
    # 2 is empty
    test_exchange_index=0
    prod_exchange_hostname="production"

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
    b = Bot(exchange)
    while True:
        data = read_from_exchange(exchange)
        data_type = data['type']
        if data_type in ['fill', 'ack', 'reject']:
            print(data)
        b.run(data)


if __name__ == "__main__":
    parser = ArgumentParser('etc')
    parser.add_argument('--test', action='store_true', default=False)
    parser.add_argument('--serv', action='store_const', default=0)
    args = parser.parse_args()
    main(args.test, args.serv)
