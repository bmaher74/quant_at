

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
```

```python
res = futures.rolldates(cts_assigned2)
```

```python
import datetime

def stitch_contracts(rolldates, ctd, price_col):

    rolldates2 = []
    for (rolldate, from_con, to_con) in rolldates:
    	if str(from_con) in ctd.keys() and str(to_con) in ctd.keys():
	   rolldates2.append((rolldate, from_con, to_con))	   

    rolldates3 = []
    for i,(rolldate, from_con, to_con) in enumerate(rolldates2):
        #print rolldate, from_con, to_con
        for j in range(200):
            #print "adjusting rolldate", rolldate, "contract", from_con, to_con
            rolldate += np.power(-1,j)*datetime.timedelta(days=j)
            if rolldate in ctd[str(from_con)].index and rolldate in ctd[str(to_con)].index:
                break
        rolldates3.append((rolldate, from_con, to_con))

    rolldates4 = []
    contracts = []
    for d,f,t in rolldates3:
    	contracts.append(f)
	contracts.append(t)
	rolldates4.append(d)

#    print len(rolldates4)
#    print len(np.unique(contracts))
    contracts = [ctd[x] for x in list(np.unique(contracts))]
    df_stitched = futures.stitch_prices(contracts, 's', rolldates4, ctd2)
    return df_stitched

df_stitched2 = None
df_stitched2 = stitch_contracts(res, ctd2, 's')
print len(df_stitched2)
```

```text
6726
```

```python
df_stitched2.plot()
plt.savefig('misc_01.png')
```







































