

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     df = pd.read_csv(z.open('SP500_price.csv'), index_col=0,parse_dates=True )
     df['x'] = pd.read_csv(z.open('US20_price.csv'), index_col=0,parse_dates=True )
df.columns = ['SP500','US20']
forecast = df.copy()
df = df.sort_index()

def calc_ewmac_forecast(price,slow,fast):
    vol = util.robust_vol_calc(price.diff())
    fast_ewma = pd.ewma(price, span=slow)
    slow_ewma = pd.ewma(price, span=fast)
    raw_ewmac = fast_ewma - slow_ewma
    return raw_ewmac /  vol 
    
df['US20_ewmac8_32'] = calc_ewmac_forecast(df['US20'], 8, 32)
df['US20_ewmac32_128'] = calc_ewmac_forecast(df['US20'], 8, 32)
df['SP500_ewmac8_32'] = calc_ewmac_forecast(df['SP500'], 32, 128)
df['SP500_ewmac32_128'] = calc_ewmac_forecast(df['SP500'], 32, 128)
forecast['US20'] = (df['US20_ewmac8_32'] + df['US20_ewmac32_128']) / 2
forecast['SP500'] = (df['SP500_ewmac8_32'] + df['SP500_ewmac32_128']) / 2
forecast['US20'] = forecast['US20'] / forecast['US20'].mean() * 10
forecast['SP500'] = forecast['SP500'] / forecast['SP500'].mean() * 10
forecast.loc[forecast.US20 > 20, 'US20'] = 20.
forecast.loc[forecast.SP500 > 20, 'SP500'] = 20.

print forecast.tail(4)
```

```text
            SP500       US20
DATETIME                    
2016-05-06     20   7.267569
2016-05-09     20  13.018939
2016-05-10     20  17.411344
2016-05-11     20  20.000000
```

```python
df['US20_ret'] = df['US20'].pct_change() * forecast.shift(1).US20 / 10
df['SP500_ret'] = df['SP500'].pct_change() * forecast.shift(1).SP500 / 10
```















































`
































