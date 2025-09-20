# 📈 SPX Analysis Dashboard

A comprehensive Streamlit application for analyzing S&P 500 (SPX) data with interactive charts, technical indicators, and statistical analysis.

## 🚀 Features

- **Real-time Data**: Fetches live S&P 500 data from Yahoo Finance
- **Interactive Charts**: Beautiful, interactive charts using Plotly
- **Technical Indicators**: 
  - Moving Averages (20, 50, 200 day)
  - Bollinger Bands
  - Relative Strength Index (RSI)
- **Statistical Analysis**:
  - Returns distribution
  - Rolling volatility
  - Key performance metrics
- **Multiple Time Periods**: Analyze data from 1 month to maximum available
- **Responsive Design**: Clean, modern UI that works on all devices

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for data fetching

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/spx_analysis.git
   cd spx_analysis
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Use the sidebar** to:
   - Select different time periods
   - Adjust analysis parameters

## 📊 What You'll See

### Main Dashboard
- **Key Metrics**: Current price, 52-week high/low, average volume
- **Price Chart**: Interactive price chart with moving averages and Bollinger Bands
- **Volume Chart**: Trading volume over time
- **RSI Chart**: Relative Strength Index with overbought/oversold levels

### Statistical Analysis
- **Returns Distribution**: Histogram of daily returns
- **Rolling Volatility**: 30-day rolling volatility chart
- **Data Table**: Recent price data

## 🔧 Technical Details

### Dependencies
- `streamlit`: Web application framework
- `yfinance`: Yahoo Finance data API
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `seaborn`: Statistical data visualization
- `matplotlib`: Plotting library
- `plotly`: Interactive charts

### Data Sources
- **Yahoo Finance**: Real-time and historical S&P 500 data
- **Symbol**: ^GSPC (S&P 500 Index)

## 📁 Project Structure

```
spx_analysis/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignore rules
└── venv/              # Virtual environment (created after setup)
```

## 🎯 Key Features Explained

### Technical Indicators
- **Moving Averages**: Trend-following indicators
- **Bollinger Bands**: Volatility and support/resistance levels
- **RSI**: Momentum oscillator (0-100 scale)

### Time Periods
- 1 Month, 3 Months, 6 Months
- 1 Year, 2 Years, 5 Years
- Maximum available data

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy your app with one click

### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Docker**: Create a `Dockerfile` for containerized deployment
- **AWS/GCP/Azure**: Deploy using their respective cloud services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It should not be used as the sole basis for investment decisions. Always consult with a qualified financial advisor before making investment choices.

## 🐛 Troubleshooting

### Common Issues

1. **Data loading errors**: Check your internet connection
2. **Module not found**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. **Port already in use**: Try `streamlit run app.py --server.port 8502`

### Getting Help

- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Open an issue on GitHub
- Check the [yfinance documentation](https://pypi.org/project/yfinance/)

## 📈 Future Enhancements

- [ ] Add more technical indicators (MACD, Stochastic, etc.)
- [ ] Support for other indices (NASDAQ, DOW, etc.)
- [ ] Portfolio analysis features
- [ ] Export functionality for charts and data
- [ ] Alert system for price movements
- [ ] Backtesting capabilities
- [ ] Machine learning predictions

---

**Happy Analyzing! 📊✨**
