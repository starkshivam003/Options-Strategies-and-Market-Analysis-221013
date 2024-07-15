import pandas as pd
import numpy as np

def construct_diversified_portfolio(price_data):
    returns = price_data.pct_change().dropna()
    correlation_matrix = returns.corr()
    
    def get_least_correlated_assets(correlation_matrix, num_assets):
        selected_assets = []
        avg_correlations = correlation_matrix.mean(axis=1)
        
        for _ in range(num_assets):
            remaining_assets = correlation_matrix.index.difference(selected_assets)
            if not remaining_assets.any():
                break
            
            min_avg_corr_asset = avg_correlations[remaining_assets].idxmin()
            selected_assets.append(min_avg_corr_asset)
            
            correlation_matrix = correlation_matrix.drop(min_avg_corr_asset).drop(min_avg_corr_asset, axis=1)
        
        return selected_assets
    
    num_assets = 5  
    
    selected_assets = get_least_correlated_assets(correlation_matrix, num_assets)
    
    return selected_assets

if __name__ == "__main__":
    data = {
        'Asset_A': [10, 11, 12, 13, 14],
        'Asset_B': [20, 22, 24, 26, 28],
        'Asset_C': [30, 27, 25, 22, 29],
        'Asset_D': [40, 45, 41, 45, 42],
        'Asset_E': [50, 56, 51, 55, 52],
        'Asset_F': [60, 65, 61, 66, 62]
    }
    
    price_data = pd.DataFrame(data)
    diversified_portfolio = construct_diversified_portfolio(price_data)
    
    print("Selected assets for diversified portfolio:")
    print(diversified_portfolio)
