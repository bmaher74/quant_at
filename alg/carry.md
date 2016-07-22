
```python
cols = ['High','Low','Open','Prev. Day Open Interest','Settle','Volume']
for dd in ctd.keys():
    year,mon = int(dd[:4]), futures.contract_month_codes[int(dd[-2:])-1]
    print year, mon
    #tmp = ctd[dd]
    #tmp.columns = cols
    #tmp.to_csv('../data/test/data_crude/CME-CL%s%d.csv' % (mon,year))
```

```text
2007 F
2007 G
2007 H
2007 J
2007 K
2007 M
2007 N
2007 Q
2007 U
2007 V
2007 X
2007 Z
2008 F
2008 G
2008 H
2008 J
2008 K
2008 M
2008 N
2008 Q
2008 U
2008 V
2008 X
2008 Z
2009 F
2009 G
2009 H
2009 J
2009 K
2009 M
2009 N
2009 Q
2009 U
2009 V
2009 X
2009 Z
2010 F
2010 G
2010 H
2010 J
2010 K
2010 M
2010 N
2010 Q
2010 U
2010 V
2010 X
2010 Z
2011 F
2011 G
2011 H
2011 J
2011 K
2011 M
2011 N
2011 Q
2011 U
2011 V
2011 X
2011 Z
2012 F
2012 G
2012 H
2012 J
2012 K
2012 M
2012 N
2012 Q
2012 U
2012 V
2012 X
2012 Z
```
















```python
import pandas as pd
import sys; sys.path.append('../data')
import futures    
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
ins = "CL"
roll = insts['rollcycle'][ins]
rolloff = insts['rolloffset'][ins]
expday = insts['expday'][ins]
expmon = insts['expmon'][ins]
carryoff = int(insts['carryoffset'][ins])
print roll, rolloff, expday,expmon,carryoff
```

```text
Z 50 25 prev -1
```

```python
ctd = futures.get_contracts("CME",ins,2007,2013)
print len(ctd)
```

```text
72
```

```python
res2 = futures.which_contract(ins, ctd, roll, rolloff, expday, expmon)
res2.to_csv("out2.csv")
```

```python
res3 = futures.create_carry(res2[pd.isnull(res2.effcont)==False],carryoff,ctd)
res3.to_csv("out3.csv")
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
resc.to_csv("out5.csv")
print util.sharpe(res3.effprice, resc)
```

```text
0.40103374339
```


```python
dfs = futures.stitch_contracts(res2, ctd, 's')
dfs.plot()
plt.savefig('carry_01.png')
```

![](carry_01.png)




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
 
 

