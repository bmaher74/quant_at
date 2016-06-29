
```python
import sys; sys.path.append('../data')
import futures
res = futures.get_contract(market="CME", sym="CL", month="Q", year=2008, db="findb")
print res
```

```text
          _id       h       l  la       o      oi       s       v
0    20060210   65.76   65.76 NaN   65.76       0   65.76       0
1    20060213   65.59   65.59 NaN   65.59       0   65.59       0
2    20060214   64.77   64.77 NaN   64.77       0   64.77       0
3    20060215   63.62   63.62 NaN   63.62       0   63.62       0
4    20060216   64.49   64.49 NaN   64.49       0   64.49       0
5    20060217   65.37   65.37 NaN   65.37       0   65.37       0
6    20060221   66.44   66.44 NaN   66.44       0   66.44       0
7    20060222   65.94   65.94 NaN   65.94       0   65.94       0
8    20060223   66.46   66.46 NaN   66.46       0   66.46       0
9    20060224   67.66   67.66 NaN   67.66       0   67.66       0
10   20060227   66.60   66.60 NaN   66.60       0   66.60       0
11   20060228   67.25   67.25 NaN   67.25       0   67.25       0
12   20060301   67.70   67.70 NaN   67.70       0   67.70       0
13   20060302   68.70   68.70 NaN   68.70       0   68.70       0
14   20060303   68.82   68.82 NaN   68.82       0   68.82       0
15   20060306   67.40   67.40 NaN   67.40       0   67.40       0
16   20060307   66.13   66.13 NaN   66.13       0   66.13       0
17   20060308   65.09   65.09 NaN   65.09       0   65.09       0
18   20060309   65.81   65.81 NaN   65.81       0   65.81       0
19   20060310   65.13   65.13 NaN   65.13       0   65.13       0
20   20060313   66.75   66.75 NaN   66.75       0   66.75       0
21   20060314   68.07   68.07 NaN   68.07       0   68.07       0
22   20060315   66.43   66.43 NaN   66.43       0   66.43       0
23   20060316   67.63   67.63 NaN   67.63       0   67.63       0
24   20060317   66.58   66.58 NaN   66.58       0   66.58       0
25   20060320   65.21   65.21 NaN   65.21       0   65.21       0
26   20060321   66.09   66.09 NaN   66.09       0   66.09       0
27   20060322   65.45   65.45 NaN   65.45       0   65.45       0
28   20060323   66.61   66.61 NaN   66.61       0   66.61       0
29   20060324   66.37   66.37 NaN   66.37     300   66.37     300
..        ...     ...     ...  ..     ...     ...     ...     ...
587  20080611  138.85  131.91 NaN  132.35  246353  136.98  147040
588  20080612  138.09  132.25 NaN  137.17  263540  137.38  172681
589  20080613  137.62  134.12 NaN  137.51  272396  135.47  117819
590  20080616  140.42  133.57 NaN  135.08  270338  135.34  147755
591  20080617  135.91  132.67 NaN  134.47  277677  134.53  162789
592  20080618  137.34  132.41 NaN  134.00  300349  137.17  215757
593  20080619  138.36  132.09 NaN  138.00  315706  132.60  359406
594  20080620  137.50  131.75 NaN  132.41  321220  135.36  278598
595  20080623  138.14  134.05 NaN  134.80  326883  136.74  248739
596  20080624  138.75  135.90 NaN  137.25  319370  137.00  229371
597  20080625  137.58  131.95 NaN  137.07  317089  134.55  290400
598  20080626  140.39  133.68 NaN  134.52  310154  139.64  295773
599  20080627  142.99  138.61 NaN  139.44  313090  140.21  277517
600  20080630  143.67  139.17 NaN  140.60  289851  140.00  253428
601  20080701  143.33  139.95 NaN  140.18  288297  140.97  238751
602  20080702  144.32  140.01 NaN  141.44  279194  143.57  253397
603  20080703  145.85  143.22 NaN  144.19  280318  145.29  193841
604  20080707  144.53  139.50 NaN  144.27  285538  141.37  304148
605  20080708  142.44  135.14 NaN  141.59  246200  136.04  382404
606  20080709  138.28  135.34 NaN  136.00  223504  136.05  299142
607  20080710  142.13  135.43 NaN  135.80  208358  141.65  294339
608  20080711  147.27  141.44 NaN  141.80  203878  145.08  334940
609  20080714  146.37  142.49 NaN  144.69  154516  145.18  252605
610  20080715  146.73  135.92 NaN  145.19  146402  138.74  392225
611  20080716  139.30  132.00 NaN  138.77  109902  134.60  293858
612  20080717  136.75  129.00 NaN  135.11   80629  129.29  379076
613  20080718  132.04  128.23 NaN  129.56   63111  128.88  208698
614  20080721  132.05  128.63 NaN  128.88   23594  131.04  133661
615  20080722  132.07  125.63 NaN  131.04   23594  127.95  133661
616  20080723  128.60  126.90 NaN  127.05   23594  126.90  133661

[617 rows x 8 columns]
```




