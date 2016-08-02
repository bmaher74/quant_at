
```python
import pandas as pd, util
import sys; sys.path.append('../data')
import futures
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





































