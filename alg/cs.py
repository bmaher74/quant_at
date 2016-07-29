import sys; sys.path.append('../data')
import futures, datetime, logging, os
import pickle, pandas as pd
import numpy as np
import matplotlib.pyplot as plt

insts = pd.read_csv('instruments.csv',index_col=0,comment='#').to_dict()

#inst = "FV"
inst = "CL"
market = insts['market'][inst]
rollcycle = insts['rollcycle'][inst]
rolloffset = insts['rolloffset'][inst]
expday = insts['expday'][inst]
expmon = insts['expmon'][inst]
carryoffset = insts['carryoffset'][inst]
print inst, market, rollcycle, rolloffset, expday, expmon, carryoffset
ctd = futures.get_contracts(market,inst,1990,futures.systemtoday().year)
cts_assigned = futures.which_contract(inst, ctd, rollcycle, rolloffset, expday, expmon)
df_carry = futures.create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
df_stitched = futures.stitch_contracts(cts_assigned, ctd, 's')
df_stitched.plot()
plt.savefig('misc_01.png')



