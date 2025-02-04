# Stock Moving Average Predictor

This project uses Python, `yfinance`, and `scikit-learn` to analyze stock price trends and predict when a stock's moving average will reach a specified target price.

## Features
- Fetches historical stock data using Yahoo Finance.
- Calculates moving averages (e.g., 50-day, 150-day).
- Uses linear regression to estimate when a moving average will hit a target price.

## Installation
Ensure you have Python installed, then install dependencies:
```bash
pip install pandas yfinance scikit-learn numpy
```

## Usage
Modify the `ticker` and `ma_target` variables as needed in `main.py`:
```python
ticker = "NVDA"
ma_target = 145
```
Run the script:
```bash
python3 prediction.py
```

## Example Output
```
In approximately 12.45 days.
```

## License
This project is open-source under the MIT License.
