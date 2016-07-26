
```python
import scipy.stats
import pandas as pd
import util

df = pd.read_csv("out.csv",index_col=0)
print util.skew(df.price, df.forecast)
```

```text
-8.45030739232
```




























