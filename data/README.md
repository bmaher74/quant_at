# INTRODUCTION

[Stock and Future Data Retrival are being reworked. Please stay tuned]

[Futures download is complete, stitching is in progress]

This folder will contain a Python / MongoDB based database /
downloader for financial data. It will do this from the open sources,
be able to update itself incrementally.

## Requirements

`conda install` or `pip install`

* pandas
* scipy
* numpy
* pymongo 3.x 
* quandl

## Data

Symbols are retrieved from seperate csv files under `data`
folder. [Details](data/README.md).

* simple.csv: Stock, ETF data.
* futures.csv: Commodity Futures.
* hft.csv: High-frequency data in 5-minute bars.
* earnings.csv: List of companies announcing their earnings per day.

Composite unique Id for stock ticker is comprised of the symbol `sym`
and the date `dt`.

Futures data is retrieved from Quandl; we use their API access, for
which you need to create a `.quandl` file with the API access key in
it (no newlines) under your home directory.

## Usage

Simplest usage for mass download is `python simple.py`. This will read
all symbols from under `data` and start downloading them. Same for
`python futures.py`.

For parallel execution, we provided a chunking ability [TBD],

```
python simple.py 0 4
```

This divides the symbol list into 4 chunks, and processes the 0th one
(it could have been 1,2,etc). For parallel execution 4 processes of
`simple.py` would be started, each for / using a different chunk number.
These processes would ideally be run under a monitoring tool, we
prefer [dand][1]. A sample configuration for this tool can be found in
[dand.conf](dand.conf) which can simply be executed with `python
dand.py dand.conf`.

Parallel inserts into Mongo are no problem, both in terms of
scalability and collisions; key value stores are particularly good at
parallel inserts, and since we are dividing the symbol list
before handing it over to a processor, no two processes can insert or
update on the same unique id. 

For research, data exploration purposes, there is a utility
function. To see all data for symbol DIJA,

```
import simple
df = simple.get("DJIA")
```

For multiple symbols in one Dataframe,

```
df = simple.get_multi(['DJIA','GOOG'])
```

This returns a Pandas dataframe which can be processes, plotted.

A simple query from mongo shell to see all tickers

```
use simple
db.tickers.count()
```

Show a certain amount of tickers

```
db.tickers.find().limit(10)
```

Show all records for a symbol and market

```
db.tickers.find({"_id.sym": "CL", "_id.market": "CME"})
db.tickers.find({"_id.sym": "CL", "_id.market": "CME"}).sort({ "_id.month": 1 })
```

To see all earnings announcements for a particular date, use

```
db.earnings.find( {"_id": 20110126 } )
```

which gives all announcements as a list of tuples for January 26, 2011. 

For some symbols we retrieve high-frequency data. Minute level tick
data for a symbol and specific day can be accessed with,

```
df = simple.get_hft("AHP", 20160213)
```

## Indexing

In the case of composite Ids, indexes might not be created properly in
MongoDB. In this case, simply create them with

```
db.tickers.create_index("_id")
```

To check indexing is working properly

```
print db.tickers.find( {"_id.sym": "DDD", "_id.dt": 20070101 } ).limit(1).explain()
```

Drop database

```
use findb
db.dropDatabase()
```

This should say something about BTrees, and indicate the table is not
fully scanned. 

[1]: https://github.com/burakbayramli/kod/tree/master/dand

[2]: https://www.stlouisfed.org

