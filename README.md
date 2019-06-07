# binance-data
[![PyPI version](https://badge.fury.io/py/binance-data.svg)](https://badge.fury.io/py/binance-data)
[![Build Status](https://travis-ci.org/uneasyguy/binance_data.svg?branch=master)](https://travis-ci.org/uneasyguy/binance_data)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/binance-data.svg)

### Installation

binance-data requires [Python](https://www.python.org/) v3.6+ to run.

Install via pip

```sh
pip install binance-data
```
## Quick Start Example:
Store data for all available pairs from Binance listing date thru current date to csv's:

```python
from binance_data import DataClient

pair_list = DataClient().get_binance_pairs()
store_data = DataClient().kline_data(pair_list,'1m')
```
## Usage:
### get_binance_pairs()
**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
base_currencies | LIST | NO |List of base currencies to search for
quote_currencies| LIST| NO | List of quote currencies to search for

### kline_data()
**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
pair_list | LIST | YES |List of currencies pairs to pull data for
interval| STRING| YES | Options: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h'
start_date|STRING|NO|Date to start pulling data from in MM/DD/YYYY format. If not provided and not previously ran will default to original listing date, else if not provided, and previously stored data exists, will erase data for the final day previously pulled and pick up from there
end_date|STRING|NO|Date to end data pull at in MM/DD/YYYY format. If not provided, will default to now.
storage|LIST|NO|Currently only supports CSV storage, SQL storage to come in future updates. Also allows to set intended storage directory by providing full fill path (if not provided, will create storage directories inside current directory). Example: storage=['csv','/home/user/kline_data/']
output|LIST|NO|Defaults to ['Opened','High','Low','Close','Volume','Closed'] if not provided (with Opened and Closed representing timestamps). Options include: Opened, High, Low, Close, Volume, Closed, Quote Asset Volume, Total Trades, Taker Buy Base Asset Volume,Taker Buy Quote Asset Volume
progress_statements|Boolean|NO|Defaults to False. If set to True, will output print statements to screen to keep you apprised of progress

## Examples:
***Example 1:***
```python
from binance_data.client import DataClient

pair_list = DataClient().get_binance_pairs(base_currencies=['BTC','XRP'],quote_currencies=['ETH','NEO','TRX'])
```
**Response:**
```python
['ETHBTC', 'NEOBTC', 'TRXBTC', 'TRXXRP']
```
***Example 2:***
```python
from binance_data.client import DataClient

pair_list = DataClient().get_binance_pairs(quote_currencies=['ETH','NEO','TRX'])
```
**Response:**
```python
['ETHBTC', 'NEOBTC', 'ETHUSDT', 'NEOETH', 'TRXBTC', 'TRXETH', 'NEOUSDT', 'NEOBNB', 'ETHTUSD', 'TRXBNB', 'TRXUSDT', 'ETHPAX', 'ETHUSDC', 'TRXTUSD', 'NEOTUSD', 'TRXXRP', 'TRXPAX', 'TRXUSDC', 'NEOPAX', 'NEOUSDC']
```
***Example 3:***
```python
from binance_data.client import DataClient

pair_list = DataClient().get_binance_pairs(base_currencies=['ETH'])
```
**Response:**
```python
['QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BNBETH', 'OAXETH', 'DNTETH', 'MCOETH', 'ICNETH', 'WTCETH', 'LRCETH', 'OMGETH', 'ZRXETH', 'STRATETH', 'SNGLSETH', 'BQXETH', 'KNCETH', 'FUNETH', 'SNMETH', 'NEOETH', 'IOTAETH', 'LINKETH', 'XVGETH', 'SALTETH', 'MDAETH', 'MTLETH', 'SUBETH', 'ETCETH', 'MTHETH', 'ENGETH', 'ZECETH', 'ASTETH', 'DASHETH', 'BTGETH', 'EVXETH', 'REQETH', 'VIBETH', 'HSRETH', 'TRXETH', 'POWRETH', 'ARKETH', 'YOYOETH', 'XRPETH', 'MODETH', 'ENJETH', 'STORJETH', 'VENETH', 'KMDETH', 'RCNETH', 'NULSETH', 'RDNETH', 'XMRETH', 'DLTETH', 'AMBETH', 'BCCETH', 'BATETH', 'BCPTETH', 'ARNETH', 'GVTETH', 'CDTETH', 'GXSETH', 'POEETH', 'QSPETH', 'BTSETH', 'XZCETH', 'LSKETH', 'TNTETH', 'FUELETH', 'MANAETH', 'BCDETH', 'DGDETH', 'ADXETH', 'ADAETH', 'PPTETH', 'CMTETH', 'XLMETH', 'CNDETH', 'LENDETH', 'WABIETH', 'LTCETH', 'TNBETH', 'WAVESETH', 'GTOETH', 'ICXETH', 'OSTETH', 'ELFETH', 'AIONETH', 'NEBLETH', 'BRDETH', 'EDOETH', 'WINGSETH', 'NAVETH', 'LUNETH', 'TRIGETH', 'APPCETH', 'VIBEETH', 'RLCETH', 'INSETH', 'PIVXETH', 'IOSTETH', 'CHATETH', 'STEEMETH', 'NANOETH', 'VIAETH', 'BLZETH', 'AEETH', 'RPXETH', 'NCASHETH', 'POAETH', 'ZILETH', 'ONTETH', 'STORMETH', 'XEMETH', 'WANETH', 'WPRETH', 'QLCETH', 'SYSETH', 'GRSETH', 'CLOAKETH', 'GNTETH', 'LOOMETH', 'BCNETH', 'REPETH', 'TUSDETH', 'ZENETH', 'SKYETH', 'CVCETH', 'THETAETH', 'IOTXETH', 'QKCETH', 'AGIETH', 'NXSETH', 'DATAETH', 'SCETH', 'NPXSETH', 'KEYETH', 'NASETH', 'MFTETH', 'DENTETH', 'ARDRETH', 'HOTETH', 'VETETH', 'DOCKETH', 'PHXETH', 'HCETH', 'PAXETH']
```
***Example 4:***
```python
from binance_data.client import DataClient

pair_list = DataClient().get_binance_pairs()
```
**Response:**
```python
['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BCCBTC', 'GASBTC', 'BNBETH', 'BTCUSDT', 'ETHUSDT', 'HSRBTC', 'OAXETH', 'DNTETH', 'MCOETH', 'ICNETH', 'MCOBTC', 'WTCBTC', 'WTCETH', 'LRCBTC', 'LRCETH', 'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'OMGETH', 'ZRXBTC', 'ZRXETH', 'STRATBTC', 'STRATETH', 'SNGLSBTC', 'SNGLSETH', 'BQXBTC', 'BQXETH', 'KNCBTC', 'KNCETH', 'FUNBTC', 'FUNETH', 'SNMBTC', 'SNMETH', 'NEOETH', 'IOTABTC', 'IOTAETH', 'LINKBTC', 'LINKETH', 'XVGBTC', 'XVGETH', 'SALTBTC', 'SALTETH', 'MDABTC', 'MDAETH', 'MTLBTC', 'MTLETH', 'SUBBTC', 'SUBETH', 'EOSBTC', 'SNTBTC', 'ETCETH', 'ETCBTC', 'MTHBTC', 'MTHETH', 'ENGBTC', 'ENGETH', 'DNTBTC', 'ZECBTC', 'ZECETH', 'BNTBTC', 'ASTBTC', 'ASTETH', 'DASHBTC', 'DASHETH', 'OAXBTC', 'ICNBTC', 'BTGBTC', 'BTGETH', 'EVXBTC', 'EVXETH', 'REQBTC', 'REQETH', 'VIBBTC', 'VIBETH', 'HSRETH', 'TRXBTC', 'TRXETH', 'POWRBTC', 'POWRETH', 'ARKBTC', 'ARKETH', 'YOYOETH', 'XRPBTC', 'XRPETH', 'MODBTC', 'MODETH', 'ENJBTC', 'ENJETH', 'STORJBTC', 'STORJETH', 'BNBUSDT', 'VENBNB', 'YOYOBNB', 'POWRBNB', 'VENBTC', 'VENETH', 'KMDBTC', 'KMDETH', 'NULSBNB', 'RCNBTC', 'RCNETH', 'RCNBNB', 'NULSBTC', 'NULSETH', 'RDNBTC', 'RDNETH', 'RDNBNB', 'XMRBTC', 'XMRETH', 'DLTBNB', 'WTCBNB', 'DLTBTC', 'DLTETH', 'AMBBTC', 'AMBETH', 'AMBBNB', 'BCCETH', 'BCCUSDT', 'BCCBNB', 'BATBTC', 'BATETH', 'BATBNB', 'BCPTBTC', 'BCPTETH', 'BCPTBNB', 'ARNBTC', 'ARNETH', 'GVTBTC', 'GVTETH', 'CDTBTC', 'CDTETH', 'GXSBTC', 'GXSETH', 'NEOUSDT', 'NEOBNB', 'POEBTC', 'POEETH', 'QSPBTC', 'QSPETH', 'QSPBNB', 'BTSBTC', 'BTSETH', 'BTSBNB', 'XZCBTC', 'XZCETH', 'XZCBNB', 'LSKBTC', 'LSKETH', 'LSKBNB', 'TNTBTC', 'TNTETH', 'FUELBTC', 'FUELETH', 'MANABTC', 'MANAETH', 'BCDBTC', 'BCDETH', 'DGDBTC', 'DGDETH', 'IOTABNB', 'ADXBTC', 'ADXETH', 'ADXBNB', 'ADABTC', 'ADAETH', 'PPTBTC', 'PPTETH', 'CMTBTC', 'CMTETH', 'CMTBNB', 'XLMBTC', 'XLMETH', 'XLMBNB', 'CNDBTC', 'CNDETH', 'CNDBNB', 'LENDBTC', 'LENDETH', 'WABIBTC', 'WABIETH', 'WABIBNB', 'LTCETH', 'LTCUSDT', 'LTCBNB', 'TNBBTC', 'TNBETH', 'WAVESBTC', 'WAVESETH', 'WAVESBNB', 'GTOBTC', 'GTOETH', 'GTOBNB', 'ICXBTC', 'ICXETH', 'ICXBNB', 'OSTBTC', 'OSTETH', 'OSTBNB', 'ELFBTC', 'ELFETH', 'AIONBTC', 'AIONETH', 'AIONBNB', 'NEBLBTC', 'NEBLETH', 'NEBLBNB', 'BRDBTC', 'BRDETH', 'BRDBNB', 'MCOBNB', 'EDOBTC', 'EDOETH', 'WINGSBTC', 'WINGSETH', 'NAVBTC', 'NAVETH', 'NAVBNB', 'LUNBTC', 'LUNETH', 'TRIGBTC', 'TRIGETH', 'TRIGBNB', 'APPCBTC', 'APPCETH', 'APPCBNB', 'VIBEBTC', 'VIBEETH', 'RLCBTC', 'RLCETH', 'RLCBNB', 'INSBTC', 'INSETH', 'PIVXBTC', 'PIVXETH', 'PIVXBNB', 'IOSTBTC', 'IOSTETH', 'CHATBTC', 'CHATETH', 'STEEMBTC', 'STEEMETH', 'STEEMBNB', 'NANOBTC', 'NANOETH', 'NANOBNB', 'VIABTC', 'VIAETH', 'VIABNB', 'BLZBTC', 'BLZETH', 'BLZBNB', 'AEBTC', 'AEETH', 'AEBNB', 'RPXBTC', 'RPXETH', 'RPXBNB', 'NCASHBTC', 'NCASHETH', 'NCASHBNB', 'POABTC', 'POAETH', 'POABNB', 'ZILBTC', 'ZILETH', 'ZILBNB', 'ONTBTC', 'ONTETH', 'ONTBNB', 'STORMBTC', 'STORMETH', 'STORMBNB', 'QTUMBNB', 'QTUMUSDT', 'XEMBTC', 'XEMETH', 'XEMBNB', 'WANBTC', 'WANETH', 'WANBNB', 'WPRBTC', 'WPRETH', 'QLCBTC', 'QLCETH', 'SYSBTC', 'SYSETH', 'SYSBNB', 'QLCBNB', 'GRSBTC', 'GRSETH', 'ADAUSDT', 'ADABNB', 'CLOAKBTC', 'CLOAKETH', 'GNTBTC', 'GNTETH', 'GNTBNB', 'LOOMBTC', 'LOOMETH', 'LOOMBNB', 'XRPUSDT', 'BCNBTC', 'BCNETH', 'BCNBNB', 'REPBTC', 'REPETH', 'REPBNB', 'BTCTUSD', 'TUSDBTC', 'ETHTUSD', 'TUSDETH', 'TUSDBNB', 'ZENBTC', 'ZENETH', 'ZENBNB', 'SKYBTC', 'SKYETH', 'SKYBNB', 'EOSUSDT', 'EOSBNB', 'CVCBTC', 'CVCETH', 'CVCBNB', 'THETABTC', 'THETAETH', 'THETABNB', 'XRPBNB', 'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'IOTXBTC', 'IOTXETH', 'QKCBTC', 'QKCETH', 'AGIBTC', 'AGIETH', 'AGIBNB', 'NXSBTC', 'NXSETH', 'NXSBNB', 'ENJBNB', 'DATABTC', 'DATAETH', 'ONTUSDT', 'TRXBNB', 'TRXUSDT', 'ETCUSDT', 'ETCBNB', 'ICXUSDT', 'SCBTC', 'SCETH', 'SCBNB', 'NPXSBTC', 'NPXSETH', 'VENUSDT', 'KEYBTC', 'KEYETH', 'NASBTC', 'NASETH', 'NASBNB', 'MFTBTC', 'MFTETH', 'MFTBNB', 'DENTBTC', 'DENTETH', 'ARDRBTC', 'ARDRETH', 'ARDRBNB', 'NULSUSDT', 'HOTBTC', 'HOTETH', 'VETBTC', 'VETETH', 'VETUSDT', 'VETBNB', 'DOCKBTC', 'DOCKETH', 'POLYBTC', 'POLYBNB', 'PHXBTC', 'PHXETH', 'PHXBNB', 'HCBTC', 'HCETH', 'GOBTC', 'GOBNB', 'PAXBTC', 'PAXBNB', 'PAXUSDT', 'PAXETH', 'RVNBTC', 'RVNBNB', 'DCRBTC', 'DCRBNB', 'USDCBNB', 'USDCBTC', 'MITHBTC', 'MITHBNB', 'BCHABCBTC', 'BCHSVBTC', 'BCHABCUSDT', 'BCHSVUSDT', 'BNBPAX', 'BTCPAX', 'ETHPAX', 'XRPPAX', 'EOSPAX', 'XLMPAX', 'RENBTC', 'RENBNB', 'BNBTUSD', 'XRPTUSD', 'EOSTUSD', 'XLMTUSD', 'BNBUSDC', 'BTCUSDC', 'ETHUSDC', 'XRPUSDC', 'EOSUSDC', 'XLMUSDC', 'USDCUSDT', 'ADATUSD', 'TRXTUSD', 'NEOTUSD', 'TRXXRP', 'XZCXRP', 'PAXTUSD', 'USDCTUSD', 'USDCPAX', 'LINKUSDT', 'LINKTUSD', 'LINKPAX', 'LINKUSDC', 'WAVESUSDT', 'WAVESTUSD', 'WAVESPAX', 'WAVESUSDC', 'BCHABCTUSD', 'BCHABCPAX', 'BCHABCUSDC', 'BCHSVTUSD', 'BCHSVPAX', 'BCHSVUSDC', 'LTCTUSD', 'LTCPAX', 'LTCUSDC', 'TRXPAX', 'TRXUSDC', 'BTTBTC', 'BTTBNB', 'BTTUSDT', 'BNBUSDS', 'BTCUSDS', 'USDSUSDT', 'USDSPAX', 'USDSTUSD', 'USDSUSDC', 'BTTPAX', 'BTTTUSD', 'BTTUSDC', 'ONGBNB', 'ONGBTC', 'ONGUSDT', 'HOTBNB', 'HOTUSDT', 'ZILUSDT', 'ZRXBNB', 'ZRXUSDT', 'FETBNB', 'FETBTC', 'FETUSDT', 'BATUSDT', 'XMRBNB', 'XMRUSDT', 'ZECBNB', 'ZECUSDT', 'ZECPAX', 'ZECTUSD', 'ZECUSDC', 'IOSTBNB', 'IOSTUSDT', 'CELRBNB', 'CELRBTC', 'CELRUSDT', 'ADAPAX', 'ADAUSDC', 'NEOPAX', 'NEOUSDC', 'DASHBNB', 'DASHUSDT', 'NANOUSDT', 'OMGBNB', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICBNB', 'MATICBTC', 'MATICUSDT', 'ATOMBNB', 'ATOMBTC', 'ATOMUSDT', 'ATOMUSDC', 'ATOMPAX', 'ATOMTUSD', 'ETCUSDC', 'ETCPAX', 'ETCTUSD', 'BATUSDC', 'BATPAX', 'BATTUSD', 'PHBBNB', 'PHBBTC', 'PHBUSDC', 'PHBTUSD', 'PHBPAX', 'TFUELBNB', 'TFUELBTC', 'TFUELUSDT', 'TFUELUSDC', 'TFUELTUSD', 'TFUELPAX', 'ONEBNB', 'ONEBTC', 'ONEUSDT', 'ONETUSD', 'ONEPAX', 'ONEUSDC']

```

***Example 5:***
```python
from binance_data.client import DataClient

pair_list = DataClient().get_binance_pairs()
store_data = DataClient().kline_data(pair_list,'1m',start_date='06/01/2019',end_date='06/05/2019',storage=['csv','/home/user/kline_data/'],progress_statements=True)
```
### Todos

 - Complete README
 - Write Tests
 - Add SQL Storage
 - Add trade by trade data storage
 

License
----

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Python]: <https://www.python.org/>
   [git-repo-url]: <https://github.com/uneasyguy/binance_data.git>
