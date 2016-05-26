
```python
import sys; sys.path.append('../data')
import pandas as pd
import numpy as np 
import simple
col = 'a'; px = simple.get('IBB')
#col = 'PRICE'; ff = 'c:/Users/burak/Downloads/pysystemtrade/sysdata/legacycsv/CRUDE_W_price.csv'
#px = pd.read_csv(ff,parse_dates=True,index_col=0)
```

```python

def crossover(df,lev):
    signals = pd.DataFrame(index=df.index) 
    signals['signal'] = 0 
    short_ma = pd.rolling_mean(df[col], 40, min_periods=1) 
    long_ma = pd.rolling_mean(df[col], 100, min_periods=1) 
    signals['signal'] = np.where(short_ma > long_ma, 1, 0) 
    df['signal'] = signals['signal'].shift(1) 
    df['ret'] = df[col].pct_change() * df['signal']
    ret = df.ret.dropna() * lev
    return ret

def bollinger(df,lev):
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

#ret = bollinger(px,lev=1.1) # CRUDE_W
#ret = crossover(px,lev=1.1) # CRUDE
ret = bollinger(px,lev=1.0) 
#ret = crossover(px,lev=1.4) 
print ret.mean(), ret.std()*np.sqrt(252)
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)    
```

```text
0.000661460999407 0.267193442191
APR 0.139856454625
Sharpe 0.623970792749
```

```python
fr=100.;to=110
print (to-fr)/fr * 100.
```

```text
10.0
10.0
```





















