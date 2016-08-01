
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
df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
#df_carry['sprice'] = df_stitched
```

```text
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-1-8fa80ab42f1f> in <module>()
     10 #cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
     11 #df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
---> 12 df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
     13 #df_carry['sprice'] = df_stitched

c:\Users\burak\Documents\quant_at\data\futures.pyc in stitch_contracts(cts_assigned, ctd, price_col)
    279 
    280     contracts = [ctd[x] for x in list(np.unique(contracts))]
--> 281     df_stitched = stitch_prices(contracts, 's', rolldates4, ctd)
    282     return df_stitched
    283 

c:\Users\burak\Documents\quant_at\data\futures.pyc in stitch_prices(dfs, price_col, dates, ctd)
    210         
    211     for i,v in enumerate(datesr):
--> 212         tmp1=float(dfsr[i].ix[v,price_col])
    213         tmp2=float(dfsr_pair[i].ix[v,price_col])
    214         dfsr_pair[i].loc[:,price_col] = dfsr_pair[i][price_col] + tmp1-tmp2

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\indexing.pyc in __getitem__(self, key)
     66                 pass
     67 
---> 68             return self._getitem_tuple(key)
     69         else:
     70             return self._getitem_axis(key, axis=0)

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\indexing.pyc in _getitem_tuple(self, tup)
    736     def _getitem_tuple(self, tup):
    737         try:
--> 738             return self._getitem_lowerdim(tup)
    739         except IndexingError:
    740             pass

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\indexing.pyc in _getitem_lowerdim(self, tup)
    861         for i, key in enumerate(tup):
    862             if is_label_like(key) or isinstance(key, tuple):
--> 863                 section = self._getitem_axis(key, axis=i)
    864 
    865                 # we have yielded a scalar ?

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\indexing.pyc in _getitem_axis(self, key, axis)
    965                     return self._get_loc(key, axis=axis)
    966 
--> 967             return self._get_label(key, axis=axis)
    968 
    969     def _getitem_iterable(self, key, axis=0):

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\indexing.pyc in _get_label(self, label, axis)
     84             raise IndexingError('no slices here, handle elsewhere')
     85 
---> 86         return self.obj._xs(label, axis=axis)
     87 
     88     def _get_loc(self, key, axis=0):

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\generic.pyc in xs(self, key, axis, level, copy, drop_level)
   1484                                                       drop_level=drop_level)
   1485         else:
-> 1486             loc = self.index.get_loc(key)
   1487 
   1488             if isinstance(loc, np.ndarray):

c:\Users\burak\Anaconda2\lib\site-packages\pandas\tseries\index.pyc in get_loc(self, key, method, tolerance)
   1347             # needed to localize naive datetimes
   1348             key = Timestamp(key, tz=self.tz)
-> 1349             return Index.get_loc(self, key, method, tolerance)
   1350 
   1351         if isinstance(key, time):

c:\Users\burak\Anaconda2\lib\site-packages\pandas\core\index.pyc in get_loc(self, key, method, tolerance)
   1757                                  'backfill or nearest lookups')
   1758             key = _values_from_object(key)
-> 1759             return self._engine.get_loc(key)
   1760 
   1761         indexer = self.get_indexer([key], method=method,

pandas\index.pyx in pandas.index.DatetimeEngine.get_loc (pandas\index.c:11072)()

pandas\index.pyx in pandas.index.DatetimeEngine.get_loc (pandas\index.c:10832)()

KeyError: Timestamp('1990-09-26 00:00:00')
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

























