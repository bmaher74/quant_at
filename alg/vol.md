
```python

import pandas as pd
import numpy as np 
import simple

def bollinger(df,ldev):
    signals = pd.DataFrame(index=df.index) 
    signals['signal'] = np.nan
    middle = pd.rolling_mean(df[col], 40, min_periods=1) 
    std = pd.rolling_std(df[col], 40, min_periods=1)
    df['middle'] = middle
    df['top'] = middle+2*std
    df['bottom'] = middle-2*std
    signals['signal'] = np.where(df[col] > middle+2*std, -1, np.nan) 
    signals['signal'] = np.where(df[col] < middle-2*std, 1, np.nan)
    signals['signal'] = signals['signal'].fillna(method='ffill')
    df['ret'] = df[col].pct_change() * signals['signal'].shift(1)
    ret = df.ret.dropna() * lev
    return ret

#col = 'a'; px = simple.get('IYH')
col = 'PRICE'; ff = 'c:/Users/burak/Downloads/pysystemtrade/sysdata/legacycsv/CRUDE_W_price.csv'
px = pd.read_csv(ff,parse_dates=True,index_col=0)

lev = 1.
ret = bollinger(px,lev)
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
    
```

