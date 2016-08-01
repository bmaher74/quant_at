

```python
import datetime, collections
import pandas as pd
ctd = collections.OrderedDict()
for y in [1990,1992,1994,1996,1998]:
    print y-2,y
    start_date = datetime.datetime(y-2, 1, 1)
    end_date = datetime.datetime(y, 12, 31)
    delta = end_date - start_date
    dates = []
    # get bizdays between start and end
    for i in range(delta.days + 1):
    	day = start_date + datetime.timedelta(days=i)
	if day.weekday() < 5: dates.append(day)
    df = pd.DataFrame(index=dates)
    df['s'] = y-1900
    print df.tail(2)
    ctd[int("%d12" % y)] = df
```

```text
1988 1990
             s
1990-12-28  90
1990-12-31  90
1990 1992
             s
1992-12-30  92
1992-12-31  92
1992 1994
             s
1994-12-29  94
1994-12-30  94
1994 1996
             s
1996-12-30  96
1996-12-31  96
1996 1998
             s
1998-12-30  98
1998-12-31  98
```

```python
import sys; sys.path.append('../data')
import futures

rollcycle = "Z"
rolloffset = 30
expday = 31
expmon = "curr"
carryoffset = -1
cts_assigned = futures.which_contract("dummy", ctd, rollcycle, rolloffset, expday, expmon)
df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
```

```python
cts_assigned.to_csv("out1.csv")
df_carry.to_csv("out2.csv")
```

```text
           effcont
1998-12-25     NaN
1998-12-28     NaN
1998-12-29     NaN
1998-12-30     NaN
1998-12-31     NaN
```

```python
df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
#df_carry['sprice'] = df_stitched
```















