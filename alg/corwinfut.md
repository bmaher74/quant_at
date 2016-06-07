
Mr. Carver, I tried to compute estimates for bid/ask spreads. I did
this so I can compute costs even when I do not have bid/ask prices
available. What do you think of this approach? A paper by Corvin and
Schultz had a formula,

http://www3.nd.edu/~scorwin/papers/high-low_spreads.pdf

Based on it I developed the code below

```python
import pandas as pd
def f(x):
    beta = np.log(x.Ht/x.Lt)**2 + np.log(x.Ht1/x.Lt1)**2
    gamma = np.log( max(x.Ht,x.Ht1) / min(x.Lt,x.Lt1)  )**2
    alpha1 = (np.sqrt(2*beta)-np.sqrt(beta)) / (3 - 2*np.sqrt(2))
    alpha2 = np.sqrt(gamma / (3-2*np.sqrt(2)))
    alpha = alpha1 - alpha2
    S = 2*(np.exp(alpha)-1) / (1 + np.exp(alpha))
    return S

df = pd.read_csv('fesx.csv')
df['S'] = df.apply(f, axis=1)
df.loc[df.S<0,'S'] = np.nan
df['spread'] = df.settle * df.S
print df.head()
df.to_csv('bidask.csv',index=None)
```

```text
       date    Lt    Ht  settle   Lt1   Ht1         S     spread
0  20140623  3261  3261    3261  3264  3264       NaN        NaN
1  20140624  3264  3264    3264  3223  3237       NaN        NaN
2  20140625  3223  3237    3235  3199  3221       NaN        NaN
3  20140626  3199  3221    3210  3200  3225  0.005493  17.631555
4  20140627  3200  3225    3206  3194  3204       NaN        NaN
```

Code is correct (I compared it to a known output). For futures, I used
FESX March 2015 contract, the same one you used in Systematic Trading
pg. 211. The input data file for FESX is at

https://dl.dropboxusercontent.com/u/1570604/tmp/fesx.csv

The output

https://dl.dropboxusercontent.com/u/1570604/tmp/bidask.csv

Sometimes the spread comes out negative, in this case the usual
approach is setting it to 0 (I used Nan). Do these estimates look
reasonable to you? Would monthly average for estimates make sense? My
trading will be in small sizes, vol target < 50,000 Eur.

My email address is skorsky12 %at% gmail.com

Regards,




