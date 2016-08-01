import sys; sys.path.append('../data')
import futures, datetime, logging, os
import pickle, pandas as pd
import numpy as np
import matplotlib.pyplot as plt

insts = pd.read_csv('instruments.csv',index_col=[0,1],comment='#').to_dict('index')
rollcycle = insts[("CL","CME")]['rollcycle']
print rollcycle
exit()

for (sym,market) in insts.to_dict('index').keys(): 
    print sym, market
    futures.combine_contract_info_save(inst, market, insts.to_dict(), db="findb")
    
   
