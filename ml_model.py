import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def calculate_rsi(data, window=14):
    """Manual RSI calculation"""
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def prepare_features(data):
    """Create features for ML model"""
    data = data.copy()
    
    # Calculate technical indicators
    data['Returns'] = data['Close'].pct_change()
    data['RSI'] = calculate_rsi(data)
    data['MA_20'] = data['Close'].rolling(20).mean()
    data['MA_50'] = data['Close'].rolling(50).mean()
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    
    return data.dropna()

def train_model(data):
    """Train and evaluate ML model"""
    ml_data = prepare_features(data)
    
    # Verify we have the required columns
    required_cols = ['RSI', 'MA_20', 'MA_50', 'Returns', 'Target']
    missing = [col for col in required_cols if col not in ml_data.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    X = ml_data[['RSI', 'MA_20', 'MA_50', 'Returns']]
    y = ml_data['Target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.2%}")
    
    return model

if __name__ == "__main__":
    from data_fetcher import fetch_data
    
    print("Testing ML model...")
    data = fetch_data("RELIANCE.NS")
    model = train_model(data)