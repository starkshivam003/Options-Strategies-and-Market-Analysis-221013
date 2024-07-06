# Import necessary libraries
import pandas as pd
import numpy as np

indicators = {
    0: {"name": "Relative Strength Index", "start_date": "2014-03-01", "end_date": "2018-12-01"},
    1: {"name": "EMA", "start_date": "2008-01-20", "end_date": "2010-10-20"},
    2: {"name": "MACD", "start_date": "2019-04-05", "end_date": "2021-11-30"},
    3: {"name": "SMA", "start_date": "2011-02-01", "end_date": "2015-09-25"},
    4: {"name": "Donchian Channel", "start_date": "2019-05-15", "end_date": "2021-12-10"}
}

def load_stock_data():
    dates = pd.date_range(start="2010-01-01", end="2022-01-01", freq="B")
    stock_data = pd.DataFrame(index=dates)
    stock_data["Close"] = np.random.randn(len(dates))
    return stock_data

def calculate_indicators(last_two_digits):
    quotient = last_two_digits
    while quotient >= 5:
        quotient = quotient / 5
    row1 = int(quotient)
    
    remainder = last_two_digits % 5
    row2 = remainder
    
    if row1 == row2:
        if row2 != 0:
            row2 = row1 - 1
        else:
            row2 = row1 + 1
    
    return row1, row2

def backtest_indicators(stock_data, indicator1, indicator2):
    indicator1_name = indicators[indicator1]["name"]
    indicator1_start_date = indicators[indicator1]["start_date"]
    indicator1_end_date = indicators[indicator1]["end_date"]
    
    indicator2_name = indicators[indicator2]["name"]
    indicator2_start_date = indicators[indicator2]["start_date"]
    indicator2_end_date = indicators[indicator2]["end_date"]
    
    print(f"Selected Indicators for backtesting:")
    print(f"Indicator 1: {indicator1_name} ({indicator1_start_date} to {indicator1_end_date})")
    print(f"Indicator 2: {indicator2_name} ({indicator2_start_date} to {indicator2_end_date})")
    
    buy_signals = []
    sell_signals = []
    for i in range(len(stock_data)):
        if i % 10 == 0:
            buy_signals.append(i)
        elif i % 15 == 0:
            sell_signals.append(i)
    
    profitability = len(buy_signals) / (len(buy_signals) + len(sell_signals))
    
    results = {
        "Buy Signals": buy_signals,
        "Sell Signals": sell_signals,
        "Profitability": profitability
    }
    
    return results

if __name__ == "__main__":
    last_two_digits = 13 # Roll No.: 221013
    row1, row2 = calculate_indicators(last_two_digits)
    stock_data = load_stock_data()
    results = backtest_indicators(stock_data, row1, row2)
    
    print("\nBacktest Results:")
    print("Buy Signals:", results["Buy Signals"])
    print("Sell Signals:", results["Sell Signals"])
    print("Profitability:", results["Profitability"])
