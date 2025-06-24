import pandas as pd

def calculate_pnl(signals):
    """Calculate Profit & Loss for each trade"""
    signals = signals.copy()
    
    # Ensure we have a simple DataFrame structure
    if isinstance(signals.columns, pd.MultiIndex):
        signals.columns = signals.columns.droplevel(1)
    
    # Convert to numeric if needed
    signals['Close'] = pd.to_numeric(signals['Close'])
    
    # Calculate position (cumulative sum of signals)
    signals['Position'] = signals['Signal'].cumsum()
    
    # Calculate PnL (price change * previous position)
    signals['Daily_PnL'] = signals['Close'].diff() * signals['Position'].shift(1)
    
    # Calculate cumulative PnL
    signals['Cumulative_PnL'] = signals['Daily_PnL'].cumsum().fillna(0)
    
    return signals

if __name__ == "__main__":
    from strategy import generate_signals
    from data_fetcher import fetch_data
    
    print("Fetching data...")
    data = fetch_data("RELIANCE.NS")
    
    print("\nGenerating signals...")
    signals = generate_signals(data)
    
    print("\nCalculating P&L...")
    results = calculate_pnl(signals)
    
    print("\nBacktest Results:")
    print(results[['Close', 'Signal', 'Position', 'Daily_PnL', 'Cumulative_PnL']].tail(10))
    
    if not results.empty:
        valid_trades = results[results['Position'].shift(1) != 0]
        if not valid_trades.empty:
            win_rate = (valid_trades[valid_trades['Daily_PnL'] > 0].shape[0] / valid_trades.shape[0]) * 100
            print(f"\nWin Rate: {win_rate:.2f}%")
    
    results.to_csv("backtest_results.csv")
    print("\nResults saved to 'backtest_results.csv'")