import sys; sys.path.append('../data')
import sys; sys.path.append('../book')
import pandas as pd, dd
import numpy as np 
import simple, util

col = 'a'; px = simple.get('IBB')

ret = util.ewmac(px,col,8,32)
print ret
