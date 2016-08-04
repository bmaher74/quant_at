
```python
import util, zipfile, pandas as pd
import sys; sys.path.append('../data')
import futures, collections
ewmacs = [(16,64),(32,128),(64,256)]

forecasts = collections.OrderedDict()
for x in ewmacs: forecasts[x] = []
forecasts['carry'] = []
prices = collections.OrderedDict()
for x in ewmacs: prices[x] = []
prices['carry'] = []

insts = ['CORN', 'EDOLLAR', 'EUROSTX', 'MXP', 'US10', 'V2X']
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
    for inst in insts: 
        df1 = pd.read_csv(z.open('%s_price.csv' % inst), index_col=0,parse_dates=True )     
        df2 = pd.read_csv(z.open('%s_carrydata.csv' % inst), index_col=0,parse_dates=True )     
        for (fast,slow) in ewmacs:
             vol = util.robust_vol_calc(df1.PRICE.diff())
             forecasts[(fast,slow)].append(util.ewma(df1.PRICE, fast, slow))
             prices[(fast,slow)].append(df1.PRICE)

        raw_carry = df2.CARRY_CONTRACT-df2.PRICE_CONTRACT
        carryoffset = df2.PRICE_CONTRACT - df2.CARRY_CONTRACT
        forecast =  util.carry(raw_carry, vol,  carryoffset*1/util.CALENDAR_DAYS_IN_YEAR)
        forecasts['carry'].append(forecast)
        prices['carry'].append(df1.PRICE)
    
for x in forecasts:
    forecasts[x] = pd.concat(forecasts[x])
for x in prices:
    prices[x] = pd.concat(prices[x])
    
df1 = pd.DataFrame()
for x in forecasts: df1[x] = forecasts[x]
df2 = pd.DataFrame()
for x in prices: df2[x] = prices[x]
df2 = df2.shift(1)

rng = pd.date_range('1/1/1900', periods=len(df1), freq='D')

df1 = df1.set_index(rng)
df2 = df2.set_index(rng)
df1.to_csv("outfore.csv")
df2.to_csv("outpri.csv")
```





















```python
df = futures.get_stitched("ED", "CME")
df.sprice.plot()
plt.savefig('misc_01.png')
print df.head()
```

```text
           carrycont  carryprice effcont  effprice  sprice
Date                                                      
1987-06-18    198806         NaN  198809       NaN   71.76
1987-06-19    198806         NaN  198809       NaN   71.77
1987-06-22    198806         NaN  198809       NaN   71.84
1987-06-23    198806         NaN  198809       NaN   71.84
1987-06-24    198806         NaN  198809       NaN   71.76
```


```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dftmp = pd.read_csv(z.open('CORN_price.csv'), index_col=0,parse_dates=True )     
dftmp[dftmp.index > '1987-06-01'].PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)


```python
raw_carry = df.carryprice-df.effprice
vol = util.robust_vol_calc(df.effprice.diff())
carryoffset = -3
forecast =  util.carry(raw_carry, vol,  carryoffset*1/util.CALENDAR_DAYS_IN_YEAR)
```




