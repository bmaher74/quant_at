import os, futures, pandas as pd, datetime
from pymongo import MongoClient
import numpy as np
import Quandl

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
    assert res[0]['oi'] == 5027.0
    res = futures.get(market="CME", sym="CL", month="G", year=1984, dt=19830624, db=testdb)
    assert res[0]['oi'] == 5.0
    res = futures.last_contract("CL","CME", db)
    assert res[0]['_id']['month'] == 'G'

    res = futures.existing_nonexpired_contracts("CL","CME", db,fake_today_1())
    assert len(res) == 0
    res = futures.existing_nonexpired_contracts("CL","CME", db,fake_today_2())
    assert len(res) > 0

def test_incremental():
    db = init()
    futures.download_data(downloader=fake_download_2,today=fake_today_726,
                          db=testdb, years=(1984,1985))
    print futures.last_date_in_contract("CL","CME","F", 1984, db)
    assert futures.last_date_in_contract("CL","CME","F", 1984, db) == 19830726    

    futures.download_data(downloader=fake_download_3,today=fake_today_727,
                          db=testdb, years=(1984,1985))
    assert futures.last_date_in_contract("CL","CME","F", 1984, db) == 19830727

def test_stitch():
    stitch_points = ['2015-03-13','2015-04-15']
    dfs = []
    dfs.append(pd.read_csv('test/data_stitch/vixmay.csv',index_col=0,parse_dates=True))
    dfs.append(pd.read_csv('test/data_stitch/vixjune.csv',index_col=0,parse_dates=True))
    dfs.append(pd.read_csv('test/data_stitch/vixjuly.csv',index_col=0,parse_dates=True))
    res = futures.stitch(dfs,'Settle',stitch_points)
    exp = pd.read_csv('test/data_stitch/stitch_expected.csv',index_col=0,parse_dates=True)
    exp['res'] = res
    assert np.sum(exp.res-exp.Settle) < 1
            
if __name__ == "__main__":    
    test_simple()
    test_incremental()
    test_stitch()
    
