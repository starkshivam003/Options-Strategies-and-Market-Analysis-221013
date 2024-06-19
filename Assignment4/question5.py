def protective_put_cost(stock_price, strike_price, put_premium):
    total_cost = stock_price + put_premium    
    return total_cost

stock_price = float(input("Enter current stock price: "))
strike_price = float(input("Enter strike price of the put option: "))
put_premium = float(input("Enter premium paid for the put option: "))

total_cost = protective_put_cost(stock_price, strike_price, put_premium)
print(f"Total cost of setting protective put strategy = ${total_cost:.2f}")
