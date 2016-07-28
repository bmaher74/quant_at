

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
    #df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
    break
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
dtype: object 7335
```

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
dtype: object 7335
```

```python
#df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
df_stitched2 = futures.stitch_contracts(cts_assigned2, ctd2, 's')
```

```python
print len(ctd2['201612'])
```

```text
65
```



```text
FV CME HMUZ 50 30 curr 3
```

```python
print ctd.keys()
```

```text
['198806', '198809', '198812', '198903', '198906', '198909', '198912', '199003', '199006', '199009', '199012', '199103', '199106', '199109', '199112', '199203', '199206', '199209', '199212', '199303', '199306', '199309', '199312', '199403', '199406', '199409', '199412', '199503', '199506', '199509', '199512', '199603', '199606', '199609', '199612', '199703', '199706', '199709', '199712', '199803', '199806', '199809', '199812', '199903', '199906', '199909', '199912', '200003', '200006', '200009', '200012', '200103', '200106', '200109', '200112', '200203', '200206', '200209', '200212', '200303', '200306', '200309', '200312', '200403', '200406', '200409', '200412', '200503', '200506', '200509', '200512', '200603', '200606', '200609', '200612', '200703', '200706', '200709', '200712', '200803', '200806', '200809', '200812', '200903', '200906', '200909', '200912', '201003', '201006', '201009', '201012', '201103', '201106', '201109', '201112', '201203', '201206', '201209', '201212', '201303', '201306', '201309', '201312', '201403', '201406', '201409', '201412', '201503', '201506', '201509', '201512', '201603', '201606', '201609', '201612']
```


```python
df_stitched.plot()
plt.savefig('misc_01.png')
```

![](misc_01.png)


```python
df_carry.to_csv("out1.csv")
df_carry['stitched'] = df_stitched
df_carry.to_csv("out2.csv")
```

```text
<class 'pandas.core.series.Series'>
Index([u'effcont', u'carrycont', u'effprice', u'carryprice', u'stitched'], dtype='object')
6939
7168
```

```python
from pymongo import MongoClient
connection = MongoClient()
fdb = connection["findb"].futures
```



```python
df_carry['stitched'] = df_stitched
sym = "FV"; market = "CME"
def f(x):
    new_row = {"_id": {"sym": sym, "market": market,  "dt": x.name.strftime('%Y-%m-%d') }, \
    	       "effcont": x.effcont, "carrycont": x.carrycont, "effprice": x.effprice, \
	       "carryprice": x.carryprice, "stitched": x.stitched }
    print new_row
df_carry.tail(10).apply(f, axis=1)    
```

```text
{'effprice': 120.0546875, 'carryprice': nan, 'stitched': 120.0546875, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-10-28', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 119.78125, 'carryprice': nan, 'stitched': 119.78125, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-10-29', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 119.7734375, 'carryprice': nan, 'stitched': 119.7734375, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-10-30', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 119.5859375, 'carryprice': nan, 'stitched': 119.5859375, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-02', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 119.4296875, 'carryprice': nan, 'stitched': 119.4296875, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-03', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 119.203125, 'carryprice': nan, 'stitched': 119.203125, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-04', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 119.1484375, 'carryprice': nan, 'stitched': 119.1484375, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-05', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 118.703125, 'carryprice': nan, 'stitched': 118.703125, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-06', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 118.703125, 'carryprice': nan, 'stitched': 118.703125, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-09', 'market': 'CME', 'sym': 'FV'}}
{'effprice': 118.90625, 'carryprice': nan, 'stitched': 118.90625, 'effcont': '201512', 'carrycont': '201603', '_id': {'dt': '2015-11-10', 'market': 'CME', 'sym': 'FV'}}
Out[1]: 
2015-10-28    None
2015-10-29    None
2015-10-30    None
2015-11-02    None
2015-11-03    None
2015-11-04    None
2015-11-05    None
2015-11-06    None
2015-11-09    None
2015-11-10    None
dtype: object
```











































