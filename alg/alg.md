
198

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
f = 'c:/Users/burak/Downloads/legacycsv.zip'
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
for i in instruments:
    price = float(dfs[i].ix[dt])
    v = float(vol[i].ix[dt])
    block_val = price * insdf.ix[i].block_value / 100.
    block_vol = block_val*v
    inst_value_vol =  block_vol*exchange[my_curr][insdf.ix[i].currency]
    print i, price, v, block_val, block_vol, daily_vol_target / inst_value_vol
```

```text
CRUDE_W 85.3 1.2678229074 853.0 1081.45294001 2.88963105501
EDOLLAR 97.055 0.0563436010408 2426.375 136.710704975 22.8584879331
US5 117.06250025 0.169944541824 1170.6250025 198.941329697 15.708148753
EUROSTX 2816.0 1.19173999773 281.6 335.59398336 8.46531592273
V2X 22.8 2.68975960664 22.8 61.3265190314 46.3243167194
MXP 0.07175 0.511000548817 358.75 183.321446888 17.0465597618
CORN 422.75 1.24748688385 211.375 263.687540074 11.8511477604
```







```python
print 75 * 1.33 * 1000 / 100.
print 25. * 50.
print 2500. * 0.5 * 10
```

```text
997.5
1250.0
12500.0
```
































