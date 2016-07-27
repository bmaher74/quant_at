

```python
import sys; sys.path.append('../data')
import futures, datetime
def sc(dfc, ctd, price_col):
    tmp = dfc.effcont.dropna().astype(int).diff().dropna()
    rolldates = tmp[tmp > 0].index
    rollconts = np.unique(dfc.effcont.dropna())
    rollconts = [x for x in rollconts if x in ctd]
    rolldates = [x for x in rolldates if \
                 int("%d%02d" % (x.year, x.month)) >= int(ctd.keys()[0]) and \
                 int("%d%02d" % (x.year, x.month)) <= int(ctd.keys()[-1])]
	   
    tmp = [ctd[x] for x in rollconts]
    for i,x in enumerate(tmp):
    	print ctd.keys()[i]
    	print x.head(1).index
    	print x.tail(1).index
    	print rolldates[i-1]
    	print '-----------'
    	if rolldates[i-1] not in x.index:
	   for j in range(5):
	       rolldates[i-1] = rolldates[i-1] - datetime.timedelta(days=j)
	       if rolldates[i-1] in ctd.values()[i].index: break
    #dfs = futures.stitch_prices(tmp, price_col, rolldates)
    #return dfs
```


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
    df_stitched = sc(cts_assigned, ctd, 's')
    break
