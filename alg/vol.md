
```python
import sys; sys.path.append('../data')
import sys; sys.path.append('../book')
import pandas as pd, dd
import numpy as np 
import simple, util
```

```python
col = 'a'; px = simple.get('DBA')
#col = 'PRICE'; ff = 'c:/Users/burak/Downloads/pysystemtrade/sysdata/legacycsv/CRUDE_W_price.csv'
#px = pd.read_csv(ff,parse_dates=True,index_col=0)

#ret = util.bollinger(px,col,lev=1.) 
ret = util.crossover(px,col,lev=1) 
print ret.mean(), ret.std()*np.sqrt(252)
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)    
print 'DD', dd.calculateMaxDD(cumret)
```

```text
0.000135274304924 0.128324682669
APR 0.026189816399
Sharpe 0.26570375005
DD (-0.28116407265346588, 1313.0)
```




















