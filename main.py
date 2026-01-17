import yfinance as yf
import schedule
import time
import sys

from config import STOCK_SYMBOL, TARGET_PRICE, CHECK_INTERVAL
from email_alert import send_email_alert

print("main.py started successfully")   # DEBUG LINE

email_sent = False


def get_current_price():
    try:
        stock = yf.Ticker(STOCK_SYMBOL)
        data = stock.history(period="1d")

        if data.empty:
            print("No data received from Yahoo Finance")
            return None

        price = data['Close'].iloc[-1]
        return round(price, 2)

    except Exception as e:
        print("Error fetching stock price:", e)
        return None


def check_stock_price():
    global email_sent

    print("Checking stock price...")   # DEBUG LINE

    current_price = get_current_price()

    if current_price is None:
        print("Price not available. Retrying...")
        return

    print(f"{STOCK_SYMBOL} Current Price: ${current_price}")

    if current_price >= TARGET_PRICE and not email_sent:
        print("Target reached! Sending email...")
        send_email_alert(STOCK_SYMBOL, current_price, TARGET_PRICE)
        email_sent = True
    elif email_sent:
        print("Alert already sent. Monitoring continues...")


# Run once immediately (IMPORTANT)
check_stock_price()

# Scheduler
schedule.every(CHECK_INTERVAL).minutes.do(check_stock_price)

print("Real-Time Stock Price Tracker is running...")
print(f"Monitoring {STOCK_SYMBOL} | Target: ${TARGET_PRICE}")

while True:
    schedule.run_pending()
    time.sleep(1)