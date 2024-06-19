import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_volatility(data):
    returns = np.log(data['Close'] / data['Close'].shift(1))
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
    return volatility, returns

def set_stop_loss(current_price, volatility, risk_tolerance):
    stop_loss = current_price * (1 - (volatility * risk_tolerance))
    return stop_loss

def get_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    return data

def main():
    symbols = input("Enter stock symbols (comma separated): ").split(',')
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    risk_tolerance = float(input("Enter your risk tolerance: "))
    
    for symbol in symbols:
        symbol = symbol.strip()
        data = get_stock_data(symbol, start_date, end_date)
        if data.empty:
            print(f"No data found for {symbol}")
            continue

        volatility, returns = calculate_volatility(data)
        current_price = data['Close'].iloc[-1]        
        stop_loss = set_stop_loss(current_price, volatility, risk_tolerance)        
        print(f"\nStock: {symbol}")
        print(f"Current Price: {current_price:.2f}")
        print(f"Annualized Volatility: {volatility:.2%}")
        print(f"Stop-Loss Level: {stop_loss:.2f}")
        plt.figure(figsize=(10, 6))
        plt.plot(data['Close'], label='Stock Price')
        plt.axhline(y=stop_loss, color='r', linestyle='--', label='Stop-Loss Level')
        plt.title(f'{symbol} Price and Stop-Loss Level')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main()
