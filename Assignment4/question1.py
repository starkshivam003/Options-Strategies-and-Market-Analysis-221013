import yfinance as yf
import pandas as pd
import numpy as np

def get_option_chain(ticker, expiration_date):
    stock = yf.Ticker(ticker)
    options = stock.option_chain(expiration_date)
    calls = options.calls
    puts = options.puts
    return calls, puts

def calculate_max_pain(calls, puts):
    strikes = sorted(set(calls['strike']).union(set(puts['strike'])))
    max_pain = None
    min_pain = float('inf')
    
    for strike in strikes:
        call_oi = calls.loc[calls['strike'] == strike, 'openInterest'].sum()
        put_oi = puts.loc[puts['strike'] == strike, 'openInterest'].sum()
        total_oi = call_oi + put_oi
        if total_oi < min_pain:
            min_pain = total_oi
            max_pain = strike
            
    return max_pain

ticker = 'AAPL'
expiration_date = '2024-06-28'  
calls, puts = get_option_chain(ticker, expiration_date)
max_pain_strike = calculate_max_pain(calls, puts)
print(f"Max Pain strike price = {max_pain_strike}")


