

```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
```

```python
inst = "CL"
market = insts['market'][inst]
rollcycle = insts['rollcycle'][inst]
rolloffset = insts['rolloffset'][inst]
expday = insts['expday'][inst]
expmon = insts['expmon'][inst]
carryoffset = insts['carryoffset'][inst]
print inst, market, rollcycle, rolloffset, expday, expmon, carryoffset
#ctd = futures.get_contracts(market,inst,1980,futures.systemtoday().year)
#cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
```

```text
CL CME Z 50 25 prev -1
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
dtype: object 8632
```

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dfus5 = pd.read_csv(z.open('US5_price.csv'), index_col=0,parse_dates=True )
dfus5.PRICE.plot()
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
dtype: object 8632
```

```python
df_stitched2 = futures.stitch_contracts(cts_assigned2, ctd2, 's')
```








































