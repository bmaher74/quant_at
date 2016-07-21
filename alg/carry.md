
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures    
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
ins = "CL"
#ins = "FV"
roll = insts['rollcycle'][ins]
rolloff = insts['rolloffset'][ins]
expday = insts['expday'][ins]
expmon = insts['expmon'][ins]
carryoff = int(insts['carryoffset'][ins])
```

```python
ctd = futures.get_contracts("CME",ins,2007,2013)
```

```python
res2 = futures.which_contract(ins, ctd, roll, rolloff, expday, expmon)
res2.to_csv("out2.csv")
```

```python
res3 = futures.create_carry(res2[pd.isnull(res2.effcont)==False],carryoff,ctd)
print res3.head()
res3.to_csv("out3.csv")
```

```text
           effcont carrycont  effprice  carryprice
2004-08-23  200412    200411       NaN         NaN
2004-08-24  200412    200411       NaN         NaN
2004-08-25  200412    200411       NaN         NaN
2004-08-26  200412    200411       NaN         NaN
2004-08-27  200412    200411       NaN         NaN
```

```python
import util
raw_carry = res3.carryprice-res3.effprice
vol = util.robust_vol_calc(res3.effprice.diff())

def carry(daily_ann_roll, vol, diff_in_years, smooth_days=90):
    ann_stdev = vol * util.ROOT_BDAYS_INYEAR
    raw_carry = daily_ann_roll / ann_stdev
    smooth_carry = pd.ewma(raw_carry, smooth_days) / diff_in_years
    return smooth_carry.fillna(method='ffill')

resc =  carry(raw_carry, vol,  carryoff*1/util.CALENDAR_DAYS_IN_YEAR)
print resc.tail()
resc.to_csv("out5.csv")
print util.sharpe(res3.effprice, resc)
```

```text
2012-09-21    3.774181
2012-09-24    3.792665
2012-09-25    3.816581
2012-09-26    3.844538
2012-09-27    3.869225
dtype: float64
0.40103374339
```

```python
tmp = res2.effcont.dropna().astype(int).diff().dropna()
rolldates = tmp[tmp > 0].index
rollconts = np.unique(res2.effcont.dropna())
print rolldates
print rollconts
#df_stitched = futures.stitch_prices([ctd[x] for x in rollconts], 's', rolldates)
```

```text
DatetimeIndex(['2004-10-07', '2005-10-07', '2006-10-06', '2007-10-08',
               '2008-10-07', '2009-10-07', '2010-10-07', '2011-10-07'],
              dtype='datetime64[ns]', freq=None)
['200412' '200512' '200612' '200712' '200812' '200912' '201012' '201112'
 '201212']
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
for monthly 0.083 (=1/12).

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
 
 

