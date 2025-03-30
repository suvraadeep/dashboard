import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

# Fetch stock data
def fetch_stock_data(ticker, period, interval):
    try:
        end_date = datetime.now()
        if period == '1wk':
            start_date = end_date - timedelta(days=7)
            data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        else:
            data = yf.download(ticker, period=period, interval=interval)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Process data
def process_data(data):
    if not data.empty:
        if data.index.tzinfo is None:
            data.index = data.index.tz_localize('UTC')
        data.index = data.index.tz_convert('US/Eastern')
        data.reset_index(inplace=True)
        data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

# Calculate basic stock metrics
def calculate_metrics(data):
    last_close = float(data['Close'].iloc[-1])
    prev_close = float(data['Close'].iloc[0])
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = float(data['High'].max())
    low = float(data['Low'].min())
    volume = int(data['Volume'].sum())
    return last_close, change, pct_change, high, low, volume

# Add technical indicators
def add_technical_indicators(data):
    if 'Close' in data.columns:
        data['SMA_20'] = ta.trend.sma_indicator(data['Close'].squeeze(), window=20)
        data['EMA_20'] = ta.trend.ema_indicator(data['Close'].squeeze(), window=20)
        data.dropna(inplace=True)
    return data

# Streamlit UI
st.set_page_config(layout="wide")
st.title('Real-Time Stock Dashboard')

st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'ADBE')
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

interval_mapping = {'1d': '1m', '1wk': '30m', '1mo': '1d', '1y': '1wk', 'max': '1wk'}

if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    if not data.empty:
        data = process_data(data)
        data = add_technical_indicators(data)
        last_close, change, pct_change, high, low, volume = calculate_metrics(data)
        
        st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("High", f"{high:.2f} USD")
        col2.metric("Low", f"{low:.2f} USD")
        col3.metric("Volume", f"{volume:,}")
        
        fig = go.Figure()
        if chart_type == 'Candlestick':
            fig.add_trace(go.Candlestick(x=data['Datetime'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))
        else:
            fig = px.line(data, x='Datetime', y='Close')
        
        for indicator in indicators:
            if indicator == 'SMA 20':
                fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20'))
            elif indicator == 'EMA 20':
                fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))
        
        fig.update_layout(title=f'{ticker} {time_period.upper()} Chart', xaxis_title='Time', yaxis_title='Price (USD)', height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader('Historical Data')
        st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])
        
        st.subheader('Technical Indicators')
        st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])
    else:
        st.warning(f"No data available for {ticker}.")

st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = float(real_time_data['Close'].iloc[-1])
        change = float(real_time_data['Close'].iloc[-1] - real_time_data['Open'].iloc[0])
        pct_change = (change / float(real_time_data['Open'].iloc[0])) * 100
        st.sidebar.metric(f"{symbol}", f"{last_price:.2f} USD", f"{change:.2f} ({pct_change:.2f}%)")
    else:
        st.sidebar.warning(f"No data for {symbol}.")

st.sidebar.subheader('About')
st.sidebar.info('This dashboard provides stock data and technical indicators for various time periods. Use the sidebar to customize your view.')
