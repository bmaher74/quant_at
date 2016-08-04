import pandas as pd, util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys; sys.path.append('../data');
import futures
import sys; sys.path.append('c:/Users/burak/Documents/classnotes/tser/tser_port')
import boot

dff = pd.read_csv("outfore.csv",index_col=0,parse_dates=True)
dfp = pd.read_csv("outpri.csv",index_col=0,parse_dates=True)
df = dfp.pct_change() * dff.shift(1)
df = df.dropna()
print df.tail()
print 'optimizing...'
weights=boot.optimise_over_periods(df,rollyears=20, monte_carlo=20,monte_length=250)
weights.to_csv("outw.csv")
