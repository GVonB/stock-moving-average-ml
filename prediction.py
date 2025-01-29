# Import necessary libraries
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np

# Retrieves stock data over specified time
def get_stock_data(ticker, days=150):
    return yf.download(ticker, period=f'{days}d')

# Calculates moving average
def calculate_moving_averages(data, window):
    return data['Close'].rolling(window=window).mean()

# Test case
ticker = "AAPL"
stock_data = get_stock_data(ticker)

# Calculate moving averages
stock_data['150_MA'] = calculate_moving_averages(stock_data, 150)
stock_data['50_MA'] = calculate_moving_averages(stock_data, 50)

print(stock_data)