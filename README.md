# Neural-Network-based-Momentum-Algotrader
# Optimizing the future price and size traded using machine learning, specifically a regression model
# this work builds on the workof Balttas and Kosowski 2017
# We chose this approach for a number of three main reasons
# Firstly, by using deep neural networks to directly generate trading signals, we remove the need to manually specify both the trend estimator and position sizing methodology allowing them to be learnt directly using modern time series prediction architectures. 
# Secondly, by utilising automatic differentiation in existing backpropagation frameworks, we explicitly optimise networks for risk-adjusted performance metrics, i.e. the Sharpe ratio [34], improving the risk profile of the signal on the whole. 
# Lastly, retaining a consistent framework with other momentum strategies also allows us to retain desirable attributes from previous works specifically volatility scaling, which plays a critical role in the positive performance of time series momentum strategies [9]. This consistency also helps when making comparisons to existing methods, and facilitates the interpretation of different components of the overall signal by practitioners.
