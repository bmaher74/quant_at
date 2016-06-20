

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     df = pd.read_csv(z.open('SP500_price.csv'), index_col=0,parse_dates=True )
     df['x'] = pd.read_csv(z.open('US20_price.csv'), index_col=0,parse_dates=True )
df.columns = ['SP500','US20']
print df.tail(4)     
```

```text
               SP500        US20
DATETIME                        
2016-05-06  2053.000  165.125000
2016-05-09  2054.250  165.625000
2016-05-10  2077.750  165.625000
2016-05-11  2070.875  166.390625
```



```python
print util.generate_fitting_dates(df, 'expanding')
```

```text
data=               SP500        US20
DATETIME                        
2016-05-06  2053.000  165.125000
2016-05-09  2054.250  165.625000
2016-05-10  2077.750  165.625000
2016-05-11  2070.875  166.390625
date_method=expanding
[Fit without data, use from 1997-09-10 00:00:00 to 1998-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 1998-09-30 00:00:00, use in 1998-09-30 00:00:00 to 1999-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 1999-09-30 00:00:00, use in 1999-09-30 00:00:00 to 2000-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2000-09-30 00:00:00, use in 2000-09-30 00:00:00 to 2001-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2001-09-30 00:00:00, use in 2001-09-30 00:00:00 to 2002-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2002-09-30 00:00:00, use in 2002-09-30 00:00:00 to 2003-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2003-09-30 00:00:00, use in 2003-09-30 00:00:00 to 2004-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2004-09-30 00:00:00, use in 2004-09-30 00:00:00 to 2005-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2005-09-30 00:00:00, use in 2005-09-30 00:00:00 to 2006-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2006-09-30 00:00:00, use in 2006-09-30 00:00:00 to 2007-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2007-09-30 00:00:00, use in 2007-09-30 00:00:00 to 2008-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2008-09-30 00:00:00, use in 2008-09-30 00:00:00 to 2009-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2009-09-30 00:00:00, use in 2009-09-30 00:00:00 to 2010-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2010-09-30 00:00:00, use in 2010-09-30 00:00:00 to 2011-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2011-09-30 00:00:00, use in 2011-09-30 00:00:00 to 2012-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2012-09-30 00:00:00, use in 2012-09-30 00:00:00 to 2013-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2013-09-30 00:00:00, use in 2013-09-30 00:00:00 to 2014-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2014-09-30 00:00:00, use in 2014-09-30 00:00:00 to 2015-09-30 00:00:00, Fit from 1997-09-10 00:00:00 to 2015-09-30 00:00:00, use in 2015-09-30 00:00:00 to 2016-05-11 00:00:00]
```







```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     df = pd.read_csv(z.open('EDOLLAR_price.csv'), index_col=0,parse_dates=True )

fast_ewma = pd.ewma(df.PRICE, span=32)
slow_ewma = pd.ewma(df.PRICE, span=128)
raw_ewmac = fast_ewma - slow_ewma
vol = util.robust_vol_calc(df.PRICE.diff())
forecast = raw_ewmac /  vol 

print util.sharpe(df.PRICE, forecast)
```

```text
0.508384873452
```


















































`
































