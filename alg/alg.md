
A Eurodollar future represents the cost of nominally borrowing $1 million for
three months and is priced at 100 minus the annual interest rate. If the price
rises by 1% from 98.00 to 98.98 then the rate of interest payable has fallen
from 2% to 1.02%. Because three months is a quarter of a year you will have
saved $1 million × 0.98% × 0.25 = $2,450 in interest on your loan. The block
value is $2,450.1

(98*1.01 - 98.) * 0.25 * 1000 * 1000 / 100.

2450.0

```python
eq = "(x*1.01 - x) * 0.25 * 1000 * 1000 / 100."
func = lambda x: eval(eq)
print func(98)
```

```text
2450.0
```


```python
vol_target = 0.20
capital = 250*1000
exchange = {'USD': {'EUR': 1.1}}
daily_vol_target = capital * vol_target / 16
print daily_vol_target
```

```text
3125.0
```

```python
f = 'c:/Users/burak/Downloads/legacycsv.zip'
import pandas as pd, zipfile
dfs = {}; vol = {}
instruments = ['CRUDE_W','EDOLLAR','US5','EUROSTX','V2X','MXP','CORN']
with zipfile.ZipFile(f, 'r') as z:
    for i in instruments:
         dfs[i] = pd.read_csv(z.open('%s_price.csv' % i), index_col=0,parse_dates=True )
         vol[i] = pd.rolling_std(dfs[i].pct_change()*100., window=25)
         #vol[i] = pd.ewmstd(dfs[i].pct_change()*100., span=36)
```

```python
dt = '2014-10-14'
for i in instruments: print i, float(dfs[i].ix[dt]), float(vol[i].ix[dt])
```

```text
CRUDE_W 85.3 1.2678229074
EDOLLAR 97.055 0.0563436010408
US5 117.06250025 0.169944541824
EUROSTX 2816.0 1.19173999773
V2X 22.8 2.68975960664
MXP 0.07175 0.511000548817
CORN 422.75 1.24748688385
```













































