
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures

inst = "FV"
market = "CME"
insts = pd.read_csv('instruments.csv',index_col=[0,1],comment='#').to_dict()
futures.combine_contract_info_save(inst, market, insts, db="findb")
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
Index([u'carrycont', u'carryprice', u'effcont', u'effprice', u'sprice'], dtype='object')
```




