```

```text
FV CME HMUZ 50 30 curr 3
198806
DatetimeIndex(['1988-05-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1988-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2015-08-12 00:00:00
-----------
198809
DatetimeIndex(['1988-05-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1988-12-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1988-08-12 00:00:00
-----------
198812
DatetimeIndex(['1988-06-10'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1989-03-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1988-11-11 00:00:00
-----------
198903
DatetimeIndex(['1988-09-09'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1989-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1989-02-09 00:00:00
-----------
198906
DatetimeIndex(['1989-01-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1989-09-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1989-05-12 00:00:00
-----------
198909
DatetimeIndex(['1989-05-02'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1989-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1989-08-11 00:00:00
-----------
198912
DatetimeIndex(['1989-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1990-03-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1989-11-10 00:00:00
-----------
199003
DatetimeIndex(['1989-11-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1990-06-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1990-02-09 00:00:00
-----------
199006
DatetimeIndex(['1990-03-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1990-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1990-05-11 00:00:00
-----------
199009
DatetimeIndex(['1990-05-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1990-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1990-08-13 00:00:00
-----------
199012
DatetimeIndex(['1990-08-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1991-03-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1990-11-12 00:00:00
-----------
199103
DatetimeIndex(['1990-11-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1991-06-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1991-02-08 00:00:00
-----------
199106
DatetimeIndex(['1991-03-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1991-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1991-05-13 00:00:00
-----------
199109
DatetimeIndex(['1991-06-10'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1991-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1991-08-12 00:00:00
-----------
199112
DatetimeIndex(['1991-08-02'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1992-03-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1991-11-11 00:00:00
-----------
199203
DatetimeIndex(['1991-11-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1992-06-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1992-02-10 00:00:00
-----------
199206
DatetimeIndex(['1992-02-24'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1992-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1992-05-12 00:00:00
-----------
199209
DatetimeIndex(['1992-03-05'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1992-12-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1992-08-12 00:00:00
-----------
199212
DatetimeIndex(['1992-06-09'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1993-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
1992-11-11 00:00:00
-----------
199303
DatetimeIndex(['1992-11-10'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1993-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1993-02-09 00:00:00
-----------
199306
DatetimeIndex(['1992-11-10'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1993-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1993-05-12 00:00:00
-----------
199309
DatetimeIndex(['1993-03-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1993-12-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1993-08-12 00:00:00
-----------
199312
DatetimeIndex(['1993-08-18'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1994-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
1993-11-11 00:00:00
-----------
199403
DatetimeIndex(['1993-10-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1994-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1994-02-09 00:00:00
-----------
199406
DatetimeIndex(['1994-01-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1994-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1994-05-12 00:00:00
-----------
199409
DatetimeIndex(['1994-05-09'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1994-12-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1994-08-12 00:00:00
-----------
199412
DatetimeIndex(['1994-08-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1995-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
1994-11-11 00:00:00
-----------
199503
DatetimeIndex(['1994-10-26'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1995-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1995-02-09 00:00:00
-----------
199506
DatetimeIndex(['1994-11-18'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1995-09-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1995-05-12 00:00:00
-----------
199509
DatetimeIndex(['1995-02-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1995-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1995-08-11 00:00:00
-----------
199512
DatetimeIndex(['1995-07-26'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1996-03-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1995-11-10 00:00:00
-----------
199603
DatetimeIndex(['1995-10-06'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1996-06-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1996-02-09 00:00:00
-----------
199606
DatetimeIndex(['1995-11-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1996-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1996-05-13 00:00:00
-----------
199609
DatetimeIndex(['1996-03-25'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1996-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1996-08-12 00:00:00
-----------
199612
DatetimeIndex(['1996-07-26'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1997-03-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1996-11-11 00:00:00
-----------
199703
DatetimeIndex(['1996-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1997-06-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1997-02-10 00:00:00
-----------
199706
DatetimeIndex(['1997-01-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1997-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1997-05-12 00:00:00
-----------
199709
DatetimeIndex(['1997-02-11'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1997-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1997-08-12 00:00:00
-----------
199712
DatetimeIndex(['1997-08-25'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1998-03-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
1997-11-11 00:00:00
-----------
199803
DatetimeIndex(['1997-11-05'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1998-06-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
1998-02-09 00:00:00
-----------
199806
DatetimeIndex(['1998-02-24'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1998-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1998-05-12 00:00:00
-----------
199809
DatetimeIndex(['1998-04-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1998-12-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1998-08-12 00:00:00
-----------
199812
DatetimeIndex(['1998-07-17'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1999-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
1998-11-11 00:00:00
-----------
199903
DatetimeIndex(['1998-10-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1999-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1999-02-09 00:00:00
-----------
199906
DatetimeIndex(['1998-12-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1999-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1999-05-12 00:00:00
-----------
199909
DatetimeIndex(['1999-06-16'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['1999-12-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
1999-08-12 00:00:00
-----------
199912
DatetimeIndex(['1999-08-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2000-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
1999-11-11 00:00:00
-----------
200003
DatetimeIndex(['1999-12-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2000-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2000-02-10 00:00:00
-----------
200006
DatetimeIndex(['2000-03-17'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2000-09-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
2000-05-12 00:00:00
-----------
200009
DatetimeIndex(['2000-06-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2000-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2000-08-11 00:00:00
-----------
200012
DatetimeIndex(['2000-06-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2001-03-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2000-11-10 00:00:00
-----------
200103
DatetimeIndex(['2000-08-07'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2001-06-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
2001-02-09 00:00:00
-----------
200106
DatetimeIndex(['2001-01-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2001-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2001-05-11 00:00:00
-----------
200109
DatetimeIndex(['2001-04-05'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2001-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2001-08-13 00:00:00
-----------
200112
DatetimeIndex(['2001-08-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2002-03-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2001-11-12 00:00:00
-----------
200203
DatetimeIndex(['2001-11-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2002-06-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2002-02-08 00:00:00
-----------
200206
DatetimeIndex(['2002-03-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2002-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2002-05-13 00:00:00
-----------
200209
DatetimeIndex(['2002-06-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2002-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2002-08-12 00:00:00
-----------
200212
DatetimeIndex(['2002-08-26'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2003-03-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
2002-11-11 00:00:00
-----------
200303
DatetimeIndex(['2002-12-09'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2003-06-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2003-02-10 00:00:00
-----------
200306
DatetimeIndex(['2003-03-05'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2003-09-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2003-05-12 00:00:00
-----------
200309
DatetimeIndex(['2003-05-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2003-12-19'], dtype='datetime64[ns]', name=u'Date', freq=None)
2003-08-12 00:00:00
-----------
200312
DatetimeIndex(['2003-09-08'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2004-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
2003-11-11 00:00:00
-----------
200403
DatetimeIndex(['2003-12-17'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2004-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2004-02-10 00:00:00
-----------
200406
DatetimeIndex(['2004-02-04'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2004-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2004-05-12 00:00:00
-----------
200409
DatetimeIndex(['2004-04-15'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2004-12-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
2004-08-12 00:00:00
-----------
200412
DatetimeIndex(['2004-08-23'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2005-03-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2004-11-11 00:00:00
-----------
200503
DatetimeIndex(['2004-09-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2005-06-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2005-02-09 00:00:00
-----------
200506
DatetimeIndex(['2005-01-24'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2005-09-21'], dtype='datetime64[ns]', name=u'Date', freq=None)
2005-05-12 00:00:00
-----------
200509
DatetimeIndex(['2005-02-25'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2005-12-20'], dtype='datetime64[ns]', name=u'Date', freq=None)
2005-08-12 00:00:00
-----------
200512
DatetimeIndex(['2005-06-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2006-03-22'], dtype='datetime64[ns]', name=u'Date', freq=None)
2005-11-11 00:00:00
-----------
200603
DatetimeIndex(['2005-07-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2006-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2006-02-09 00:00:00
-----------
200606
DatetimeIndex(['2006-01-04'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2006-09-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
2006-05-12 00:00:00
-----------
200609
DatetimeIndex(['2005-12-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2006-12-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
2006-08-11 00:00:00
-----------
200612
DatetimeIndex(['2006-08-24'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2007-03-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2006-11-10 00:00:00
-----------
200703
DatetimeIndex(['2006-11-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2007-06-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
2007-02-09 00:00:00
-----------
200706
DatetimeIndex(['2007-02-23'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2007-09-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
2007-05-11 00:00:00
-----------
200709
DatetimeIndex(['2007-05-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2007-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2007-08-13 00:00:00
-----------
200712
DatetimeIndex(['2007-07-25'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2008-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2007-11-12 00:00:00
-----------
200803
DatetimeIndex(['2007-07-25'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2008-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2008-02-11 00:00:00
-----------
200806
DatetimeIndex(['2008-01-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2008-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2008-05-12 00:00:00
-----------
200809
DatetimeIndex(['2008-01-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2008-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2008-08-12 00:00:00
-----------
200812
DatetimeIndex(['2008-01-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2009-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2008-11-11 00:00:00
-----------
200903
DatetimeIndex(['2008-04-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2009-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2009-02-09 00:00:00
-----------
200906
DatetimeIndex(['2008-07-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2009-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2009-05-12 00:00:00
-----------
200909
DatetimeIndex(['2008-10-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2009-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2009-08-12 00:00:00
-----------
200912
DatetimeIndex(['2009-01-02'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2010-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2009-11-11 00:00:00
-----------
201003
DatetimeIndex(['2009-04-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2010-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2010-02-09 00:00:00
-----------
201006
DatetimeIndex(['2009-07-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2010-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2010-05-12 00:00:00
-----------
201009
DatetimeIndex(['2009-10-01'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2010-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2010-08-12 00:00:00
-----------
201012
DatetimeIndex(['2010-01-04'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2011-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2010-11-11 00:00:00
-----------
201103
DatetimeIndex(['2010-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2011-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2011-02-09 00:00:00
-----------
201106
DatetimeIndex(['2010-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2011-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2011-05-12 00:00:00
-----------
201109
DatetimeIndex(['2010-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2011-12-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2011-08-12 00:00:00
-----------
201112
DatetimeIndex(['2010-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2012-03-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2011-11-11 00:00:00
-----------
201203
DatetimeIndex(['2011-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2012-06-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
2012-02-10 00:00:00
-----------
201206
DatetimeIndex(['2011-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2012-09-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
2012-05-11 00:00:00
-----------
201209
DatetimeIndex(['2011-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2012-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2012-08-13 00:00:00
-----------
201212
DatetimeIndex(['2011-12-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2013-03-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
2012-11-12 00:00:00
-----------
201303
DatetimeIndex(['2012-03-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2013-06-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
2013-02-08 00:00:00
-----------
201306
DatetimeIndex(['2012-06-29'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2013-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2013-05-13 00:00:00
-----------
201309
DatetimeIndex(['2012-09-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2013-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2013-08-12 00:00:00
-----------
201312
DatetimeIndex(['2012-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2014-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2013-11-11 00:00:00
-----------
201403
DatetimeIndex(['2013-03-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2014-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2014-02-10 00:00:00
-----------
201406
DatetimeIndex(['2013-06-28'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2014-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2014-05-12 00:00:00
-----------
201409
DatetimeIndex(['2013-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2014-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2014-08-12 00:00:00
-----------
201412
DatetimeIndex(['2014-02-14'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2015-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2014-11-11 00:00:00
-----------
201503
DatetimeIndex(['2014-03-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2015-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2015-02-09 00:00:00
-----------
201506
DatetimeIndex(['2014-06-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2015-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
2015-05-12 00:00:00
-----------
201509
DatetimeIndex(['2014-09-30'], dtype='datetime64[ns]', name=u'Date', freq=None)
DatetimeIndex(['2015-12-31'], dtype='datetime64[ns]', name=u'Date', freq=None)
2015-08-02 00:00:00
-----------
```

```python
#print cts_assigned.columns
#print cts_assigned.ix['2008-11-10']
#print cts_assigned.ix['2008-11-11']
#print cts_assigned.ix['2008-11-12']
#2008-11-11
print ctd['200809'].tail(1)
print ctd['200812'].ix['2008-11-10']
print ctd['200903'].ix['2008-11-10']
```

```text
                   h         l         o     oi         s  v
Date                                                        
2008-09-30  113.6875  113.6875  113.6875  19282  113.6875  0
h         115.703125
l         115.296875
o         115.296875
oi    1274665.000000
s         115.703125
v         117.000000
Name: 2008-11-10 00:00:00, dtype: float64
h       113.500000
l       113.156250
o       113.156250
oi    35245.000000
s        92.601548
v       117.000000
Name: 2008-11-10 00:00:00, dtype: float64
```
































