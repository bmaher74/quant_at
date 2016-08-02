
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
```

```python
d = futures.get_stitched("CL", "CME")
print d.tail()
```

```text
           carrycont  carryprice effcont  effprice  sprice
Date                                                      
2016-06-24    201611       49.29  201612     49.72   49.72
2016-06-27    201611       48.06  201612     48.52   48.52
2016-06-28    201611       49.72  201612     50.20   50.20
2016-06-29    201611       51.70  201612     52.19   52.19
2016-06-30    201611       50.13  201612     50.62   50.62
```

```python
df_carry.sprice.plot()
plt.savefig('misc_01.png')
```

![](misc_01.png)


```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dftmp = pd.read_csv(z.open('CORN_price.csv'), index_col=0,parse_dates=True )     
dftmp[dftmp.index > '1990-01-01'].PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)























