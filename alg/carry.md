
```python
import datetime
d1 = datetime.datetime(2016, 3, 24)
d2 = datetime.datetime(2016, 6, 20)
print (d2-d1).days 
```

```text
88
```


```python
import sys; sys.path.append('../data')
import futures       
res = futures.get_contracts("CME","CL",2000,2010)
```

```python
#res2 = futures.stitch_contracts(res, "out_40_months_every_90_days")
res2 = futures.stitch_contracts(res, "hold_dec_roll_nov")
print res2.tail()
res2.to_csv("out.csv")
```

```text
           contract
2009-11-16   201012
2009-11-17   201012
2009-11-18   201012
2009-11-19   201012
2009-11-20   201012
```

```python
import pandas as pd
inst = pd.read_csv('instruments.csv',index_col=0).to_dict()
print inst['carryoffset']['CL']

def create_carry(contract, contracts_list):
    print len(contracts_list)
    

create_carry("CL", res2)

```

```text
{'currency': {'EDOLLAR': 'USD', 'CL': 'USD', 'EUROSTX': 'EUR', 'CORN': 'USD', 'V2X': 'EUR', 'MXP': 'USD', 'US5': 'USD'}, 'block_value': {'EDOLLAR': 2500, 'CL': 1000, 'EUROSTX': 10, 'CORN': 50, 'V2X': 100, 'MXP': 500000, 'US5': 1000}, 'carryoffset': {'EDOLLAR': -3, 'CL': -1, 'EUROSTX': 3, 'CORN': -3, 'V2X': -1, 'MXP': 3, 'US5': -9}, 'slippage': {'EDOLLAR': 0.0025000000000000001, 'CL': 0.0145328653, 'EUROSTX': 0.5, 'CORN': 0.125, 'V2X': 0.025499999999999998, 'MXP': 1.1567000000000001e-05, 'US5': 0.0040000000000000001}}
-1
3197
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
 
 

