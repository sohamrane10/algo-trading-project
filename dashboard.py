import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import fetch_data
from strategy import generate_signals
from backtester import calculate_pnl

# Page configuration
st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")

# Sidebar controls
st.sidebar.header("Parameters")
ticker = st.sidebar.text_input("Stock Ticker", "RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y"], index=0)

# Main dashboard
st.title("Algo Trading Dashboard")
st.write(f"Showing analysis for {ticker} ({period})")

@st.cache_data
def load_data(ticker, period):
    data = fetch_data(ticker, period)
    signals = generate_signals(data)
    results = calculate_pnl(signals)
    return data, signals, results

try:
    # Load data with progress indicator
    with st.spinner("Loading data..."):
        data, signals, results = load_data(ticker, period)
    
    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(data.tail(), use_container_width=True)
    
    # Plot prices and indicators
    st.subheader("Price and Indicators")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Price')
    ax.plot(signals.index, signals['20_MA'], label='20 MA')
    ax.plot(signals.index, signals['50_MA'], label='50 MA')
    
    # Plot buy/sell signals
    buy_signals = signals[signals['Signal'] == 1]
    sell_signals = signals[signals['Signal'] == -1]
    ax.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy')
    ax.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell')
    
    ax.legend()
    st.pyplot(fig)
    
    # Performance metrics
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    
    if not results.empty:
        valid_trades = results[results['Position'].shift(1) != 0]
        win_rate = (valid_trades[valid_trades['Daily_PnL'] > 0].shape[0] / valid_trades.shape[0]) * 100
        total_pnl = results['Cumulative_PnL'].iloc[-1]
        
        col1.metric("Total Trades", len(valid_trades))
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Total P&L", f"₹{total_pnl:.2f}")
    
    # Show RSI
    st.subheader("RSI Indicator")
    st.line_chart(signals['RSI'])
    
    # Show raw signals
    st.subheader("Trading Signals")
    st.dataframe(signals[['Close', '20_MA', '50_MA', 'RSI', 'Signal']].tail(), use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")