# Stock Dashboard

This project is a real-time stock dashboard built using **Streamlit**, **Plotly**, and **Yahoo Finance API (yfinance)**. It allows users to visualize stock price data with interactive charts and technical indicators.

Deployed Link: 
https://huggingface.co/spaces/suvradeepp/stocks-dashboard

## Features
- Fetches real-time stock data using **Yahoo Finance API**
- Supports multiple time periods (**1d, 1wk, 1mo, 1y, max**)
- Candlestick and line chart visualization using **Plotly**
- Displays stock metrics including **last price, daily change, high, low, and volume**
- Includes **Simple Moving Average (SMA 20)** and **Exponential Moving Average (EMA 20)** as technical indicators
- Sidebar to **select stock ticker, chart type, and indicators**
- **Real-time stock prices** of selected stocks displayed in the sidebar

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/suvraadeep/dashboard.git
cd dashboard
```

### 2. Create and Activate Virtual Environment
#### On Windows:
```bash
python -m venv dashboard
.\dashboard\Scripts\activate
```

#### On macOS/Linux:
```bash
python -m venv dashboard
source dashboard/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
Run the Streamlit app using the following command:
```bash
streamlit run app.py
```

This will launch the dashboard in your default web browser.

## Required Dependencies
The `requirements.txt` file includes the necessary dependencies:
```
streamlit
plotly
pandas
yfinance
pytz
ta
```

## How It Works
1. **User Input**: Select a stock ticker, time period, and chart type from the sidebar.
2. **Fetching Data**: Retrieves stock data from Yahoo Finance.
3. **Data Processing**: Converts timestamps, calculates metrics, and applies indicators.
4. **Visualization**: Plots interactive charts and displays key stock metrics.
5. **Real-Time Prices**: Displays updated prices for selected stocks in the sidebar.

## Example Screenshot
![image](https://github.com/user-attachments/assets/72fc7817-e755-4a12-a35b-4ad6fe37b732)





