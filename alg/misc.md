

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
    df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
    break
```

```text
FV CME HMUZ 50 30 curr 3
```

```python
print cts_assigned.columns
print ctd['198806'].s.head()
```

```text
Index([u'effcont'], dtype='object')
Date
1988-05-20    96.953125
1988-05-23    96.796875
1988-05-24    96.812500
1988-05-25    96.890625
1988-05-26    96.765625
Name: s, dtype: float64
```
































