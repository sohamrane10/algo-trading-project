import gspread
from oauth2client.service_account import ServiceAccountCredentials

def log_to_gsheet(data, json_keyfile, sheet_name):
    """Log data to Google Sheets"""
    scope = ["https://spreadsheets.google.com/feeds", 
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    
    # Convert DataFrame to list of lists
    values = [data.columns.tolist()] + data.fillna('').values.tolist()
    sheet.update('A1', values)

if __name__ == "__main__":
    from strategy import generate_signals
    from data_fetcher import fetch_data
    from backtester import calculate_pnl
    
    print("Fetching data...")
    data = fetch_data("RELIANCE.NS")
    
    print("Generating signals...")
    signals = generate_signals(data)
    
    print("Calculating P&L...")
    results = calculate_pnl(signals)
    
    print("Logging to Google Sheets...")
    log_to_gsheet(
        results[['Close', 'Signal', 'Cumulative_PnL']].tail(20),
        "credentials.json",
        "AlgoTradingLogs"
    )
    print("Successfully updated Google Sheets!")