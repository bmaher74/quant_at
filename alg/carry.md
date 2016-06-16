The carry rule

EWMAC is a positive skew rule which needs prices to trend in one
direction or another.  Carry, which is sometimes called roll down or
contango, is the return that you will get if asset prices are
perfectly stable. If the world doesn’t change this will be equal to
the yield on the asset, less the cost of borrowing (or the interest
you would have got from holding cash). So if you buy shares in French
supermarket Carrefour which currently has a dividend yield of 3%, and
you pay 1% to borrow the purchase cost, then you earn 2% carry on the
position if the share price is unchanged.

Similarly today I can buy June 2018 Eurodollar futures at 97.94, or
March 2018 at 98.01. If there is no change in the shape of the yield
curve then in three months’ time June futures will rise to 98.01,
earning 0.07 per contract.  Academic theory predicts that prices
should move against us to offset these returns, but it often
doesn’t. Carry is usually earned steadily on these kinds of trades
although occasionally they go horribly wrong and the relationship
temporarily breaks down, giving this trading rule some evil negative
skew. I think the rule is profitable as a reward for taking on this
nasty skew and various other kinds of risk premium which tend to be
correlated to carry trades.

Full details on how I calculate carry are given in appendix B, from
page 297 onwards. There is an example of the carry trading rule in
action in figure 19, again showing crude oil futures during the great
crash of 2008. The price of the nearer futures contract dips below the
contract we are trading in mid-August.  This is a bearish carry signal
and the rule sells to enjoy some of the continuing fall in price.

Unfortunately it remains bearish long after the market has turned, but
you can’t win them all. It makes sense to combine diversifying trading
rules like the positive skew, trend following EWMAC rule, with a
negative skew carry rule.

Futures: If not trading nearest contract (preferred)
Current contract price The price of the contract you are trading.
Nearer contract price The price of the next closest contract. So if you are trading June 2017 Eurodollar it would be March 2017.
Price differential Current contract price minus nearer contract price.
Distance between contracts The time in years between the two contracts (current and nearer). For adjacent quarterly expiries it is 0.25 and for monthly 0.083.
Net expected return in price units  You need to annualise the price differential by dividing by the distance between contracts.

Futures: If trading nearest contract (approximation)
Current contract price The price of the contract you are trading.
Next contract price The price of the contract with the next expiry. So if you had June 2017 Treasury bonds it would be September 2017.
Price differential Next contract price minus current contract price.
Distance between contracts The time in years between the two contracts (current and next). For adjacent quarterly expiries it would be 0.25, for monthly 0.083 and so on.
Net expected return in price units You need to annualise the price differential by dividing by the distance between contracts.

Forecast calculation
Net expected return in price units  From relevant information above. Note this is an annualised measure.
Standard deviation of returns This is the standard deviation of returns in price points, not percentage  points as normal. The volatility in price points is equal to the percentage  point volatility (price volatility as defined in chapter ten, ‘Position sizing’, on page 165), multiplied by the current price.
Annualised standard deviation of returns Multiply the standard deviation of returns by the ‘square root of time’ to annualise it. Assuming 256 business days in a year you should multiply by 16. 
Raw carry: Volatility standardised expected As I pointed out in chapter seven, you want forecasts to be adjusted for return standard deviation. So this is the net expected return in price units divided by the annualised standard deviation of returns.
Forecast scalar: The forecast scalar is 30. I explain below where the multiplier comes from.
Forecast: The forecast will be the forecast scalar times the raw carry.
Capped forecast This is the forecast with values outside the range -20, +20 capped.
 
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
 
 

