

```python
import pandas as pd
import sys; sys.path.append('../data')
import futures
insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
```

```python
inst = "FV"
market = insts['market'][inst]
rollcycle = insts['rollcycle'][inst]
rolloffset = insts['rolloffset'][inst]
expday = insts['expday'][inst]
expmon = insts['expmon'][inst]
carryoffset = insts['carryoffset'][inst]
print inst, market, rollcycle, rolloffset, expday, expmon, carryoffset
#ctd = futures.get_contracts(market,inst,1990,futures.systemtoday().year)
#cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
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
dtype: object 6986
```

```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     #dftmp = pd.read_csv(z.open('CRUDE_W_price.csv'), index_col=0,parse_dates=True )
     dftmp = pd.read_csv(z.open('US5_price.csv'), index_col=0,parse_dates=True )
dftmp.PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)


```python
import sys; sys.path.append('../data')
import futures
import pickle, pandas as pd
df_carry2 = pd.read_csv("out1.csv",index_col=0,parse_dates=True)
cts_assigned2 = pickle.load( open( "cts_assigned.pkl", "rb" ) )
ctd2 = pickle.load( open( "ctd.pkl", "rb" ) )
```

```python
res = futures.rolldates(cts_assigned2)
```

```python
import datetime

def stitch_contracts(rolldates, ctd, price_col):

    rolldates2 = []
    for (rolldate, from_con, to_con) in rolldates:
    	if str(from_con) in ctd.keys() and str(to_con) in ctd.keys():
	   rolldates2.append((rolldate, from_con, to_con))	   

    rolldates3 = []
    for i,(rolldate, from_con, to_con) in enumerate(rolldates2):
        #print rolldate, from_con, to_con
        for j in range(200):
            #print "adjusting rolldate", rolldate, "contract", from_con, to_con
            rolldate += np.power(-1,j)*datetime.timedelta(days=j)
            if rolldate in ctd[str(from_con)].index and rolldate in ctd[str(to_con)].index:
                break
        rolldates3.append((rolldate, from_con, to_con))

    for x in rolldates3: print x