The carry rule

EWMAC is a positive skew rule which needs prices to trend in one
direction or another.

There is an example of the carry trading rule in action in figure 19,
again showing crude oil futures during the great crash of 2008. The
price of the nearer futures contract dips below the contract we are
trading in mid-August.  This is a bearish carry signal and the rule
sells to enjoy some of the continuing fall in price.

Unfortunately it remains bearish long after the market has turned, but
you can’t win them all. It makes sense to combine diversifying trading
rules like the positive skew, trend following EWMAC rule, with a
negative skew carry rule.

* Futures: If not trading nearest contract (preferred)

Current contract price: The price of the contract you are trading.

Nearer contract price: The price of the next closest contract. So if
you are trading June 2017 Eurodollar it would be March 2017.

Price differential Current contract price minus nearer contract price.

Distance between contracts: The time in years between the two contracts
(current and nearer). For adjacent quarterly expiries it is 0.25 and
for monthly 0.083.

Net expected return in price units: You need to annualise the price
differential by dividing by the distance between contracts.

* Futures: If trading nearest contract (approximation)

Current contract price: The price of the contract you are trading.

Next contract price: The price of the contract with the next expiry. So
if you had June 2017 Treasury bonds it would be September 2017.

Price differential: Next contract price minus current contract price.

Distance between contracts: The time in years between the two contracts
(current and next). For adjacent quarterly expiries it would be 0.25,
for monthly 0.083 and so on.

Net expected return in price units: You need to annualise the price
differential by dividing by the distance between contracts.

* Forecast calculation

Net expected return in price units: From relevant information
above. Note this is an annualised measure.

Standard deviation of returns: This is the standard deviation of
returns in price points, not percentage points as normal. The
volatility in price points is equal to the percentage point volatility
(price volatility as defined in chapter ten, ‘Position sizing’, on
page 165), multiplied by the current price.

Annualised standard deviation of returns: Multiply the standard
deviation of returns by the ‘square root of time’ to annualise
it. Assuming 256 business days in a year you should multiply by 16.

Raw carry: Volatility standardised expected As I pointed out in
chapter seven, you want forecasts to be adjusted for return standard
deviation. So this is the net expected return in price units divided
by the annualised standard deviation of returns.

Forecast scalar: The forecast scalar is 30. I explain below where the
multiplier comes from.

Forecast: The forecast will be the forecast scalar times the raw
carry.

Capped forecast This is the forecast with values outside the range
-20, +20 capped.
 
Which forecast scalar to use?
The raw carry measure is effectively an annualised Sharpe ratio (SR),
an expected return divided by standard deviation. I used the technique
in appendix D and data from a large number of markets across different
asset classes to work out the right forecast scalar. This gives a
forecast scalar of around 30.

What is the turnover of carry?
It’s hard to generalise about the turnover (round trips per year) of
carry since it depends on the asset class and how often you update the
value of the forecast. I suggest checking the forecast weekly to avoid
spurious noise which can otherwise be a problem. If you do this then
it is reasonable to use a rule of thumb value of 10 for the turnover
of the carry rule.
 
 

