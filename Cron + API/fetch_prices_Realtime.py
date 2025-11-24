import pandas as pd
import yfinance as yf
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

# MySQL configuration
# REMINDER: Mask your password before pushing to GitHub!
DB_CONFIG = {
   "host":"localhost",
   "user":"exampleuser",
   "password":"examplepassword",
   "database": "stockdb"

}

# Check if CSV exists
if not os.path.exists("omxh25_companies.csv"):
    print("Error: omxh25_companies.csv not found")
    exit()

# Read tickers from CSV
companies = pd.read_csv("omxh25_companies.csv")
tickers = companies['symbol'].tolist()

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    current_time = datetime.now()
    print(f"Task started: {current_time}")

    success_count = 0

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            # Fetch latest data
            hist = stock.history(period="1d")

            if not hist.empty:
                r = hist.iloc[-1]

                # SQL query
                sql = """INSERT INTO stock_prices (symbol, date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

                # Data tuple
                val = (ticker, current_time, float(r['Open']), float(r['High']), float(r['Low']), float(r['Close']), int(r['Volume']))

                cursor.execute(sql, val)
                print(f"OK: {ticker} - {float(r['Close'])}")
                success_count += 1
            else:
                print(f"Warning: No data for {ticker}")

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    conn.commit()
    print(f"Done. Updated {success_count} records.")

except Error as e:
    print(f"Database Error: {e}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()