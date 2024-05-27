import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import datetime


def get_option_chain(ticker, expiration_date):
    stock = yf.Ticker(ticker)
    options = stock.option_chain(expiration_date)
    return options


def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price


ticker = 'AAPL'
expiration_date = '2024-05-31'  
options = get_option_chain(ticker, expiration_date)


call_options = options.calls
put_options = options.puts


stock_price = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
risk_free_rate = 0.05  


today = datetime.date.today()
expiration = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()
days_to_expiration = (expiration - today).days
T = days_to_expiration / 365


def categorize_options(options, stock_price):
    itm = options[options['strike'] < stock_price]
    otm = options[options['strike'] > stock_price]
    atm = options.iloc[(options['strike'] - stock_price).abs().argsort()[:1]]
    return itm, otm, atm


itm_calls, otm_calls, atm_calls = categorize_options(call_options, stock_price)
itm_puts, otm_puts, atm_puts = categorize_options(put_options, stock_price)




def assess_options(options, stock_price, T, risk_free_rate):
    assessments = []
    for _, option in options.iterrows():
        strike = option['strike']
        market_price = option['lastPrice']
        implied_vol = option['impliedVolatility']
        if option['contractSymbol'].endswith('C'):
            bsm_price = black_scholes_call(stock_price, strike, T, risk_free_rate, implied_vol)
        else:
            bsm_price = black_scholes_put(stock_price, strike, T, risk_free_rate, implied_vol)
        is_overpriced = market_price > bsm_price
        assessments.append({
            'Strike': strike,
            'Market Price': market_price,
            'BSM Price': bsm_price,
            'Overpriced': is_overpriced
        })
    return pd.DataFrame(assessments)


itm_calls_assessment = assess_options(itm_calls, stock_price, T, risk_free_rate)
otm_calls_assessment = assess_options(otm_calls, stock_price, T, risk_free_rate)
atm_calls_assessment = assess_options(atm_calls, stock_price, T, risk_free_rate)

itm_puts_assessment = assess_options(itm_puts, stock_price, T, risk_free_rate)
otm_puts_assessment = assess_options(otm_puts, stock_price, T, risk_free_rate)
atm_puts_assessment = assess_options(atm_puts, stock_price, T, risk_free_rate)



assessments = pd.concat([
    itm_calls_assessment, otm_calls_assessment, atm_calls_assessment,
    itm_puts_assessment, otm_puts_assessment, atm_puts_assessment
], keys=['ITM Calls', 'OTM Calls', 'ATM Calls', 'ITM Puts', 'OTM Puts', 'ATM Puts'])

print(assessments)
