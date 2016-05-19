import pandas as pd
import numpy as np 
import simple

#px = simple.get('DJIA')

col = 'PRICE'
ff = 'c:/Users/burak/Downloads/pysystemtrade/sysdata/legacycsv/AUD_price.csv'
px = pd.read_csv(ff,parse_dates=True,index_col=0)
df_yhoo = px

signals = pd.DataFrame(index=px.index) 
signals['signal'] = 0 

short_ma = pd.rolling_mean(px[col], 40, min_periods=1) 
long_ma = pd.rolling_mean(px[col], 100, min_periods=1) 
signals['signal'] = np.where(short_ma > long_ma, 1, 0) 
px['signal'] = signals['signal'].shift(1) 
px['ret'] = px[col].pct_change() * px['signal']
ret = px.ret.dropna()
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)

#df_yhoo = pd.read_csv("./legacycsv/CORN_price.csv",parse_dates=True,index_col=0)
signals = pd.DataFrame(index=df_yhoo.index) 
signals['signal'] = np.nan
middle = pd.rolling_mean(df_yhoo[col], 40, min_periods=1) 
std = pd.rolling_std(df_yhoo[col], 40, min_periods=1)

df_yhoo['middle'] = middle
df_yhoo['top'] = middle+2*std
df_yhoo['bottom'] = middle-2*std
df_yhoo[[col,'middle','bottom','top']].plot()

signals['signal'] = np.where(df_yhoo[col] > middle+2*std, -1, np.nan) 
signals['signal'] = np.where(df_yhoo[col] < middle-2*std, 1, np.nan)
signals['signal'] = signals['signal'].fillna(method='ffill')
df_yhoo['ret'] = df_yhoo[col].pct_change() * signals['signal'].shift(1)
ret = df_yhoo.ret.dropna()
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
