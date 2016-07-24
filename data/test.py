import os, futures, pandas as pd, datetime
from pymongo import MongoClient
import numpy as np, sys, Quandl
sys.path.append('../alg')
import util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

testdb = "fakedb"

def load_data(contract,subdir,start,end):
    f = contract.replace("/","-")
    f = "./test/%s/%s.csv" % (subdir,f)
    if not os.path.isfile(f): raise Quandl.Quandl.DatasetNotFound()
    df = pd.read_csv(f)
    df = df.set_index("Date")
    df = df[df.index > start]
    return df
    
def fake_download_1(contract,start,end):
    return load_data(contract, "data_1",start,end)

def fake_download_2(contract,start,end):
    return load_data(contract, "data_2",start,end)

def fake_download_3(contract,start,end):
    return load_data(contract, "data_3",start,end)

def fake_download_crude(contract,start,end):
    return load_data(contract, "data_crude",start,end)

def fake_today_1():
    return datetime.datetime(2016, 5, 1) 

def fake_today_2():
    return datetime.datetime(1984, 1, 1) 

def fake_today_726():
    return datetime.datetime(1983, 7, 26) 

def fake_today_727():
    return datetime.datetime(1983, 7, 27) 

def init():
    c = MongoClient()
    c[testdb].futures.drop()
    c[testdb].tickers.drop()
    return c[testdb]

def test_simple():
    db = init()
    futures.download_data(downloader=fake_download_1,today=fake_today_1,
                          db=testdb, years=(1984,1985))
    res = futures.get(market="CME", sym="CL", month="F", year=1984, dt=19831205, db=testdb)
    assert (res[0]['oi'] == 5027.0)
    res = futures.get(market="CME", sym="CL", month="G", year=1984, dt=19830624, db=testdb)
    assert (res[0]['oi'] == 5.0)
    res = futures.last_contract("CL","CME", db)
    assert (res[0]['_id']['month'] == 'G')
    res = futures.existing_nonexpired_contracts("CL","CME", fake_today_1(), db)
    assert (len(res) == 0)
    res = futures.existing_nonexpired_contracts("CL","CME", fake_today_2(), db)
    assert (len(res) > 0)
    res = futures.get_contract(market="CME", sym="CL", month="G", year=1984, db=testdb)
    assert (len(res)==143)
    
def test_incremental():
    db = init()
    futures.download_data(downloader=fake_download_2,today=fake_today_726,
                          db=testdb, years=(1984,1985))
    print futures.last_date_in_contract("CL","CME","F", 1984, db)
    assert (futures.last_date_in_contract("CL","CME","F", 1984, db) == 19830726)
    futures.download_data(downloader=fake_download_3,today=fake_today_727,
                          db=testdb, years=(1984,1985))
    assert (futures.last_date_in_contract("CL","CME","F", 1984, db) == 19830727)

def test_stitch():
    stitch_points = ['2015-03-13','2015-04-15']
    dfs = []
    base = 'test/data_stitch/vix%s.csv'
    for f in ['may','june','july']:
        dfs.append(pd.read_csv(base % f,index_col=0,parse_dates=True))
    res = futures.stitch_prices(dfs,'Settle',stitch_points)
    exp = pd.read_csv('test/data_stitch/stitch_expected.csv',index_col=0,parse_dates=True)
    exp['res'] = res
    assert (np.sum(exp.res-exp.Settle) < 1)

def test_missing_contract():
    db = init()
    futures.download_data(downloader=fake_download_1,today=fake_today_1,
                          db=testdb, years=(1984,1985))
    res = futures.get_contract(market="CME", sym="CL", month="Z", year=1984, db=testdb)
    assert (res==None)
    
def test_one_load():
    db = init()
    futures.download_and_save(work_items=[('CME','CL','G',1984,'1980-01-01')],
                              db=db.futures,
                              downloader=fake_download_2)
    
    res = futures.get_contract(market="CME", sym="CL", month="G", year=1984, db=testdb)
    assert (len(res) == 22)

def test_rollover():
    db = init()
    futures.download_data(downloader=fake_download_crude,today=fake_today_1,
                          db=testdb, years=(2007,2013))
    ctd = futures.get_contracts("CME","CL",2006,2014,db=testdb)
    print len(ctd)
    roll = "Z"; rolloff = 50; expday = 25; expmon = "prev"
    res2 = futures.which_contract("CL", ctd, roll, rolloff, expday, expmon)
    carryoff = -1
    res3 = futures.create_carry(res2[pd.isnull(res2.effcont)==False],carryoff,ctd)
    raw_carry = res3.carryprice-res3.effprice
    vol = util.robust_vol_calc(res3.effprice.diff())
    def carry(daily_ann_roll, vol, diff_in_years, smooth_days=90):
        ann_stdev = vol * util.ROOT_BDAYS_INYEAR
        raw_carry = daily_ann_roll / ann_stdev
        smooth_carry = pd.ewma(raw_carry, smooth_days) / diff_in_years
        return smooth_carry.fillna(method='ffill')
    resc =  carry(raw_carry, vol,  carryoff*1/util.CALENDAR_DAYS_IN_YEAR)
    assert (util.sharpe(res3.effprice, resc) - 0.4) < 0.01
    dfs = futures.stitch_contracts(res2, ctd, 's')

    
if __name__ == "__main__":    
    test_simple()
    test_incremental()
    test_stitch()
    test_missing_contract()
    test_one_load()
    if len(sys.argv) > 1 and sys.argv[1] == '--extra':
        # this is a slow one
        test_rollover()
        
