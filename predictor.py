import pandas as py
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

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
    
def get_stock_data(ticker, days=300):
    return yf.download(ticker, period=f'{days}d', progress=False)

def calculate_moving_averages(data, window):
    return data['Close'].rolling(window=window).mean()

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