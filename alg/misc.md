
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
```

```python
d = futures.get_stitched("C", "CME")
d.sprice.plot()
#d[d.index > '2013-01-01'].sprice.plot()
plt.savefig('misc_01.png')
print d.head()
```

```text
           carrycont  carryprice effcont  effprice  sprice
Date                                                      
1988-09-26    198909         NaN  198912       NaN     NaN
1988-09-27    198909         NaN  198912       NaN     NaN
1988-09-28    198909         NaN  198912       NaN     NaN
1988-09-29    198909         NaN  198912       NaN     NaN
1988-09-30    198909         NaN  198912       NaN     NaN
```


```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dftmp = pd.read_csv(z.open('CORN_price.csv'), index_col=0,parse_dates=True )     
dftmp[dftmp.index > '1987-06-01'].PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)























