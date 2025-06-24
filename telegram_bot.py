from telegram import Bot
import time
from strategy import generate_signals
from data_fetcher import fetch_data

def send_alert(message, token, chat_id):
    """Send message to Telegram"""
    try:
        bot = Bot(token=token)
        bot.send_message(chat_id=chat_id, text=message)
        print("Alert sent successfully!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def monitor_signals(token, chat_id, ticker="RELIANCE.NS"):
    """Check for trading signals and send alerts"""
    while True:
        try:
            data = fetch_data(ticker)
            signals = generate_signals(data)
            latest_signal = signals.iloc[-1]['Signal']
            
            if latest_signal == 1:
                send_alert("🚀 BUY Signal Generated!", token, chat_id)
            elif latest_signal == -1:
                send_alert("🔻 SELL Signal Generated!", token, chat_id)
                
            # Check every hour (adjust as needed)
            time.sleep(3600)
            
        except Exception as e:
            print(f"Error in monitoring: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    # Replace these with your actual credentials
    TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"  # From @BotFather
    CHAT_ID = "YOUR_CHAT_ID"  # Get from @userinfobot
    
    print("Starting Telegram monitoring...")
    monitor_signals(TELEGRAM_TOKEN, CHAT_ID)