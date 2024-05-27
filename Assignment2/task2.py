import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


stock_ticker = 'AAPL'  
stock_data = yf.download(stock_ticker, start='2015-01-01', end='2024-05-25')['Adj Close']


def monte_carlo_simulation(S0, mu, sigma, T, dt, n_simulations):
    n_steps = int(T / dt)
    price_paths = np.zeros((n_steps + 1, n_simulations))
    price_paths[0] = S0

    for t in range(1, n_steps + 1):
        Z = np.random.standard_normal(n_simulations)
        price_paths[t] = price_paths[t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)
    
    return price_paths





S0 = stock_data[-1]
mu = stock_data.pct_change().mean() * 252
sigma = stock_data.pct_change().std() * np.sqrt(252)
T = 1.0  
dt = 1/252  
n_simulations = 1000

simulated_prices = monte_carlo_simulation(S0, mu, sigma, T, dt, n_simulations)





plt.figure(figsize=(12, 6))
plt.plot(stock_data.index, stock_data, label='Historical Stock Price', color='red')
for i in range(10): 
    plt.plot(pd.date_range(stock_data.index[-1], periods=int(T / dt) + 1, freq='D'), simulated_prices[:, i], linestyle='--', color='blue', alpha=0.4)
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('Historical vs Simulated Stock Price Paths')
plt.legend()
plt.show()
