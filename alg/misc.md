
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
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     #dftmp = pd.read_csv(z.open('CRUDE_W_price.csv'), index_col=0,parse_dates=True )
     dftmp = pd.read_csv(z.open('US5_price.csv'), index_col=0,parse_dates=True )
dftmp.PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)





































