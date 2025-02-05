# Import necessary libraries
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
import sys
import time
from tabulate import tabulate

# ANSI color codes for better output
class Colors:
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

# Check if a given ticker symbol is valid
def check_valid_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        if hist.empty:
            return False
        return True
    except Exception as e:
        print(f"Error checking ticker {ticker}: {e}")
        return False
    
# Check if moving average target is positive
# Currently this is defined in its own method in case
# of future improvements.
def check_valid_target(ma_target):
    try:
        ma_target = float(ma_target)
        return ma_target >= 0
    except ValueError:
        return False

# Retrieves stock data over a specified time
def get_stock_data(ticker, days=300):
    return yf.download(ticker, period=f'{days}d', progress=False)

# Calculates moving average
def calculate_moving_averages(data, window):
    return data['Close'].rolling(window=window).mean()

# Predicts when a moving average will hit the target
def predict_ma_hit(data, ma_window, ma_target):
    ma = calculate_moving_averages(data, ma_window)
    ma_recent = ma.dropna().values  # Drop NaNs for regression
    
    if len(ma_recent) < 10:  # Ensure enough data points
        return None, "Not enough data for a reliable prediction."
    
    x = np.arange(len(ma_recent)).reshape(-1, 1)  # Days as features
    y = ma_recent

    # Train linear regression to predict MA trend
    model = LinearRegression()
    model.fit(x, y)

    # Avoid division by zero (flat moving average)
    if abs(model.coef_[0][0]) < 1e-5:
        return None, "No significant trend detected, unable to predict crossover."
    
    # Extract scalars
    intercept = model.intercept_[0]
    coef = model.coef_[0][0]

    # Predict when MA hits target
    days_needed = (ma_target - intercept) / coef

    if days_needed < 0:
        return None, f"The 150-day moving average has already been below ${ma_target:.2f}. Consider adjusting your target."

    return round(days_needed, 2), None

# Handle incorrect number of command line arguments
if len(sys.argv) < 3:
    print(f"{Colors.RED}Error: Missing arguments!{Colors.RESET}")
    print("Usage: python3 prediction.py <ticker> <target_moving_average>")
    exit(1)

# Validate this format: python3 ticker_symbol ma_target
ticker = sys.argv[1]
if not check_valid_ticker(ticker):
    print(f"{Colors.RED}Invalid stock ticker: {ticker}{Colors.RESET}")
    exit(1)


# Check for valid ma_target
ma_target = sys.argv[2]
if not check_valid_target(ma_target):
    print(f"{Colors.RED}Invalid moving average target. Must be a positive value.{Colors.RESET}")
    exit(1)

ma_target = float(ma_target)

# Simulated progress effect
print(f"{Colors.YELLOW}Fetching stock data for {ticker}...{Colors.RESET}")
time.sleep(1)

# Retrieve stock data from Yahoo Finance
stock_data = get_stock_data(ticker)

# Calculate moving averages
stock_data['150_MA'] = calculate_moving_averages(stock_data, 150)
stock_data['50_MA'] = calculate_moving_averages(stock_data, 50)

# Check if Close column exists and extract price correctly for multi-index data
if 'Close' in stock_data.columns and ticker in stock_data['Close']:
    current_price = stock_data['Close'][ticker].dropna().iloc[-1]  # Get most recent valid closing price
else:
    current_price = "N/A"

# Predict when the 150-day moving average will hit target
days_needed, error_message = predict_ma_hit(stock_data, 150, ma_target)

table_data = [
    ["Stock Ticker", ticker],
    ["Current Price", f"${current_price:,.2f}" if isinstance(current_price, (int, float)) else "N/A"],
    ["Target Moving Average", f"${ma_target:,.2f}"],
    ["Projected Days Until Target", f"{Colors.GREEN}{days_needed} days{Colors.RESET}" if days_needed else f"{Colors.RED}{error_message}{Colors.RESET}"]
]

print(f"{Colors.BOLD}\n📊 Stock Analysis for {ticker}{Colors.RESET}")
print(tabulate(table_data, tablefmt="fancy_grid"))

if days_needed:
    print(f"\n{Colors.BLUE}🚀 Based on current trends, {ticker} is expected to hit ${ma_target} in approximately {days_needed} days!{Colors.RESET}")
else:
    print(f"\n{Colors.RED}⚠️ {error_message}{Colors.RESET}")