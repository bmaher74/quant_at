
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures    
insts = pd.read_csv('instruments.csv',index_col=0).to_dict()
```

```python
#res = futures.get_contracts("CME","CL",2000,2010)
res = futures.get_contracts("CME","FV",2000,2010)
print len(res)
```

```text
40
```

```python
ins = "FV"
res2 = futures.which_contract("FV", res, insts['rollcycle'][ins], insts['rolloffset'][ins], insts['expiration'][ins])
```

```python
import datetime

def offset_contract(con, offset):
    s = pd.to_datetime(con, format='%Y%m')
    ss = s + datetime.timedelta(days=31*offset)
    return "%d%02d" % (ss.year, ss.month)
print offset_contract("200003", 2)
print offset_contract("200003", -4)

def create_carry(df, offset):
    print offset, df[1000:1010]
        
create_carry(res2, insts['carryoffset'][ins])
```

```text
-9            effcont
2003-06-30  200309
2003-07-01  200309
2003-07-02  200309
2003-07-03  200309
2003-07-04  200309
2003-07-07  200309
2003-07-08  200309
2003-07-09  200309
2003-07-10  200309
2003-07-11  200309
```












eurodollar
===================
2008-10-08
2009-01-07
2009-04-09
2009-07-10

* very liquid
* 40 months out

crude oil
===============
always hold december contract
rollover november 15

gold
========
In January I'd want to be in April Gold, so I can measure rolldown off
February. 70 days before April Gold expires I would then switch to
June Gold. 70 days before June Gold expires I would move to August
Gold, and so on.



```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     df = pd.read_csv(z.open('CRUDE_W_carrydata.csv'), index_col=0,parse_dates=True )
df = df[(df.index > '2008-06-01') & (df.index < '2011-01-01')]
```

```python
import sys; sys.path.append('../data')
import futures
res = futures.get_contract(market="CME", sym="CL", month="Z", year=2008)
print res.head(1)
```

```text
                h      l      o  oi      s  v
Date                                         
2001-11-21  21.29  21.29  21.29   0  21.29  0
```










The carry rule

EWMAC is a positive skew rule which needs prices to trend in one
direction or another.

There is an example of the carry trading rule in action in figure 19,
again showing crude oil futures during the great crash of 2008. The
price of the nearer futures contract dips below the contract we are
trading in mid-August.  This is a bearish carry signal and the rule
sells to enjoy some of the continuing fall in price.

Unfortunately it remains bearish long after the market has turned, but
you can’t win them all. It makes sense to combine diversifying trading
rules like the positive skew, trend following EWMAC rule, with a
negative skew carry rule.

* Futures: If not trading nearest contract (preferred)

Current contract price: The price of the contract you are trading.

Nearer contract price: The price of the next closest contract. So if
you are trading June 2017 Eurodollar it would be March 2017.

Price differential Current contract price minus nearer contract price.

Distance between contracts: The time in years between the two contracts
(current and nearer). For adjacent quarterly expiries it is 0.25 and
for monthly 0.083.

Net expected return in price units: You need to annualise the price
differential by dividing by the distance between contracts.

* Futures: If trading nearest contract (approximation)

Current contract price: The price of the contract you are trading.

Next contract price: The price of the contract with the next expiry. So
if you had June 2017 Treasury bonds it would be September 2017.

Price differential: Next contract price minus current contract price.

Distance between contracts: The time in years between the two contracts
(current and next). For adjacent quarterly expiries it would be 0.25,
for monthly 0.083 and so on.

Net expected return in price units: You need to annualise the price
differential by dividing by the distance between contracts.

* Forecast calculation

Net expected return in price units: From relevant information
above. Note this is an annualised measure.

Standard deviation of returns: This is the standard deviation of
returns in price points, not percentage points as normal. The
volatility in price points is equal to the percentage point volatility
(price volatility as defined in chapter ten, ‘Position sizing’, on
page 165), multiplied by the current price.

Annualised standard deviation of returns: Multiply the standard
deviation of returns by the ‘square root of time’ to annualise
it. Assuming 256 business days in a year you should multiply by 16.

Raw carry: Volatility standardised expected As I pointed out in
chapter seven, you want forecasts to be adjusted for return standard
deviation. So this is the net expected return in price units divided
by the annualised standard deviation of returns.

Forecast scalar: The forecast scalar is 30. I explain below where the
multiplier comes from.

Forecast: The forecast will be the forecast scalar times the raw
carry.

Capped forecast This is the forecast with values outside the range
-20, +20 capped.
 
Which forecast scalar to use?
The raw carry measure is effectively an annualised Sharpe ratio (SR),
an expected return divided by standard deviation. I used the technique
in appendix D and data from a large number of markets across different
asset classes to work out the right forecast scalar. This gives a
forecast scalar of around 30.

What is the turnover of carry?
It’s hard to generalise about the turnover (round trips per year) of
carry since it depends on the asset class and how often you update the
value of the forecast. I suggest checking the forecast weekly to avoid
spurious noise which can otherwise be a problem. If you do this then
it is reasonable to use a rule of thumb value of 10 for the turnover
of the carry rule.
 
 

