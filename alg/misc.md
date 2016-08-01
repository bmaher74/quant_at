
```python
import pandas as pd
import sys; sys.path.append('../data')
import futures

inst = "FV"
market = "CME"
insts = pd.read_csv('instruments.csv',index_col=[0,1],comment='#').to_dict()
futures.combine_contract_info_save(inst, market, insts, db="findb")
```































