import sys; sys.path.append('../data')
import futures, datetime, logging, os
import pickle, pandas as pd
import numpy as np
import matplotlib.pyplot as plt

insts = pd.read_csv('instr1.csv',index_col=[0,1],comment='#').to_dict('index')
print insts

for (sym,market) in insts.keys(): 
    print sym, market
    futures.combine_contract_info_save(sym, market, insts, db="findb")
    
