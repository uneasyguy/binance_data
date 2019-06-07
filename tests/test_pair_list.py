from binance_data.client import DataClient
import pytest

def test_single_pair_list():
	pair_list = DataClient().get_binance_pairs(base_currencies=['BTC'],quote_currencies=['ETH'])
	assert pair_list == ['ETHBTC']

def test_single_erroneous_pair():
	with pytest.raises(ValueError):
		pair_list = DataClient().get_binance_pairs(base_currencies=['NMN'],quote_currencies=['ETH'])

