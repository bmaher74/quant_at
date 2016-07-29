import sys; sys.path.append('../data')
import futures, datetime
import pickle, pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_carry2 = pd.read_csv("out1.csv",index_col=0,parse_dates=True)
cts_assigned2 = pickle.load( open( "cts_assigned.pkl", "rb" ) )
ctd2 = pickle.load( open( "ctd.pkl", "rb" ) )
df_stitched2 = futures.stitch_contracts(cts_assigned2, ctd2, 's')

# insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()
# for inst in insts['rolloffset']:
#     market = insts['market'][inst]
#     rollcycle = insts['rollcycle'][inst]
#     rolloffset = insts['rolloffset'][inst]
#     expday = insts['expday'][inst]
#     expmon = insts['expmon'][inst]
#     carryoffset = insts['carryoffset'][inst]
#     print inst, market, rollcycle, rolloffset, expday, expmon, carryoffset
#     ctd = futures.get_contracts(market,inst,1980,futures.systemtoday().year)
#     cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
#     df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
#     df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
#     df_stitched.plot()
#     plt.savefig('misc_%s_01.png' % inst)

