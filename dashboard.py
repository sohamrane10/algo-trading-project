import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Secure Configuration ---
st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")

# --- Public Data Fallback (No API Keys Needed) ---
def get_sample_data():
    """Generate sample data if real data fails"""
    dates = pd.date_range(end=datetime.today(), periods=100)
    return pd.DataFrame({
        'Close': np.random.normal(100, 10, 100).cumsum(),
        '20_MA': np.random.normal(100, 5, 100),
        '50_MA': np.random.normal(100, 3, 100),
        'RSI': np.random.uniform(30, 70, 100),
        'Signal': np.random.choice([-1, 0, 1], 100)
    }, index=dates)

# --- Sidebar Controls ---
st.sidebar.header("Parameters")
use_live_data = st.sidebar.toggle("Use Live Data", True)
ticker = st.sidebar.text_input("Stock Ticker", "RELIANCE.NS") if use_live_data else None
period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y"], index=0)

# --- Main Dashboard ---
st.title("Algo Trading Dashboard")
st.write(f"Showing {'live' if use_live_data else 'sample'} data analysis")

def load_data():
    try:
        if use_live_data:
            from data_fetcher import fetch_data
            from strategy import generate_signals
            from backtester import calculate_pnl
            
            data = fetch_data(ticker, period)
            signals = generate_signals(data)
            results = calculate_pnl(signals)
            return data, signals, results
        
        # Fallback to sample data
        data = get_sample_data()
        signals = data.copy()
        signals['Position'] = signals['Signal'].cumsum()
        signals['Daily_PnL'] = signals['Close'].diff() * signals['Position'].shift(1)
        signals['Cumulative_PnL'] = signals['Daily_PnL'].cumsum()
        return data, signals, signals
    
    except Exception as e:
        st.warning(f"⚠️ Error loading live data: {str(e)}")
        st.info("Showing sample data instead")
        data = get_sample_data()
        return data, data, data

# --- Display Data ---
data, signals, results = load_data()

# 1. Price Chart
st.subheader("Price and Indicators")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data.index, data['Close'], label='Price')
if '20_MA' in signals.columns:
    ax.plot(signals.index, signals['20_MA'], label='20 MA')
    ax.plot(signals.index, signals['50_MA'], label='50 MA')

if 'Signal' in signals.columns:
    buy_signals = signals[signals['Signal'] == 1]
    sell_signals = signals[signals['Signal'] == -1]
    ax.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy')
    ax.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell')

ax.legend()
st.pyplot(fig)

# 2. Performance Metrics
st.subheader("Performance Metrics")
col1, col2, col3 = st.columns(3)

if not results.empty:
    valid_trades = results[results['Position'].shift(1) != 0] if 'Position' in results.columns else pd.DataFrame()
    win_rate = (valid_trades[valid_trades['Daily_PnL'] > 0].shape[0] / valid_trades.shape[0]) * 100 if not valid_trades.empty else 0
    total_pnl = results['Cumulative_PnL'].iloc[-1] if 'Cumulative_PnL' in results.columns else 0
    
    col1.metric("Total Trades", len(valid_trades))
    col2.metric("Win Rate", f"{win_rate:.1f}%")
    col3.metric("Total P&L", f"₹{total_pnl:.2f}")

# 3. RSI Indicator
if 'RSI' in signals.columns:
    st.subheader("RSI Indicator")
    st.line_chart(signals['RSI'])

# 4. Raw Data
st.subheader("Recent Signals")
st.dataframe(signals[['Close', '20_MA', '50_MA', 'RSI', 'Signal']].tail() if all(col in signals.columns for col in ['Close', '20_MA', '50_MA', 'RSI', 'Signal']) 
      else signals.tail(), use_container_width=True)

# --- Deployment Guide ---
st.sidebar.markdown("""
### Deployment Options
1. **Streamlit Sharing**:  
   - Just upload this file to [share.streamlit.io](https://share.streamlit.io/)
2. **Public Google Sheet**:  
   - Make your Sheet public and use iframe
3. **Local Run**:  
   ```bash
   streamlit run dashboard.py
