import pandas as pd
import numpy as np 
import simple

#col = 'a'; px = simple.get('IYH')
col = 'PRICE'; ff = 'c:/Users/burak/Downloads/pysystemtrade/sysdata/legacycsv/CRUDE_W_price.csv'
px = pd.read_csv(ff,parse_dates=True,index_col=0)

lev = 1.

signals = pd.DataFrame(index=px.index) 
signals['signal'] = 0 
short_ma = pd.rolling_mean(px[col], 40, min_periods=1) 
long_ma = pd.rolling_mean(px[col], 100, min_periods=1) 
signals['signal'] = np.where(short_ma > long_ma, 1, 0) 
px['signal'] = signals['signal'].shift(1) 
px['ret'] = px[col].pct_change() * px['signal']
ret = px.ret.dropna() * lev
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)

signals = pd.DataFrame(index=px.index) 
signals['signal'] = np.nan
middle = pd.rolling_mean(px[col], 40, min_periods=1) 
std = pd.rolling_std(px[col], 40, min_periods=1)
px['middle'] = middle
px['top'] = middle+2*std
px['bottom'] = middle-2*std
signals['signal'] = np.where(px[col] > middle+2*std, -1, np.nan) 
signals['signal'] = np.where(px[col] < middle-2*std, 1, np.nan)
signals['signal'] = signals['signal'].fillna(method='ffill')
px['ret'] = px[col].pct_change() * signals['signal'].shift(1)
ret = px.ret.dropna() * lev
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
