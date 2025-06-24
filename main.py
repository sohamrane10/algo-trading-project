from data_fetcher import fetch_data
from strategy import generate_signals
from backtester import calculate_pnl
from gsheets import log_to_gsheet
from ml_model import train_model

def main():
    try:
        print("Starting algo trading system...")
        
        # 1. Data Collection
        print("\nFetching data...")
        data = fetch_data("RELIANCE.NS")
        print("Columns available:", data.columns.tolist())
        
        # 2. Generate Signals
        print("\nGenerating trading signals...")
        signals = generate_signals(data)
        
        # 3. Backtest
        print("\nRunning backtest...")
        results = calculate_pnl(signals)
        print(results[['Close', 'Signal', 'Position', 'Cumulative_PnL']].tail())
        
        # 4. Google Sheets Logging
        print("\nLogging to Google Sheets...")
        log_to_gsheet(results, "credentials.json", "AlgoTradingLogs")
        
        # 5. ML Model (Optional)
        print("\nTraining ML model...")
        if len(data) > 100:  # Only run if sufficient data
            try:
                train_model(data)
            except Exception as e:
                print(f"ML model skipped: {str(e)}")
        
        print("\nAll tasks completed successfully!")
        
    except Exception as e:
        print(f"\nSystem error: {str(e)}")
        print("Check your data and API connections.")

if __name__ == "__main__":
    main()