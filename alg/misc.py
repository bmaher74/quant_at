import pandas as pd, util
import numpy as np
import matplotlib.pyplot as plt
import sys; sys.path.append('../data');
import futures
import sys; sys.path.append('c:/Users/burak/Documents/classnotes/tser/tser_port')
import boot
import util, zipfile, pandas as pd
import sys; sys.path.append('../data')
import futures, collections

ewmacs = [(16,64),(32,128),(64,256)]

forecasts = collections.OrderedDict()
for x in ewmacs: forecasts[x] = []
forecasts['carry'] = []
prices = collections.OrderedDict()
for x in ewmacs: prices[x] = []
prices['carry'] = []

insts = ['CORN', 'EDOLLAR', 'EUROSTX', 'MXP', 'US10', 'V2X']
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
    for inst in insts: 
        df1 = pd.read_csv(z.open('%s_price.csv' % inst), index_col=0,parse_dates=True )     
        df2 = pd.read_csv(z.open('%s_carrydata.csv' % inst), index_col=0,parse_dates=True )     
        for (fast,slow) in ewmacs:
             vol = util.robust_vol_calc(df1.PRICE.diff())
             forecasts[(fast,slow)].append(util.ewma(df1.PRICE, fast, slow))
             prices[(fast,slow)].append(df1.PRICE)

        raw_carry = df2.CARRY_CONTRACT-df2.PRICE_CONTRACT
        carryoffset = df2.PRICE_CONTRACT - df2.CARRY_CONTRACT
        forecast =  util.carry(raw_carry, vol,  carryoffset*1/util.CALENDAR_DAYS_IN_YEAR)
        forecasts['carry'].append(forecast)
        prices['carry'].append(df1.PRICE)
    
for x in forecasts:
    forecasts[x] = pd.concat(forecasts[x])
for x in prices:
    prices[x] = pd.concat(prices[x])
    
dff = pd.DataFrame()
for x in forecasts: dff[x] = forecasts[x]
dfp = pd.DataFrame()
for x in prices: dfp[x] = prices[x]

rng = pd.date_range('1/1/1900', periods=len(dff), freq='D')

dff = dff.set_index(rng)
dfp = dfp.set_index(rng)

df = dfp.pct_change() * dff.shift(1)
df = df.dropna()
print 'optimizing...'
weights=boot.optimise_over_periods(df,rollyears=20, monte_carlo=20,monte_length=250)
weights.to_csv("outw.csv")