stitch_contracts(res, ctd2, 's')
```

```text
(Timestamp('1990-02-09 00:00:00'), '199003', '199006')
(Timestamp('1990-05-11 00:00:00'), '199006', '199009')
(Timestamp('1990-08-13 00:00:00'), '199009', '199012')
(Timestamp('1990-11-12 00:00:00'), '199012', '199103')
(Timestamp('1991-02-08 00:00:00'), '199103', '199106')
(Timestamp('1991-05-13 00:00:00'), '199106', '199109')
(Timestamp('1991-08-12 00:00:00'), '199109', '199112')
(Timestamp('1991-11-11 00:00:00'), '199112', '199203')
(Timestamp('1992-02-10 00:00:00'), '199203', '199206')
(Timestamp('1992-05-12 00:00:00'), '199206', '199209')
(Timestamp('1992-08-12 00:00:00'), '199209', '199212')
(Timestamp('1992-11-11 00:00:00'), '199212', '199303')
(Timestamp('1993-02-09 00:00:00'), '199303', '199306')
(Timestamp('1993-05-12 00:00:00'), '199306', '199309')
(Timestamp('1993-08-12 00:00:00'), '199309', '199312')
(Timestamp('1993-11-11 00:00:00'), '199312', '199403')
(Timestamp('1994-02-09 00:00:00'), '199403', '199406')
(Timestamp('1994-05-12 00:00:00'), '199406', '199409')
(Timestamp('1994-08-12 00:00:00'), '199409', '199412')
(Timestamp('1994-11-11 00:00:00'), '199412', '199503')
(Timestamp('1995-02-09 00:00:00'), '199503', '199506')
(Timestamp('1995-05-12 00:00:00'), '199506', '199509')
(Timestamp('1995-08-11 00:00:00'), '199509', '199512')
(Timestamp('1995-11-10 00:00:00'), '199512', '199603')
(Timestamp('1996-02-09 00:00:00'), '199603', '199606')
(Timestamp('1996-05-13 00:00:00'), '199606', '199609')
(Timestamp('1996-08-12 00:00:00'), '199609', '199612')
(Timestamp('1996-11-12 00:00:00'), '199612', '199703')
(Timestamp('1997-02-10 00:00:00'), '199703', '199706')
(Timestamp('1997-05-12 00:00:00'), '199706', '199709')
(Timestamp('1997-08-12 00:00:00'), '199709', '199712')
(Timestamp('1997-11-10 00:00:00'), '199712', '199803')
(Timestamp('1998-02-09 00:00:00'), '199803', '199806')
(Timestamp('1998-05-12 00:00:00'), '199806', '199809')
(Timestamp('1998-08-12 00:00:00'), '199809', '199812')
(Timestamp('1998-11-10 00:00:00'), '199812', '199903')
(Timestamp('1999-02-09 00:00:00'), '199903', '199906')
(Timestamp('1999-05-12 00:00:00'), '199906', '199909')
(Timestamp('1999-08-12 00:00:00'), '199909', '199912')
(Timestamp('1999-11-10 00:00:00'), '199912', '200003')
(Timestamp('2000-02-10 00:00:00'), '200003', '200006')
(Timestamp('2000-05-12 00:00:00'), '200006', '200009')
(Timestamp('2000-08-11 00:00:00'), '200009', '200012')
(Timestamp('2000-11-10 00:00:00'), '200012', '200103')
(Timestamp('2001-02-09 00:00:00'), '200103', '200106')
(Timestamp('2001-05-11 00:00:00'), '200106', '200109')
(Timestamp('2001-08-13 00:00:00'), '200109', '200112')
(Timestamp('2001-11-13 00:00:00'), '200112', '200203')
(Timestamp('2002-02-08 00:00:00'), '200203', '200206')
(Timestamp('2002-05-13 00:00:00'), '200206', '200209')
(Timestamp('2002-08-12 00:00:00'), '200209', '200212')
(Timestamp('2002-11-12 00:00:00'), '200212', '200303')
(Timestamp('2003-02-10 00:00:00'), '200303', '200306')
(Timestamp('2003-05-12 00:00:00'), '200306', '200309')
(Timestamp('2003-08-12 00:00:00'), '200309', '200312')
(Timestamp('2003-11-10 00:00:00'), '200312', '200403')
(Timestamp('2004-02-10 00:00:00'), '200403', '200406')
(Timestamp('2004-05-12 00:00:00'), '200406', '200409')
(Timestamp('2004-08-12 00:00:00'), '200409', '200412')
(Timestamp('2004-11-10 00:00:00'), '200412', '200503')
(Timestamp('2005-02-09 00:00:00'), '200503', '200506')
(Timestamp('2005-05-12 00:00:00'), '200506', '200509')
(Timestamp('2005-08-12 00:00:00'), '200509', '200512')
(Timestamp('2005-11-10 00:00:00'), '200512', '200603')
(Timestamp('2006-02-09 00:00:00'), '200603', '200606')
(Timestamp('2006-05-12 00:00:00'), '200606', '200609')
(Timestamp('2006-08-11 00:00:00'), '200609', '200612')
(Timestamp('2006-11-10 00:00:00'), '200612', '200703')
(Timestamp('2007-02-09 00:00:00'), '200703', '200706')
(Timestamp('2007-05-11 00:00:00'), '200706', '200709')
(Timestamp('2007-08-13 00:00:00'), '200709', '200712')
(Timestamp('2007-11-13 00:00:00'), '200712', '200803')
(Timestamp('2008-02-11 00:00:00'), '200803', '200806')
(Timestamp('2008-05-12 00:00:00'), '200806', '200809')
(Timestamp('2008-08-12 00:00:00'), '200809', '200812')
(Timestamp('2008-11-10 00:00:00'), '200812', '200903')
(Timestamp('2009-02-09 00:00:00'), '200903', '200906')
(Timestamp('2009-05-12 00:00:00'), '200906', '200909')
(Timestamp('2009-08-12 00:00:00'), '200909', '200912')
(Timestamp('2009-11-11 00:00:00'), '200912', '201003')
(Timestamp('2010-02-09 00:00:00'), '201003', '201006')
(Timestamp('2010-05-12 00:00:00'), '201006', '201009')
(Timestamp('2010-08-12 00:00:00'), '201009', '201012')
(Timestamp('2010-11-11 00:00:00'), '201012', '201103')
(Timestamp('2011-02-09 00:00:00'), '201103', '201106')
(Timestamp('2011-05-12 00:00:00'), '201106', '201109')
(Timestamp('2011-08-12 00:00:00'), '201109', '201112')
(Timestamp('2011-11-11 00:00:00'), '201112', '201203')
(Timestamp('2012-02-10 00:00:00'), '201203', '201206')
(Timestamp('2012-05-11 00:00:00'), '201206', '201209')
(Timestamp('2012-08-13 00:00:00'), '201209', '201212')
(Timestamp('2012-11-12 00:00:00'), '201212', '201303')
(Timestamp('2013-02-08 00:00:00'), '201303', '201306')
(Timestamp('2013-05-13 00:00:00'), '201306', '201309')
(Timestamp('2013-08-12 00:00:00'), '201309', '201312')
(Timestamp('2013-11-11 00:00:00'), '201312', '201403')
(Timestamp('2014-02-10 00:00:00'), '201403', '201406')
(Timestamp('2014-05-12 00:00:00'), '201406', '201409')
(Timestamp('2014-08-12 00:00:00'), '201409', '201412')
(Timestamp('2014-11-11 00:00:00'), '201412', '201503')
(Timestamp('2015-02-09 00:00:00'), '201503', '201506')
(Timestamp('2015-05-12 00:00:00'), '201506', '201509')
(Timestamp('2015-08-12 00:00:00'), '201509', '201512')
(Timestamp('2015-11-11 00:00:00'), '201512', '201603')
(Timestamp('2016-03-31 00:00:00'), '201603', '201612')
```

















```python
print ctd2['201512'].tail(1)
print ctd2['201603'].tail(1)
# 2016-02-10'????
# 2015-11-11
```

```text
                     h       l           o     oi          s     v
Date                                                              
2015-12-31  118.890625  118.75  118.757812  36363  118.84375  3052
                     h           l           o     oi          s     v
Date                                                                  
2016-03-31  121.390625  121.179688  121.257812  34709  121.34375  2376
```

```python
print cts_assigned2.tail(4)
```

```text
           effcont
2016-06-27     NaN
2016-06-28     NaN
2016-06-29     NaN
2016-06-30     NaN
```









```python
df_stitched2 = futures.stitch_contracts(cts_assigned2, ctd2, 's')
```

```python
df_stitched2.plot()
plt.savefig('misc_01.png')
```







































