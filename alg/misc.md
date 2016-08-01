
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
insts = pd.read_csv('instr1.csv',index_col=[0,1],comment='#').to_dict('index')
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
cts_assigned.to_csv("out.csv")
print ctd.keys()
#df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
#df_carry['sprice'] = df_stitched
```

```text ['199003', '199005', '199007', '199009', '199012', '199103',
'199105', '199107', '199109', '199112', '199203', '199205', '199207',
'199209', '199212', '199303', '199305', '199307', '199309', '199312',
'199403', '199405', '199407', '199409', '199412', '199503', '199505',
'199507', '199509', '199512', '199603', '199605', '199607', '199609',
'199612', '199703', '199705', '199707', '199709', '199712', '199803',
'199805', '199807', '199809', '199812', '199903', '199905', '199907',
'199909', '199912', '200001', '200003', '200005', '200007', '200009',
'200011', '200012', '200101', '200103', '200105', '200107', '200109',
'200111', '200112', '200201', '200203', '200205', '200207', '200209',
'200212', '200303', '200305', '200307', '200309', '200312', '200403',
'200405', '200407', '200409', '200412', '200503', '200505', '200507',
'200509', '200512', '200603', '200605', '200607', '200609', '200612',
'200703', '200705', '200707', '200709', '200712', '200803', '200805',
'200807', '200809', '200812', '200903', '200905', '200907', '200909',
'200912', '201003', '201005', '201007', '201009', '201012', '201103',
'201105', '201107', '201109', '201112', '201203', '201205', '201207',
'201209', '201212', '201303', '201305', '201307', '201309', '201312',
'201403', '201405', '201407', '201409', '201412', '201503', '201505',
'201507', '201509', '201512', '201603', '201605', '201607', '201609',
'201612'] ```

```python
df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
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
d.sprice.plot()
plt.savefig('misc_01.png')
```

![](misc_01.png)

























