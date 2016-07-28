

```python
import sys; sys.path.append('../data')
import futures, datetime
def sc(dfc, ctd, price_col):
    tmp = dfc.effcont.dropna().astype(int).diff().dropna()
    rolldates = tmp[tmp > 0].index
    rollconts = np.unique(dfc.effcont.dropna())
    rollconts = [x for x in rollconts if x in ctd]
    rolldates = [x for x in rolldates if \
                 int("%d%02d" % (x.year, x.month)) >= int(ctd.keys()[0]) and \
                 int("%d%02d" % (x.year, x.month)) <= int(ctd.keys()[-1])]
	   
    tmp = [ctd[x] for x in rollconts]
    for i,x in enumerate(tmp):
    	if rolldates[i-1] not in x.index:
	   for j in range(5):
	       rolldates[i-1] = rolldates[i-1] - datetime.timedelta(days=j)
	       if rolldates[i-1] in ctd.values()[i].index: break
    dfs = futures.stitch_prices(tmp, price_col, rolldates)
    return dfs
```


```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
```

```python
for inst in insts['rolloffset']:
    market = insts['market'][inst]
    rollcycle = insts['rollcycle'][inst]
    rolloffset = insts['rolloffset'][inst]
    expday = insts['expday'][inst]
    expmon = insts['expmon'][inst]
    carryoffset = insts['carryoffset'][inst]
    print inst, market, rollcycle, rolloffset, expday, expmon, carryoffset
    #ctd = futures.get_contracts(market,inst,1980,futures.systemtoday().year)
    #cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
    #df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
    df_stitched = sc(cts_assigned, ctd, 's')
    break
```

```text
FV CME HMUZ 50 30 curr 3
```

```python
#print cts_assigned.columns
#print cts_assigned.ix['2008-11-10']
#print cts_assigned.ix['2008-11-11']
#print cts_assigned.ix['2008-11-12']
#2008-11-11
print ctd['200809'].tail(1)
print ctd['200812'].ix['2008-11-10']
print ctd['200903'].ix['2008-11-10']
```

```text
                   h         l         o     oi         s  v
Date                                                        
2008-09-30  113.6875  113.6875  113.6875  19282  113.6875  0
h         115.703125
l         115.296875
o         115.296875
oi    1274665.000000
s         115.703125
v         117.000000
Name: 2008-11-10 00:00:00, dtype: float64
h       113.500000
l       113.156250
o       113.156250
oi    35245.000000
s        92.601548
v       117.000000
Name: 2008-11-10 00:00:00, dtype: float64
```


```python
df_stitched.plot()
plt.savefig('misc_01.png')
```

![](misc_01.png)

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dfus5 = pd.read_csv(z.open('US5_price.csv'), index_col=0,parse_dates=True )
dfus5.PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)
























