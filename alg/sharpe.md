


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


















































`
































