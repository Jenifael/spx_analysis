# 📈 SPX Analysis Dashboard

A comprehensive Streamlit application for analyzing S&P 500 (SPX) data with interactive charts, technical indicators, and real-time analysis.

## 🚀 Features

### Daily Analysis
- **4-Hour Candlestick Charts** with EMA 50 and EMA 200
- **Flexible Time Periods** (1 Month to 5 Years)
- **Daily Summary Table** with last 30 days data
- **Last 5-Minute Analysis** with point variations and trend indicators
- **Day of Week** identification and colored trend arrows

### Intraday Analysis
- **1-Minute Candlestick Charts** with MACD and EMA 200
- **Date Selector** for historical intraday analysis
- **Customizable MACD Parameters** (Fast, Slow, Signal periods)
- **Real-time Technical Analysis** with bullish/bearish signals
- **Last Hour Focus** for end-of-day momentum analysis

## 🛠️ Windows Installation

### Prerequisites
- **Python 3.8+** installed on Windows
- **Internet connection** for data fetching

### Step 1: Clone the Repository
```cmd
git clone https://github.com/yourusername/spx_analysis.git
cd spx_analysis
```

### Step 2: Create Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 4: Run the Application
```cmd
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 What You'll See

### Daily Analysis Page
- **4-Hour Price Chart**: Interactive candlestick chart with EMA overlays
- **Key Metrics**: Current price, period high/low, average volume
- **Daily Summary Table**: Last 30 days with opening, closing, daily %, and trend indicators

### Intraday Analysis Page
- **1-Minute Candlesticks**: Detailed intraday price action
- **MACD Analysis**: Moving Average Convergence Divergence with histogram
- **Technical Signals**: Real-time bullish/bearish indicators
- **Hourly Metrics**: Price changes and volume for the selected hour

## 🔧 Technical Details

### Dependencies
- `streamlit`: Web application framework
- `yfinance`: Yahoo Finance data API
- `pandas`: Data manipulation
- `plotly`: Interactive charts
- `pytz`: Timezone handling

### Data Sources
- **Yahoo Finance**: Real-time and historical S&P 500 data
- **Symbol**: ^GSPC (S&P 500 Index)
- **Timeframes**: 1-minute (last 30 days), 4-hour (up to 5 years)

## 🎯 Key Features

### Technical Indicators
- **EMA 50 & 200**: Trend identification
- **MACD**: Momentum analysis
- **Last 5-Minute Analysis**: End-of-day momentum

### Timezone Support
- **Paris Time (CET/CEST)**: All charts and data display in Paris timezone
- **Automatic Conversion**: Handles both winter and summer time

### Data Limitations
- **1-Minute Data**: Available for last 30 days only
- **4-Hour Data**: Available for up to 5 years
- **Real-time Updates**: Data refreshes automatically

## 🚀 Quick Start

1. **Activate your environment**:
   ```cmd
   venv\Scripts\activate
   ```

2. **Run the app**:
   ```cmd
   streamlit run app.py
   ```

3. **Navigate**: Use the sidebar to switch between Daily and Intraday analysis

4. **Analyze**: Select time periods, dates, and customize parameters

## 📁 Project Structure

```
spx_analysis/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore rules
└── venv/              # Virtual environment (created after setup)
```

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It should not be used as the sole basis for investment decisions. Always consult with a qualified financial advisor before making investment choices.

## 🐛 Troubleshooting

### Common Issues
1. **Data loading errors**: Check your internet connection
2. **Module not found**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. **Port already in use**: Try `streamlit run app.py --server.port 8502`

### Getting Help
- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Check the [yfinance documentation](https://pypi.org/project/yfinance/)

---

**Happy Analyzing! 📊✨**