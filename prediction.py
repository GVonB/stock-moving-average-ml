# Import necessary libraries
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np

# Retrieves stock data over specified time
def get_stock_data(ticker, days=150):
    return yf.download(ticker, period=f'{days}d')

# Test case
ticker = "AAPL"
stock_data = get_stock_data(ticker)

print(stock_data)