

```python
import util, zipfile, pandas as pd

slow=32;fast=128
ewmacs = [(2,8),(4,16),(8,32),(16,64),(32,128),(64,256)]

for (slow,fast) in ewmacs: 
    with zipfile.ZipFile('legacycsv.zip', 'r') as z:
        res = []
        for x in  z.namelist():
            if '_price' in x:
                df = pd.read_csv(z.open(x), index_col=0,parse_dates=True )
                tmp = util.ewma(df.PRICE, slow, fast)
                res.append(tmp)

    tmp = pd.DataFrame(pd.concat(res))
    tmp.columns = ['forecast']
    print 'ewma', slow,fast,'=', float(util.estimate_forecast_scalar(tmp))
```

```text
ewma 2 8 = 12.8587606411
ewma 4 16 = 8.91499507015
ewma 8 32 = 6.09843054736
ewma 16 64 = 4.17115322451
ewma 32 128 = 2.84127283125
ewma 64 256 = 1.92365849221
```

book

2,8 10.6
4,16 7.5
8,32 5.3
16,64 3.75
32,128 2.65
64,256 1.87

pysys

#64_256 1.68
#32_128 2.57
#2_8 12.22

```python
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
    res = []
    for x in  z.namelist():
        if '_price' in x:
            df = pd.read_csv(z.open(x), index_col=0,parse_dates=True )
            tmp = util.ewma(df.PRICE, slow, fast)
            res.append(tmp)

tmp = pd.DataFrame(pd.concat(res))
tmp.columns = ['forecast']
print slow,fast,float(util.estimate_forecast_scalar(tmp).tail(1))
```




































