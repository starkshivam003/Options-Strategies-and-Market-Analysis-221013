def butterfly_spread_profit_loss(K1, K2, K3, premium_K1, premium_K2, premium_K3):
    net_premium_received = premium_K2 - premium_K1 - premium_K3
    max_loss = (K2 - K1) - net_premium_received
    profit_loss = net_premium_received - max_loss
    return profit_loss

def main():
    try:
        K1 = float(input("Enter lower strike price (K1): "))
        K2 = float(input("Enter middle strike price (K2): "))
        K3 = float(input("Enter higher strike price (K3): "))
        premium_K1 = float(input(f"Enter premium paid for buying K1 call: "))
        premium_K2 = float(input(f"Enter premium received for selling K2 calls: "))
        premium_K3 = float(input(f"Enter premium paid for buying K3 call: "))
        
        result = butterfly_spread_profit_loss(K1, K2, K3, premium_K1, premium_K2, premium_K3)
        print(f"Potential profit/loss of butterfly spread: {result}")
    
    except ValueError:
        print("Error: Enter valid numeric values for strike prices and premiums.")

if __name__ == "__main__":
    main()
