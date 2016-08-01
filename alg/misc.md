
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

























