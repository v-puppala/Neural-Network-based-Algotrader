# Neural-Network-based-Momentum-Algotrader
# Optimizing the future price using machine learning, specifically a regression model
# Multi-layer Perceptron (MLP) is a supervised learning algorithm that learns a function f(.): f^m -> f^n by training on a dataset, where is the number of dimensions for input and s the number of dimensions for output. Given a set of features and a target it can learn a non-linear function approximator for either classification o  regression. 
#https://scikit-learn.org/stable/modules/neural_networks_supervised.htmlhttps://scikit-learn.org/stable/modules/neural_networks_supervised.html
# We chose this approach for a number of three main reasons
# Firstly, by using deep neural networks to directly generate trading signals, we remove the need to manually specify both the trend estimator and position sizing methodology allowing them to be learnt directly using modern time series prediction architectures. 
# Secondly, by utilising automatic differentiation in existing backpropagation frameworks, we explicitly optimise networks for risk-adjusted performance metrics, i.e. the Sharpe ratio [34], improving the risk profile of the signal on the whole. 
# Lastly, retaining a consistent framework with other momentum strategies also allows us to retain desirable attributes from previous works specifically volatility scaling, which plays a critical role in the positive performance of time series momentum strategies [9]. This consistency also helps when making comparisons to existing methods, and facilitates the interpretation of different components of the overall signal by practitioners.
# why we chose SPY low risk product: is the oldest traded ETF, with 84.5 million shares traded daily and avaerage returns of -15.53%,	9.09%,	11.56% over 1yr,5yr and 10 yrs respectively. SPY is sector agnostic and spans across 10 sector, reducing  the following: liquidity risk, geopolitical risk, sector risk, concentration risk ( the client will hard have any impact on the price ) which improves execution and reduces chances of spread cross and slippage.
https://finance.yahoo.com/quote/SPY/holdings/
https://en.wikipedia.org/wiki/SPDR_S%26P_500_Trust_ETF
# Why we chose APPL meduim level: One of the best performing stock over the past decade 200% return over the past 5 yrs despite this impressive performance the client is still exposed to sector risk and concentration risk
https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch
# why we chose EAST: it is a penny stock and it is exposed to all the reisk mitiagted for  by SPY with a huge potentialon the upside and a petential for the investor to be wiped out
# We recognize that the client will not be protected against market risk since this product is direction and not hedged



#Code
