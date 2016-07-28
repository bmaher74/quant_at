import sys; sys.path.append('../data')
import futures, datetime
import pickle, pandas as pd
import numpy as np

df_carry2 = pd.read_csv("out1.csv",index_col=0,parse_dates=True)
cts_assigned2 = pickle.load( open( "cts_assigned.pkl", "rb" ) )
ctd2 = pickle.load( open( "ctd.pkl", "rb" ) )

def sc(dfc, ctd, price_col):
    tmp = dfc.effcont.dropna().astype(int).diff().dropna()
    rolldates = tmp[tmp > 0].index
    rollconts = np.unique(dfc.effcont.dropna())
    rollconts = [x for x in rollconts if x in ctd]
    rolldates = [x for x in rolldates if \
                 int("%d%02d" % (x.year, x.month)) >= int(ctd.keys()[0]) and \
                 int("%d%02d" % (x.year, x.month)) <= int(ctd.keys()[-1])]

    tmp = [ctd[x] for x in rollconts]
    tmp_keys = [x for x in rollconts]
    print len(tmp_keys), len(rolldates)

    print '----------------------------------'
    for i,x in enumerate(rolldates):
        print "rolldate", rolldates[i], "contract", tmp_keys[i], tmp_keys[i+1]
    
    for i,x in enumerate(rolldates):
        for j in range(5):
            print "adjusting rolldate", rolldates[i], "contract", tmp_keys[i], tmp_keys[i+1]
            rolldates[i] = rolldates[i] - datetime.timedelta(days=1)
            if rolldates[i] in tmp[i].index and rolldates[i] in tmp[i+1].index:
                break  
        if rolldates[i] not in tmp[i].index or rolldates[i] not in tmp[i+1].index:
            print "Error"            
            print tmp[i].head(1).index[0], tmp[i].tail(1).index[0]
            print tmp[i+1].head(1).index[0], tmp[i+1].tail(1).index[0]
            exit()
            
    print '----------------------------------'
    for i,x in enumerate(rolldates):
        print "rolldate", rolldates[i], "contract", tmp_keys[i], tmp_keys[i+1]

    dfs = futures.stitch_prices(tmp, price_col, rolldates, ctd)

df_stitched2 = sc(cts_assigned2, ctd2, 's')
