import pandas as pd
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

def predict_ma_projection(data, ma_window, ma_target, days_forward=30):
    ma = data['Close'].rolling(window=ma_window).mean()
    ma_recent = ma.dropna().values  # Drop NaNs
    
    if len(ma_recent) < 10:
        return None, None, "Not enough data for a reliable prediction."
    
    x = np.arange(len(ma_recent)).reshape(-1, 1)
    y = ma_recent

    model = LinearRegression()
    model.fit(x, y)
    
    # Use correct indexing for 1D arrays
    if abs(model.coef_[0]) < 1e-5:
        return None, None, "No significant trend detected, unable to predict crossover."
    
    intercept = model.intercept_
    coef = model.coef_[0]
    
    days_needed = (ma_target - intercept) / coef
    if days_needed < 0:
        return None, None, f"The {ma_window}-day moving average is already below ${ma_target:.2f}."
    
    last_day_index = len(ma_recent) - 1
    future_indexes = np.arange(last_day_index + 1, last_day_index + 1 + days_forward).reshape(-1, 1)
    future_ma = model.predict(future_indexes)
    future_ma = future_ma.flatten()  # Ensure it's 1D
    
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=days_forward)
    projection_df = pd.DataFrame({'Date': future_dates, 'Predicted_MA': future_ma})
    
    return round(days_needed, 2), projection_df, None