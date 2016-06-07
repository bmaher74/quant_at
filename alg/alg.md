

```python
my_curr = 'USD'
vol_target = 0.20
capital = 250*1000
exchange = {'USD': {'EUR': 1.1, 'USD': 1.0} }
daily_vol_target = capital * vol_target / 16
print daily_vol_target
```

```text
3125.0
```

```python
f = 'legacycsv.zip'
import pandas as pd, zipfile
dfs = {}; vol = {}
instruments = ['CRUDE_W','EDOLLAR','US5','EUROSTX','V2X','MXP','CORN']
with zipfile.ZipFile(f, 'r') as z:
    for i in instruments:
         dfs[i] = pd.read_csv(z.open('%s_price.csv' % i), index_col=0,parse_dates=True )
         vol[i] = pd.rolling_std(dfs[i].pct_change()*100., window=25)
```

```python
insdf = pd.read_csv('instruments.csv',index_col=0)
dt = '2014-10-14'
res = []
cols = ['ins','price','vol','val_block','vol_block','units']
for i in instruments:
    price = float(dfs[i].ix[dt])
    v = float(vol[i].ix[dt])
    block_val = price * insdf.ix[i].block_value / 100.
    block_vol = block_val*v
    inst_value_vol =  block_vol*exchange[my_curr][insdf.ix[i].currency]
    units = daily_vol_target / inst_value_vol
    res.append([i, price, v, block_val, block_vol, units])
print pd.DataFrame(res,columns=cols)
```

```text
       ins       price       vol    val_block    vol_block      units
0  CRUDE_W    85.30000  1.267823   853.000000  1081.452940   2.889631
1  EDOLLAR    97.05500  0.056344  2426.375000   136.710705  22.858488
2      US5   117.06250  0.169945  1170.625002   198.941330  15.708149
3  EUROSTX  2816.00000  1.191740   281.600000   335.593983   8.465316
4      V2X    22.80000  2.689760    22.800000    61.326519  46.324317
5      MXP     0.07175  0.511001   358.750000   183.321447  17.046560
6     CORN   422.75000  1.247487   211.375000   263.687540  11.851148
```



```python
# 20150123
import sys; sys.path.append('../data')
import futures
res = futures.get_prices(market="EUREX", sym="FESX", month="H", year=2015,  db="findb")
res = [x['s'] for x in res if x['_id']['dt'] < 20150123]
df = pd.DataFrame(res)
df['d'] = df.diff()
df['d1'] = df.d.shift(1)
print 2 * np.sqrt(-1*df.d.cov(df.d1))
```

```text
26.7176250667
```

```python
import roll
rm = roll.RollModel()
res = np.array(res)
for samp in res:
    rm.addSample( samp )
print "uncertainty in measured fair (closing) price= ", 2*rm.get_c()
print "uncertainty in fair price (overnight move) dynamics= ", rm.get_sigmau2()
```

```text
uncertainty in measured fair (closing) price=  26.6274319871
uncertainty in fair price (overnight move) dynamics=  1269.44993289
```





























