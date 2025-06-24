import pandas as pd
import numpy as np

def calculate_rsi(data, window=14):
    """Manual RSI calculation"""
    close_prices = data['Close'].values if isinstance(data['Close'], pd.DataFrame) else data['Close']
    delta = np.diff(close_prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = pd.Series(gain).rolling(window).mean()
    avg_loss = pd.Series(loss).rolling(window).mean()
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def generate_signals(data):
    """Generate trading signals"""
    # Simplify DataFrame structure if needed
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    data = data.copy()
    
    # Calculate indicators
    data['20_MA'] = data['Close'].rolling(20).mean()
    data['50_MA'] = data['Close'].rolling(50).mean()
    data['RSI'] = calculate_rsi(data)
    
    # Initialize signals
    data['Signal'] = 0
    
    # Buy signal conditions
    ma_cross = (data['20_MA'] > data['50_MA']) & (data['20_MA'].shift(1) <= data['50_MA'].shift(1))
    rsi_condition = (data['RSI'] < 30)
    data.loc[ma_cross & rsi_condition, 'Signal'] = 1  # Buy
    
    # Sell signal condition
    data.loc[data['RSI'] > 70, 'Signal'] = -1  # Sell
    
    return data