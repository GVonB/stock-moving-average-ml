# Import necessary libraries
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
import sys  # For command line arguments

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
    return yf.download(ticker, period=f'{days}d')

# Calculates moving average
def calculate_moving_averages(data, window):
    return data['Close'].rolling(window=window).mean()

# Predicts when a moving average will hit the target
def predict_ma_hit(data, ma_window, ma_target):
    ma = calculate_moving_averages(data, ma_window)
    ma_recent = ma.dropna().values  # Drop NaNs for regression
    
    if len(ma_recent) < 10:  # Ensure enough data points
        return "Not enough data for a reliable prediction."
    
    x = np.arange(len(ma_recent)).reshape(-1, 1)  # Days as features
    y = ma_recent

    # Train linear regression to predict MA trend
    model = LinearRegression()
    model.fit(x, y)

    # Avoid division by zero (flat moving average)
    if abs(model.coef_[0]) < 1e-5:
        return "No significant trend detected, unable to predict crossover."
    
    # Extract scalars
    intercept = model.intercept_[0]
    coef = model.coef_[0][0]

    # Predict when MA hits target
    days_needed = float((ma_target - intercept) / coef)
    return f"In approximately {days_needed:.2f} days." if days_needed > 0 else "Target will not be reached based on current trend."

# Check for additional command line arguments
argv_length = len(sys.argv)

# Handle incorrect number of command line arguments
if argv_length < 3:
    if argv_length == 1:
        print("Only 1 argument was passed instead of the required 3.")
    else:   
        print(f"{argv_length} arguments were passed instead of the required 3.")
    print("Please use the format when running the program:\npython3 ticker_symbol ma_target\n")
    exit(1)

# Validate this format: python3 ticker_symbol ma_target
ticker = sys.argv[1]
if not check_valid_ticker(ticker):
    exit("Invalid stock ticker.")

# Check for valid ma_target
ma_target = sys.argv[2]
if not check_valid_target(ma_target):
    exit("Invalid moving average target. Must be a positive value.")

# Retrieve stock data from Yahoo Finance
stock_data = get_stock_data(ticker)

# Calculate moving averages
stock_data['150_MA'] = calculate_moving_averages(stock_data, 150)
stock_data['50_MA'] = calculate_moving_averages(stock_data, 50)

# Predict when the 150-day moving average will hit target
ma_target = 145
prediction = predict_ma_hit(stock_data, 150, ma_target)

print(prediction)