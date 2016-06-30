#
# Futures Contracts downloader - symbols are in futures.csv, each
# symbol in this file is retrieved from Quandl and inserted into a
# Mongo database. At each new invocation, only new data for
# non-expired contracts are downloaded. 
#
# F - Jan, G - Feb, H - Mar, J - Apr, K - May, M - Jun
# N - Jul, Q - Aug, U - Sep, V - Oct, X - Nov, Z - Dec
#

import Quandl, os, itertools, sys
from pymongo import MongoClient
import logging, datetime, simple
import pandas as pd
import numpy as np
from memo import *

contract_month_codes = ['F', 'G', 'H', 'J', 'K', 'M','N', 'Q', 'U', 'V', 'X', 'Z']
contract_month_dict = dict(zip(contract_month_codes,range(1,len(contract_month_codes)+1)))

def web_download(contract,start,end):
    df = Quandl.get(contract,trim_start=start,trim_end=end,
                    returns="pandas",authtoken=simple.get_quandl_auth())
    return df

def systemtoday():
    return datetime.datetime.today()

def get(market, sym, month, year, dt, db="findb"):
    """
    Returns all data for symbol in a pandas dataframe
    """
    connection = MongoClient()
    db = connection[db]
    yearmonth = "%d%s" % (year,month)
    q = {"$query" :{"_id": {"sym": sym, "market": market, "month": month,
                            "year": year, "yearmonth": yearmonth, "dt": dt }} }
    res = list(db.futures.find( q ))
    return res

def get_contract(market, sym, month, year, db="findb"):
    """
    Returns all data for symbol in a pandas dataframe
    """
    connection = MongoClient()
    db = connection[db]
    res = []
    yearmonth = "%d%s" % (year,month)
    q = {"$query" : {"_id.sym": sym, "_id.market": market, "_id.yearmonth": yearmonth },
         "$orderby":{"_id.dt" : 1} 
    }
    res = list(db.futures.find( q ))
    res = pd.DataFrame(res)
    res['Date'] = res['_id'].map(lambda x: datetime.datetime.strptime(str(x["dt"]), '%Y%m%d'))
    res = res.drop('_id',axis=1)
    res = res.set_index('Date')
    return res

def last_contract(sym, market, db="findb"):
    q = { "$query" : {"_id.sym": sym, "_id.market": market}, "$orderby":{"_id.yearmonth" : -1} }
    res = db.futures.find(q).limit(1)    
    return list(res) 

def existing_nonexpired_contracts(sym, market, today, db="findb"):
    yearmonth = "%d%s" % (today.year,contract_month_codes[today.month-1])
    q = { "$query" : {"_id.sym": sym, "_id.market": market,
                      "_id.yearmonth": {"$gte": yearmonth } }
    }
    res = {}
    for x in db.futures.find(q): res[(x['_id']['year'],x['_id']['month'])]=1
    return res.keys()

def get_contracts(market, sym, from_year, to_year):
    """
    Get all contracts, from jan to dec, between given years
    """
    res = []
    for year in range(from_year,to_year):
        for month in contract_month_codes:
     	    res.append(get_contract(market=market, sym=sym, month=month, year=year))
    return res	    

def last_date_in_contract(sym, market, month, year, db="findb"):
    q = { "$query" : {"_id.sym": sym, "_id.market": market,
                      "_id.month": month, "_id.year": year},
          "$orderby":{"_id.dt" : -1}          
    }
    res = db.futures.find(q).limit(1)
    res = list(res)
    if len(res) > 0: return res[0]['_id']['dt']

def download_data(chunk=1,chunk_size=1,downloader=web_download,
                  today=systemtoday,db="findb",years=(1984,2022)):

    # a tuple of contract years, defining the beginning
    # of time and end of time
    start_year,end_year=years
    futcsv = pd.read_csv('futures.csv')
    instruments = zip(futcsv.Symbol,futcsv.Market)

    str_start = datetime.datetime(start_year-2, 1, 1).strftime('%Y-%m-%d')
    str_end = today().strftime('%Y-%m-%d')
    today_month,today_year = today().month, today().year
    
    connection = MongoClient()
    futures = connection[db].futures

    work_items = []
        
    # download non-existing / missing contracts - this is the case of
    # running for the first time, or a new contract became available
    # since the last time we ran.
    for (sym,market) in instruments:
        last = last_contract(sym, market, connection[db])
        for year in range(start_year,end_year):
            for month in contract_month_codes:
                if len(last)==0 or (len(last) > 0 and last[0]['_id']['yearmonth'] < "%d%s" % (year,month)):
                    # for non-existing contracts, get as much as possible
                    # from str_start (two years from the beginning of time)
                    # until the end of time
                    work_items.append([market, sym, month, year, str_start])

        # for existing contracts, add to the work queue the download of
        # additional days that are not there. if today is a new day, and
        # for for existing non-expired contracts we would have new price
        # data.  
        for (nonexp_year,nonexp_month) in existing_nonexpired_contracts(sym, market, today(), connection[db]):
            last_con = last_date_in_contract(sym,market,nonexp_month,nonexp_year,connection[db])
            last_con = pd.to_datetime(str(last_con), format='%Y%m%d')
            logging.debug("last date contract %s" % last_con)
            if today() > last_con: work_items.append([market, sym, nonexp_month, nonexp_year, last_con.strftime('%Y-%m-%d')])

    for market, sym, month, year, work_start in work_items:
        contract = "%s/%s%s%d" % (market,sym,month,year)
        try:
            logging.debug(contract)
            df = downloader(contract,work_start,str_end)
            # sometimes oi is in Prev Days Open Interest sometimes just Open Interest
            # use whichever is there
            oicol = [x for x in df.columns if 'Open Interest' in x][0]
            yearmonth = "%d%s" % (year,month)
            logging.debug("%d records" % len(df))
            for srow in df.iterrows():
                dt = str(srow[0])[0:10]
                dt = int(dt.replace("-",""))
                new_row = {"_id": {"sym": sym, "market": market, "month": month,
                                   "year": year, "yearmonth": yearmonth, "dt": dt },
                           "o": srow[1].Open,
                           "h": srow[1].High,
                           "l": srow[1].Low,
                           "s": srow[1].Settle,
                           "v": srow[1].Volume,
                           "oi": srow[1][oicol]
                }

                futures.save(new_row)

        except Quandl.Quandl.DatasetNotFound:
            logging.error("No dataset")

