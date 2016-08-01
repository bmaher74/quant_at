
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
insts = pd.read_csv('instr2.csv',index_col=[0,1],comment='#').to_dict('index')
```

```python
inst = "C"; market = "CME"
rollcycle = insts[(inst,market)]['rollcycle']
rolloffset = insts[(inst,market)]['rolloffset']
expday = insts[(inst,market)]['expday']
expmon = insts[(inst,market)]['expmon']
carryoffset = insts[(inst,market)]['carryoffset']
#ctd = futures.get_contracts(market,inst,1990,futures.systemtoday().year)
#cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
#df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
#cts_assigned.to_csv("out.csv")
#df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
df_carry['sprice'] = df_stitched 
```







```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
```

```python
d = futures.get_stitched(inst, market)
print d.tail()
```

```text
           carrycont  carryprice effcont    effprice      sprice
Date                                                            
2016-05-05    201703         NaN  201612  120.890625  120.890625
2016-05-06    201703         NaN  201612  120.773438  120.773438
2016-05-09    201703         NaN  201612  120.937500  120.937500
2016-05-10    201703         NaN  201612  120.929688  120.929688
2016-05-11    201703         NaN  201612  120.937500  120.937500
```

```python
df_carry.sprice.plot()
plt.savefig('misc_01.png')
```

![](misc_01.png)


```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dftmp = pd.read_csv(z.open('CORN_price.csv'), index_col=0,parse_dates=True )     
dftmp[dftmp.index > '1990-01-01'].PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)























