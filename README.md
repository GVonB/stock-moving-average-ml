# 📈 Stock Moving Average Prediction Tool

## 🔍 Overview
This Python script predicts when a stock's **150-day moving average** will reach a given target price using **linear regression**. It fetches historical stock data via `yfinance`, performs calculations, and presents the results in a clean, easy-to-read table format.

---

## 🚀 Features
- Fetches **real-time stock data** from Yahoo Finance.
- Calculates **50-day and 150-day moving averages**.
- Uses **linear regression** to predict the crossover date.
- **Beautiful terminal output** with ANSI colors and a formatted table.

---

## 🛠 Installation
If you're new to Python and Git, follow these steps to install and run the project.

### 1️⃣ Install Python (if not already installed)
Ensure you have Python **3.8+** installed. Check with:
```sh
python3 --version
```
If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### 2️⃣ Clone the Repository
If you have Git installed, run:
```sh
git clone https://github.com/GVonB/stock-moving-average-ml.git
cd stock-moving-average-ml
```
If you don’t have Git, download the ZIP file from GitHub and extract it manually.

### 3️⃣ Create a Virtual Environment (Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

### 4️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

---

## 📌 Usage
Run the script using the command:
```sh
python3 prediction.py <STOCK_TICKER> <TARGET_PRICE>
```
### Example:
```sh
python3 prediction.py NVDA 150
```

This command predicts when **NVIDIA (NVDA)** will have a **150-day moving average** reaching **$150.00**.

---

## 📊 Example Output
```sh
Fetching stock data for NVDA...

📊 Stock Analysis for NVDA
╒═════════════════════════════╤═════════════╕
│ Stock Ticker                │ NVDA        │
├─────────────────────────────┼─────────────┤
│ Current Price               │ $116.66     │
├─────────────────────────────┼─────────────┤
│ Target Moving Average       │ $150.00     │
├─────────────────────────────┼─────────────┤
│ Projected Days Until Target │ 197.52 days │
╘═════════════════════════════╧═════════════╛

🚀 Based on current trends, NVDA is expected to hit $150.0 in approximately 197.52 days!
```

---

## ❓ FAQ
### 1️⃣ What if I get `Invalid stock ticker`?
Make sure you're entering a **valid ticker symbol** (e.g., `AAPL`, `TSLA`, `GOOGL`).

### 2️⃣ How do I update dependencies?
Run:
```sh
pip install --upgrade -r requirements.txt
```

### 3️⃣ Can I predict other moving averages?
Currently, the script is set to **150-day MA**, but you can modify `predict_ma_hit()` to use **custom time frames**.
The necessary format is shown in the **50-day MA**, which is currently calculated but unused.

---

## 🤝 Contributing
Feel free to submit pull requests or open issues for improvements.

---

## 📝 License
This project is open-source under the **MIT License**.

