
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
2016-05-05    201611       46.28  201612     46.55   46.55
2016-05-06    201611       46.79  201612     47.07   47.07
2016-05-09    201611       45.52  201612     45.80   45.80
2016-05-10    201611       47.00  201612     47.28   47.28
2016-05-11    201611       48.59  201612     48.84   48.84
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























