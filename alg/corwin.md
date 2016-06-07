					


```python
df = pd.read_csv('20day.csv',sep='\s*')
df['Lt1'] = df.Lt.shift(-1)
df['Ht1'] = df.Ht.shift(-1)

def f(x):
    beta = np.log(x.Ht/x.Lt)**2 + np.log(x.Ht1/x.Lt1)**2
    gamma = np.log( max(x.Ht,x.Ht1) / min(x.Lt,x.Lt1)  )**2
    alpha1 = (np.sqrt(2*beta)-np.sqrt(beta)) / (3 - 2*np.sqrt(2))
    alpha2 = np.sqrt(gamma / (3-2*np.sqrt(2)))
    alpha = alpha1 - alpha2
    S = 2*(np.exp(alpha)-1) / (1 + np.exp(alpha))
    return S

df['S'] = df.apply(f, axis=1)
df = df.fillna(0)
df.loc[df.S<0,'S'] = 0

print df.head()
```

```text
   Close     Lt     Ht    Lt1    Ht1         S
0  25.25  25.25  25.32  25.19  25.32  0.001683
1  25.32  25.19  25.32  25.28  25.41  0.000000
2  25.30  25.28  25.41  25.28  25.38  0.003243
3  25.33  25.28  25.38  25.27  25.37  0.002995
4  25.33  25.27  25.37  25.36  25.45  0.000000
```
























