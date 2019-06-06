# binance-data

### Installation

binance-data requires [Python](https://www.python.org/) v3.6+ to run.

Install via pip

```sh
pip install binance-data
```
### Example
Store data for all available pairs from Binance listing date thru current date to csv's:

```python
from binance_data import DataClient

pair_list = DataClient().get_binance_pairs()
store_data = DataClient().kline_data(pair_list,'1m')
```



### Todos

 - Complete README
 - Write Tests
 - Add SQL Storage
 

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
