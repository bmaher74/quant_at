

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     df = pd.read_csv(z.open('EDOLLAR_price.csv'), index_col=0,parse_dates=True )

fast_ewma = pd.ewma(df.PRICE, span=32)
slow_ewma = pd.ewma(df.PRICE, span=128)
raw_ewmac = fast_ewma - slow_ewma
vol = util.robust_vol_calc(df.PRICE.diff())
forecast = raw_ewmac /  vol 

print util.sharpe(df.PRICE, forecast)
```

```text
0.508384873452
```

```python
import util, zipfile, pandas as pd

def ewma(price, slow, fast):
   fast_ewma = pd.ewma(df.PRICE, span=slow)
   slow_ewma = pd.ewma(df.PRICE, span=fast)
   raw_ewmac = fast_ewma - slow_ewma
   vol = util.robust_vol_calc(price.diff())
   return raw_ewmac /  vol 

res = []
slow=32;fast=128
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     for x in  z.namelist():
     	 if '_price' in x:
	    df = pd.read_csv(z.open(x), index_col=0,parse_dates=True )
	    tmp = ewma(df.PRICE, slow, fast)
	    res.append(tmp)
	    
tmp = pd.DataFrame(pd.concat(res))
tmp.columns = ['forecast']
#tmp.loc[tmp.forecast<-20,'forecast']=-20
#tmp.loc[tmp.forecast>20,'forecast']=20
print util.estimate_forecast_scalar(tmp).tail()
```

```text
DATETIME
2016-05-05    2.841221
2016-05-06    2.841235
2016-05-09    2.841248
2016-05-10    2.841261
2016-05-11    2.841273
Name: forecast, dtype: float64
```
mine

8,32 6.09
2,8 12.22
4,16 8.91
32,128 2.8

book

# 2,8 10.6
# 4,16 7.5
# 8,32 5.3
# 16,64 3.75
# 32,128 2.65
# 64,256 1.87

pysys

#64_256 1.68
#32_128 2.57
#2_8 12.22













































`
































