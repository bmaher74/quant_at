

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
cols = ['ins','price','vol','val_block','vol_block','units','exec_cost_per_block']
for i in instruments:
    price = float(dfs[i].ix[dt])
    v = float(vol[i].ix[dt])
    block_val = price * insdf.ix[i].block_value / 100.
    block_vol = block_val*v
    inst_value_vol =  block_vol*exchange[my_curr][insdf.ix[i].currency]
    units = daily_vol_target / inst_value_vol
    exec_cost = insdf.ix[i].slippage / price * 100 * block_val
    res.append([i, price, v, block_val, block_vol, units, exec_cost])
print pd.DataFrame(res,columns=cols)
```

```text
       ins       price       vol    val_block    vol_block      units  \
0  CRUDE_W    85.30000  1.267823   853.000000  1081.452940   2.889631   
1  EDOLLAR    97.05500  0.056344  2426.375000   136.710705  22.858488   
2      US5   117.06250  0.169945  1170.625002   198.941330  15.708149   
3  EUROSTX  2816.00000  1.191740   281.600000   335.593983   8.465316   
4      V2X    22.80000  2.689760    22.800000    61.326519  46.324317   
5      MXP     0.07175  0.511001   358.750000   183.321447  17.046560   
6     CORN   422.75000  1.247487   211.375000   263.687540  11.851148   

   exec_cost_per_block  
0            14.532865  
1             6.250000  
2             4.000000  
3             5.000000  
4             2.550000  
5             5.783500  
6             6.250000  
```

Turnover

```python
avg =  (df.price / 10).diff().abs().mean()
print avg * 256
```

```python
f = 'legacycsv.zip'
import pandas as pd, zipfile, util
with zipfile.ZipFile(f, 'r') as z:
     crdf = pd.read_csv(z.open('CRUDE_W_price.csv'), index_col=0,parse_dates=True )

fast_ewma = pd.ewma(crdf.PRICE, span=32)
slow_ewma = pd.ewma(crdf.PRICE, span=128)
raw_ewmac = fast_ewma - slow_ewma
vol = util.robust_vol_calc(crdf[['PRICE']].diff()).vol
pred = raw_ewmac /  vol
print pred.mean()
forecast_scalar = 10. / pred.mean()
print forecast_scalar
pred_scaled = pred * forecast_scalar
print pred_scaled.tail(20)
```

```text
0.996495521789
10.0351680277
DATETIME
2016-04-14   -17.212719
2016-04-15   -16.234287
2016-04-18   -15.826642
2016-04-19   -14.761395
2016-04-20   -13.042248
2016-04-21   -11.828032
2016-04-22   -10.526289
2016-04-25    -9.355273
2016-04-26    -7.821639
2016-04-27    -5.572717
2016-04-28    -3.544346
2016-04-29    -1.536177
2016-05-02    -0.141449
2016-05-03     0.714540
2016-05-04     1.446155
2016-05-05     2.348545
2016-05-06     3.489593
2016-05-09     3.611675
2016-05-10     4.445694
2016-05-11     5.902835
dtype: float64
```




































