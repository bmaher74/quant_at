
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures    
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
ins = "CL"
roll = insts['rollcycle'][ins]
rolloff = insts['rolloffset'][ins]
expday = insts['expday'][ins]
expmon = insts['expmon'][ins]
carryoff = int(insts['carryoffset'][ins])
print roll, rolloff, expday,expmon,carryoff
```

```text
Z 50 25 prev -1
```

```python
ctd = futures.get_contracts("CME",ins,2007,2013)
```

```python
res2 = futures.which_contract(ins, ctd, roll, rolloff, expday, expmon)
res2.to_csv("out2.csv")
```

```python
res3 = futures.create_carry(res2[pd.isnull(res2.effcont)==False],carryoff,ctd)
res3.to_csv("out3.csv")
```

```python
import util
raw_carry = res3.carryprice-res3.effprice
vol = util.robust_vol_calc(res3.effprice.diff())

def carry(daily_ann_roll, vol, diff_in_years, smooth_days=90):
    ann_stdev = vol * util.ROOT_BDAYS_INYEAR
    raw_carry = daily_ann_roll / ann_stdev
    smooth_carry = pd.ewma(raw_carry, smooth_days) / diff_in_years
    return smooth_carry.fillna(method='ffill')

resc =  carry(raw_carry, vol,  carryoff*1/util.CALENDAR_DAYS_IN_YEAR)
resc.to_csv("out5.csv")
print util.sharpe(res3.effprice, resc)
```

```text
0.40103374339
```


```python
dfs = futures.stitch_contracts(res2, ctd, 's')
dfs.plot()
plt.savefig('carry_01.png')
```

![](carry_01.png)



 