def shift(lst,empty):
    res = lst[:]
    temp = res[0]
    for index in range(len(lst) - 1): res[index] = res[index + 1]         
    res[index + 1] = temp
    res[-1] = empty
    return res
    
def stitch(dfs, price_col, dates):
    """Stitches together a list of contract prices. dfs should contain a
    list of dataframe objects, price_col is the column name to be
    combined, and dates is a list of stitch dates. The dataframes must
    be date indexed, and the order of dates must match the order of
    the dataframes. The stitching method is called the Panama method -
    more details can be found at
    http://qoppac.blogspot.de/2015/05/systems-building-futures-rolling.html
    """
    
    res = []
    datesr = list(reversed(dates))
    dfsr = list(reversed(dfs))    
    dfsr_pair = shift(dfsr,pd.DataFrame())
        
    for i,v in enumerate(datesr):
        tmp1=float(dfsr[i].ix[v,price_col])
        tmp2=float(dfsr_pair[i].ix[v,price_col])
        dfsr_pair[i].loc[:,price_col] = dfsr_pair[i][price_col] + tmp1-tmp2

    dates.insert(0,'1900-01-01')
    dates_end = shift(dates,'2200-01-01')
    
    for i,v in enumerate(dates):
        tmp = dfs[i][(dfs[i].index > dates[i]) & (dfs[i].index <= dates_end[i])]
        res.append(tmp.Settle)
    return pd.concat(res)

def contract_per_date(contracts, method):
    """Forms a single continuous timeline from dates in contracts, and for
    each date it calculates which contract should be active for which
    date, depending on rollover method.
    """ 
    start_date = contracts[0].head(1).index[0] # first dt of first contract
    end_date = contracts[-1].tail(1).index[0] # last date of last contract
    delta = end_date - start_date
    dates = []
    # get bizdays between start and end
    for i in range(delta.days + 1):
    	day = start_date + datetime.timedelta(days=i)
	if day.weekday() < 5: dates.append(day)
    df = pd.DataFrame(index=dates)
    if method=="out_40_months_every_90_days":
        # roll every 6 weeks, go to the 40 month ahead
        # do the calculation only every 90 days
        df2 = df.resample("3M",how="first")
        # get the contract 40 months out
        df2['Date40'] = df2.index.map(lambda x: x+datetime.timedelta(days=40*30))
        df2['contract'] = df2.Date40.map(lambda x: "%d%02d" % (x.year, x.month))
        df['contract'] = df2.contract
        df.contract = df.contract.fillna(method="ffill")
        df.contract = df.contract.fillna(method="bfill")
    elif method=="hold_dec_roll_nov":
        # in the middle of november, roll to the december of next year
        df = pd.DataFrame(index=dates)
        # only take novembers
        df2 = df[df.index.month == 11]
        df2['year'] = df2.index.year
        # need to measure 'middle of november', smallest distance to nov 15
        df2['mid'] = df2.index.map(lambda x: np.abs(x.day-15))
        # pick the min mid out of year
        df2 = df2[df2.groupby(['year'])['mid'].transform(min) == df2['mid']]
        df2['contract'] = df2.index.map(lambda x: "%d%02d" % (x.year+1, 12))
        df['contract'] = df2.contract
        df.contract = df.contract.fillna(method="ffill")                
        df.to_csv('out.csv')
        
    return df
        
            
if __name__ == "__main__":

    simple.check_mongo()    
    
    f = '%(asctime)-15s: %(message)s'
    if len(sys.argv) == 3:
        p = (os.environ['TEMP'],int(sys.argv[1]))
        logging.basicConfig(filename='%s/futures-%d.log' % p,level=logging.DEBUG,format=f)
        download_data(chunk=int(sys.argv[1]),chunk_size=int(sys.argv[2]))
    else:
        logging.basicConfig(filename='%s/futures.log' % os.environ['TEMP'],level=logging.DEBUG, format=f)
        download_data()

        
