

```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
```

```python
inst = "FV"
market = insts['market'][inst]
rollcycle = insts['rollcycle'][inst]
rolloffset = insts['rolloffset'][inst]
expday = insts['expday'][inst]
expmon = insts['expmon'][inst]
carryoffset = insts['carryoffset'][inst]
print inst, market, rollcycle, rolloffset, expday, expmon, carryoffset
#ctd = futures.get_contracts(market,inst,1990,futures.systemtoday().year)
#cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
```

```text
FV CME HMUZ 50 30 curr 3
```

```python
import pickle

df_carry.to_csv("out1.csv")
cts_assigned.to_csv("out2.csv")
output = open('cts_assigned.pkl', 'wb'); pickle.dump(cts_assigned, output)
output.close()
output = open('ctd.pkl', 'wb'); pickle.dump(ctd, output)
output.close()
print cts_assigned.dtypes, len(cts_assigned)
```

```text
effcont    object
dtype: object 6986
```

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     #dftmp = pd.read_csv(z.open('CRUDE_W_price.csv'), index_col=0,parse_dates=True )
     dftmp = pd.read_csv(z.open('US5_price.csv'), index_col=0,parse_dates=True )
dftmp.PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)


```python
import sys; sys.path.append('../data')
import futures
import pickle, pandas as pd
df_carry2 = pd.read_csv("out1.csv",index_col=0,parse_dates=True)
cts_assigned2 = pickle.load( open( "cts_assigned.pkl", "rb" ) )
ctd2 = pickle.load( open( "ctd.pkl", "rb" ) )
print cts_assigned2.dtypes, len(cts_assigned2)
```

```text
effcont    object
dtype: object 6986
```

```python
print ctd2['201512'].tail(1)
print ctd2['201603'].tail(1)
# 2016-02-10'????
# 2015-11-11
```

```text
                     h       l           o     oi          s     v
Date                                                              
2015-12-31  118.890625  118.75  118.757812  36363  118.84375  3052
                     h           l           o     oi          s     v
Date                                                                  
2016-03-31  121.390625  121.179688  121.257812  34709  121.34375  2376
```

```python
print cts_assigned2.tail(4)
```

```text
           effcont
2016-06-27     NaN
2016-06-28     NaN
2016-06-29     NaN
2016-06-30     NaN
```









```python
df_stitched2 = futures.stitch_contracts(cts_assigned2, ctd2, 's')
```

```python
df_stitched2.plot()
plt.savefig('misc_01.png')
```







































