import Quandl, os, itertools, sys
from pymongo import MongoClient
import logging, datetime, simple
import pandas as pd, collections
import numpy as np
from memo import *

contract_month_codes = ['F', 'G', 'H', 'J', 'K', 'M','N', 'Q', 'U', 'V', 'X', 'Z']
contract_month_dict = dict(zip(contract_month_codes,range(1,len(contract_month_codes)+1)))

def web_download(contract,start,end):
    df = Quandl.get(contract,trim_start=start,trim_end=end,
                    returns="pandas",authtoken=simple.get_quandl_auth())
    return df

def systemtoday():
    #return datetime.datetime.today()
    return datetime.datetime(2016, 6, 30) 

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
    Returns all data for contract symbol in a pandas dataframe
    """
    connection = MongoClient()
    db = connection[db]
    res = []
    yearmonth = "%d%s" % (year,month)
    q = {"$query" : {"_id.sym": sym, "_id.market": market, "_id.yearmonth": yearmonth },
         "$orderby":{"_id.dt" : 1} 
    }
    res = list(db.futures.find( q ))
    if len(res) == 0: return None
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

def get_contracts(market, sym, from_year, to_year, db="findb"):
    """
    Get all contracts, from jan to dec, between (and including) given years,
    for all possible year / month combination.

    Returns: An ordered dictionary whose key is YYYYMM year-month code,
    and value is the contract in a dataframe.
    """
    res = collections.OrderedDict()
    for year in range(from_year,to_year+1):
        for month in contract_month_codes:
            c = get_contract(market=market, sym=sym, month=month, year=year, db=db)
            key = "%d%02d" % (year,contract_month_dict[month])
            if 'DataFrame' in str(type(c)): res[key] = c
    return res	    

def last_date_in_contract(sym, market, month, year, db="findb"):
    q = { "$query" : {"_id.sym": sym, "_id.market": market,
                      "_id.month": month, "_id.year": year},
          "$orderby":{"_id.dt" : -1}          
    }
    res = db.futures.find(q).limit(1)
    res = list(res)
    if len(res) > 0: return res[0]['_id']['dt']

def download_and_save(work_items, db, downloader=web_download, today=systemtoday):
    for market, sym, month, year, work_start in work_items:
        contract = "%s/%s%s%d" % (market,sym,month,year)
        try:
            logging.debug(contract)
            df = downloader(contract,work_start,today().strftime('%Y-%m-%d'))
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
                db.save(new_row)

        except Quandl.Quandl.DatasetNotFound:
            logging.error("No dataset")
    
    
def download_data(downloader=web_download,today=systemtoday,db="findb",years=(1984,2022)):

    """
    Futures Contracts downloader - symbols are in futures.csv, each
    symbol in this file is retrieved from Quandl and inserted into a
    Mongo database. At each new invocation, only new data for
    non-expired contracts are downloaded. 
    """
    
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

    download_and_save(work_items, futures, downloader, today)

def shift(lst,empty):
    res = lst[:]
    temp = res[0]
    for index in range(len(lst) - 1): res[index] = res[index + 1]         
    res[index + 1] = temp
    res[-1] = empty
    return res
    
def stitch_prices(dfs, price_col, dates, ctd):
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
        #print 'stitching'
        #print dfsr[i].head(1).index[0],dfsr[i].tail(1).index[0]
        #print dfsr_pair[i].head(1).index[0], dfsr_pair[i].tail(1).index[0]
        #print 'with', v
        tmp1=float(dfsr[i].ix[v,price_col])
        tmp2=float(dfsr_pair[i].ix[v,price_col])
        dfsr_pair[i].loc[:,price_col] = dfsr_pair[i][price_col] + tmp1-tmp2

    dates.insert(0,'1900-01-01')
    dates_end = shift(dates,'2200-01-01')
    
    for i,v in enumerate(dates):
        tmp = dfs[i][(dfs[i].index > dates[i]) & (dfs[i].index <= dates_end[i])]
        res.append(tmp[price_col])
    return pd.concat(res)

def rolldates(cts_assigned):
    """
    Converts the date-contract assignment dataframe, coming from which_contract
    into a list of (rolldate,from_contract,to_contract) tuple.    
    """
    tmp = cts_assigned.effcont.dropna().astype(int).diff().dropna()
    rolls = tmp[tmp > 0].index
    cts_assigned_s =cts_assigned.shift(1)
    res = []
    for x in list(rolls):
    	 res.append((x, cts_assigned_s.ix[x].effcont, cts_assigned.ix[x].effcont))
    return res
    
def stitch_contracts(cts_assigned, ctd, price_col):
    """
    Using a contract mapped series and a dictionary of contracts,
    creates a continuous time series. 
    
    Inputs

    dfc: Date indexed series with each date mapped to a contract in YYYYMM format

    Returns
    """

    rolls = rolldates(cts_assigned)
    rolldates2 = []
    for (rolldate, from_con, to_con) in rolls:
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

    rolldates4 = []
    contracts = []
    for d,f,t in rolldates3:
    	contracts.append(f)
	contracts.append(t)
	rolldates4.append(d)

#    print len(rolldates4)
#    print len(np.unique(contracts))
    contracts = [ctd[x] for x in list(np.unique(contracts))]
    df_stitched = stitch_prices(contracts, 's', rolldates4, ctd2)
    return df_stitched

def which_contract(instrument, contract_list, cycle, offset, expday, expmon):
    """
    For a list of contracts it creates a continuous date index, and
    calculates which contract would be effective on that date for a
    given offset (how far ahead) and a rollcycle for the contracts in
    question.

    Returns: A date-indexed Dataframe and an effcont column which points to the
    effective contract for that date.
    """
    start_date = contract_list[contract_list.keys()[0]].head(1).index[0] # first dt of first contract
    end_date = contract_list[contract_list.keys()[-1]].tail(1).index[0] # last date of last contract
    delta = end_date - start_date
    dates = []
    # get bizdays between start and end
    for i in range(delta.days + 1):
    	day = start_date + datetime.timedelta(days=i)
	if day.weekday() < 5: dates.append(day)
    df = pd.DataFrame(index=dates)
    
    def closest_biz(d): # get closest biz day
    	diffs = np.abs((d - df.index).days)
    	return df.index[np.argmin(diffs)]

    cycle_d = [contract_month_dict[x] for x in cycle]
    df['effcont'] = np.nan
    for year in np.unique(df.index.year):
    	for c in cycle_d:
	    v = "%d%02d" % (year,c)
	    exp_d = datetime.datetime(year, c, expday)
            # sometimes expiration month is the previous month
            # this happens for crude oil for example
            if expmon=="prev": exp_d = exp_d - datetime.timedelta(days=30)
	    df.loc[closest_biz(exp_d),'effcont'] = v
            
    df = df.fillna(method='bfill')
    # get the contract offset days in the future - the little arithmetic
    # below was necessary to turn offset days into offset business days.
    df['effcont'] = df.effcont.shift(-int(offset*2/3 + 3))

    return df

def create_carry(df, offset, contract_list):
    """
    Creates a new column for the carry contract, gets prices for both
    effective and carry contracts.
    
    Input:
    
    df: Dataframe indexed by date which has an 'effcont' column for the effective
    contract for that day
    offset: How far / behind will we look for a carry contract in relation to the
    effective contract.

    Returns:
    Same dataframe df with carry contract, effective price, carry price colunns
    appended.
    """
    df2 = df.copy()
    df2['effcont'] = df2.effcont.astype(str)
    def offset_contract(con):
    	s = pd.to_datetime(con + "15", format='%Y%m%d')
    	ss = s + datetime.timedelta(days=30*offset)
    	return "%d%02d" % (int(ss.year), int(ss.month)) 
    df2['carrycont'] = df2.effcont.map(offset_contract)
    df2['effprice'] = df2.apply(lambda x: contract_list.get(x.effcont).s.get(x.name) if x.effcont in contract_list else np.nan,axis=1)
    df2['carryprice'] = df2.apply(lambda x: contract_list.get(x.carrycont).s.get(x.name) if x.carrycont in contract_list else np.nan,axis=1)
    return df2

if __name__ == "__main__":

    simple.check_mongo()    
    f = '%(asctime)-15s: %(message)s'
    logging.basicConfig(filename='%s/futures.log' % os.environ['TEMP'],level=logging.DEBUG, format=f)
    if len(sys.argv) == 4:
        if sys.argv[1] == "--load-save-cnt":
            """
            Download from web and load a single contract, example usage is
            futures.py --load-save-cnt CME CLX2004
            """
            x1,x1,market, cnt = sys.argv
            year=cnt[-4:]; mon=cnt[-5]; code=cnt[:-5]
            connection = MongoClient()
            findb = connection["findb"].futures
            download_and_save(work_items=[(market,code,mon,int(year),'1900-01-01')],db=findb)
            
    elif len(sys.argv) == 2:
        """
        Simply get the latest
        """
        if sys.argv[1] == "--latest":
            print 'latest'
            download_data()


#
# F - Jan, G - Feb, H - Mar, J - Apr, K - May, M - Jun
# N - Jul, Q - Aug, U - Sep, V - Oct, X - Nov, Z - Dec
#
