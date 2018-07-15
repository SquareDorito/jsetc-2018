from .simple_bond import simple_bond
from .average import average
from .etf_arbitrage import etf
from .adr_pair_trading import adr_pair

strategies = [simple_bond, average, etf]
test_strategies = [simple_bond, average, adr_pair]
