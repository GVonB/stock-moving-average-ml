# prediction.py
import sys
import time
from tabulate import tabulate
from predictor import check_valid_ticker, get_stock_data, calculate_moving_averages, predict_ma_hit

# ANSI color codes for output
class Colors:
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

if len(sys.argv) < 3:
    print(f"{Colors.RED}Error: Missing arguments!{Colors.RESET}")
    print("Usage: python3 prediction.py <ticker> <target_moving_average>")
    exit(1)

ticker = sys.argv[1]
if not check_valid_ticker(ticker):
    print(f"{Colors.RED}Invalid stock ticker: {ticker}{Colors.RESET}")
    exit(1)

ma_target = sys.argv[2]
try:
    ma_target = float(ma_target)
    if ma_target < 0:
        raise ValueError
except ValueError:
    print(f"{Colors.RED}Invalid moving average target. Must be a positive value.{Colors.RESET}")
    exit(1)

print(f"{Colors.YELLOW}Fetching stock data for {ticker}...{Colors.RESET}")
time.sleep(1)
stock_data = get_stock_data(ticker)
stock_data['150_MA'] = calculate_moving_averages(stock_data, 150)
stock_data['50_MA'] = calculate_moving_averages(stock_data, 50)

# For multi-index data, check how to extract current price correctly
if 'Close' in stock_data.columns and ticker in stock_data['Close']:
    current_price = stock_data['Close'][ticker].dropna().iloc[-1]
else:
    current_price = "N/A"

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