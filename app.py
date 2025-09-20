import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="SPX Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


def load_4h_data(period="1y"):
    """Load 4-hour S&P 500 data from Yahoo Finance"""
    try:
        spx = yf.Ticker("^GSPC")
        data = spx.history(period=period, interval="4h")
        
        # Convert to Paris time for consistency
        data = convert_to_paris_time(data)
        
        return data
    except Exception as e:
        st.error(f"Error loading 4-hour data: {str(e)}")
        return None

def convert_to_paris_time(data):
    """Convert data index to Paris timezone"""
    if data is None or data.empty:
        return data
    
    try:
        # Convert to Paris timezone (handles both CET and CEST automatically)
        paris_tz = pytz.timezone('Europe/Paris')
        
        # If data is timezone-naive, assume it's UTC and localize it
        if data.index.tz is None:
            data.index = data.index.tz_localize('UTC')
        
        # Convert to Paris time
        data.index = data.index.tz_convert(paris_tz)
        
        return data
    except Exception as e:
        st.warning(f"Could not convert timezone: {str(e)}")
        return data

def load_intraday_data(date_str, interval="1m"):
    """Load 1-minute intraday data for a specific date"""
    try:
        spx = yf.Ticker("^GSPC")
        
        # Convert date string to datetime for better handling
        from datetime import datetime
        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)
        
        # Get data for the specific date with a small buffer
        data = spx.history(
            start=start_date.strftime("%Y-%m-%d"), 
            end=end_date.strftime("%Y-%m-%d"), 
            interval=interval
        )
        
        # Filter data to only include the requested date
        if not data.empty:
            data = data[data.index.date == start_date.date()]
        
        # Convert to Paris time
        data = convert_to_paris_time(data)
        
        return data
    except Exception as e:
        st.error(f"Error loading intraday data: {str(e)}")
        return None

def load_intraday_data_robust(date_str, interval="1m"):
    """More robust intraday data loading with fallback options"""
    try:
        # First try the specific date
        data = load_intraday_data(date_str, interval)
        
        if data is not None and not data.empty:
            return data
        
        # If no data, try a few days back
        from datetime import datetime, timedelta
        original_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        for days_back in range(1, 8):  # Try up to 7 days back
            try_date = original_date - timedelta(days=days_back)
            data = load_intraday_data(try_date.strftime("%Y-%m-%d"), interval)
            
            if data is not None and not data.empty:
                st.info(f"Using data from {try_date.strftime('%Y-%m-%d')} (original date had no data)")
                return data
                
        return None
        
    except Exception as e:
        st.error(f"Error in robust data loading: {str(e)}")
        return None

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    ema_fast = data['Close'].ewm(span=fast).mean()
    ema_slow = data['Close'].ewm(span=slow).mean()
    
    data['MACD'] = ema_fast - ema_slow
    data['MACD_Signal'] = data['MACD'].ewm(span=signal).mean()
    data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
    
    return data

def calculate_ema(data, period=200):
    """Calculate Exponential Moving Average"""
    data[f'EMA_{period}'] = data['Close'].ewm(span=period).mean()
    return data

def create_candlestick_chart(data):
    """Create 1-minute candlestick chart with MACD and EMA 200"""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='SPX',
        increasing_line_color='#00ff00',
        decreasing_line_color='#ff0000'
    ))
    
    # EMA 200
    if 'EMA_200' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['EMA_200'],
            mode='lines',
            name='EMA 200',
            line=dict(color='purple', width=2)
        ))
    
    fig.update_layout(
        title="SPX 1-Minute Candlestick Chart (Paris Time)",
        xaxis_title="Time (CET/CEST)",
        yaxis_title="Price ($)",
        height=500,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_4h_candlestick_chart(data):
    """Create 4-hour candlestick chart with EMA 50 and EMA 200"""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='SPX',
        increasing_line_color='#00ff00',
        decreasing_line_color='#ff0000'
    ))
    
    # EMA 50
    if 'EMA_50' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['EMA_50'],
            mode='lines',
            name='EMA 50',
            line=dict(color='orange', width=2)
        ))
    
    # EMA 200
    if 'EMA_200' in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['EMA_200'],
            mode='lines',
            name='EMA 200',
            line=dict(color='purple', width=2)
        ))
    
    fig.update_layout(
        title="SPX 4-Hour Candlestick Chart (Paris Time)",
        xaxis_title="Time (CET/CEST)",
        yaxis_title="Price ($)",
        height=500,
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_daily_summary_table(data):
    """Create daily summary table with opening, closing, percent change, and trend"""
    if data is None or data.empty:
        return None
    
    # Get daily data (resample to daily)
    daily_data = data.resample('D').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()
    
    # Calculate daily percent change
    daily_data['Daily_Change'] = daily_data['Close'].pct_change() * 100
    
    # Create daily trend column with colored arrows
    daily_data['Daily_Trend'] = daily_data['Daily_Change'].apply(
        lambda x: '🟢🔼' if x > 0 else '🔴🔽' if x < 0 else '⚪➡️'
    )
    
    # Calculate last 5 minutes variation for each day (last 30 days only)
    daily_data['Last_5min_Change'] = 0.0  # Initialize
    daily_data['Last_5min_Trend'] = '⚪➡️'  # Initialize
    
    # Only process the last 30 days (where 1-minute data is available)
    recent_daily_data = daily_data.tail(30)
    
    # For each day in the last 30 days, get the last 5 minutes of trading data
    for i, (date, row) in enumerate(recent_daily_data.iterrows()):
        try:
            # Get intraday data for this specific date
            date_str = date.strftime('%Y-%m-%d')
            intraday_data = load_intraday_data(date_str, "1m")
            
            if intraday_data is not None and not intraday_data.empty:
                # Get the last 5 minutes of data
                last_5min = intraday_data.tail(5)
                if len(last_5min) >= 2:
                    # Calculate the change in the last 5 minutes
                    start_price = last_5min['Close'].iloc[0]
                    end_price = last_5min['Close'].iloc[-1]
                    change_points = end_price - start_price
                    daily_data.loc[date, 'Last_5min_Change'] = change_points
                    
                    # Create trend for last 5 minutes
                    if change_points > 0:
                        daily_data.loc[date, 'Last_5min_Trend'] = '🟢🔼'
                    elif change_points < 0:
                        daily_data.loc[date, 'Last_5min_Trend'] = '🔴🔽'
                    else:
                        daily_data.loc[date, 'Last_5min_Trend'] = '⚪➡️'
        except:
            # If we can't get intraday data, keep default values
            pass
    
    # Format the data for display - show last 30 days
    summary_data = []
    recent_data = daily_data.tail(30)  # Show last 30 days
    for date, row in recent_data.iterrows():
        # Get day of the week
        day_name = date.strftime('%A')
        
        summary_data.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Day': day_name,
            'Opening': f"${row['Open']:.2f}",
            'Closing': f"${row['Close']:.2f}",
            'Daily %': f"{row['Daily_Change']:.2f}%",
            'Daily Trend': row['Daily_Trend'],
            'Last 5min (pts)': f"{row['Last_5min_Change']:+.2f}",
            'Last 5min Trend': row['Last_5min_Trend']
        })
    
    return pd.DataFrame(summary_data)

def create_macd_chart(data):
    """Create MACD chart"""
    fig = go.Figure()
    
    # MACD line
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD'],
        mode='lines',
        name='MACD',
        line=dict(color='blue', width=2)
    ))
    
    # Signal line
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD_Signal'],
        mode='lines',
        name='Signal',
        line=dict(color='red', width=2)
    ))
    
    # Histogram
    colors = ['green' if val >= 0 else 'red' for val in data['MACD_Histogram']]
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['MACD_Histogram'],
        name='Histogram',
        marker_color=colors,
        opacity=0.7
    ))
    
    # Zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title="MACD (Moving Average Convergence Divergence) - Paris Time",
        xaxis_title="Time (CET/CEST)",
        yaxis_title="MACD",
        height=300
    )
    
    return fig

def daily_analysis_page():
    """Daily analysis page with 4-hour candlesticks and daily summary"""
    # Header
    st.markdown('<h1 class="main-header">📈 SPX Daily Analysis</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("Settings")
    
    # Time period selection
    period_options = {
        "1 Month": "1mo",
        "3 Months": "3mo", 
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y",
        "5 Years": "5y",
        "Max": "max"
    }
    
    selected_period = st.sidebar.selectbox(
        "Select Time Period",
        options=list(period_options.keys()),
        index=3  # Default to 1 year
    )
    
    # Load 4-hour data for the selected period
    with st.spinner("Loading 4-hour SPX data..."):
        data = load_4h_data(period_options[selected_period])
    
    if data is not None and not data.empty:
        
        # Calculate EMAs
        data = calculate_ema(data, 50)
        data = calculate_ema(data, 200)
        
        # Key metrics
        st.subheader("📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_price = data['Close'].iloc[-1]
            st.metric(
                label="Current Price",
                value=f"${current_price:.2f}",
                delta=f"{data['Close'].pct_change().iloc[-1]*100:.2f}%"
            )
        
        with col2:
            high_period = data['High'].max()
            st.metric(
                label="Period High",
                value=f"${high_period:.2f}"
            )
        
        with col3:
            low_period = data['Low'].min()
            st.metric(
                label="Period Low", 
                value=f"${low_period:.2f}"
            )
        
        with col4:
            avg_volume = data['Volume'].mean()
            st.metric(
                label="Avg Volume",
                value=f"{avg_volume:,.0f}"
            )
        
        # 4-Hour Candlestick Chart
        st.subheader("📈 4-Hour Price Analysis")
        
        # Candlestick chart with EMAs
        candlestick_chart = create_4h_candlestick_chart(data)
        st.plotly_chart(candlestick_chart, use_container_width=True)
        
        # Daily Summary Table (independent - always last 30 days)
        st.subheader("📋 Daily Summary")
        
        # Add info about data limitations
        st.info("💡 **Data Note**: Table shows last 30 days with accurate 1-minute data for last 5 minutes calculation.")
        
        # Load separate data for the table (last 30 days only)
        with st.spinner("Loading data for daily summary table..."):
            table_data = load_4h_data("1mo")  # Always last 30 days for table
        
        if table_data is not None and not table_data.empty:
            summary_table = create_daily_summary_table(table_data)
            if summary_table is not None:
                st.dataframe(
                    summary_table, 
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Unable to generate daily summary table.")
        else:
            st.warning("Unable to load data for daily summary table.")
        
    else:
        st.error("Failed to load data. Please check your internet connection and try again.")

def intraday_analysis_page():
    """Intraday analysis page with 1-minute candles"""
    # Header
    st.markdown('<h1 class="main-header">⚡ SPX Intraday Analysis</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("Intraday Settings")
    
    # Date selector
    selected_date = st.sidebar.date_input(
        "Select Date",
        value=datetime.now().date(),
        max_value=datetime.now().date()
    )
    
    # MACD parameters
    st.sidebar.subheader("MACD Parameters")
    macd_fast = st.sidebar.slider("MACD Fast Period", 5, 20, 12)
    macd_slow = st.sidebar.slider("MACD Slow Period", 20, 50, 26)
    macd_signal = st.sidebar.slider("MACD Signal Period", 5, 15, 9)
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data", help="Try to reload data if it failed"):
        st.rerun()
    
    # Timezone info
    st.sidebar.info("🕐 All times displayed in Paris time (CET/CEST)")
    
    # Load intraday data with robust fallback
    with st.spinner(f"Loading 1-minute data for {selected_date}..."):
        data = load_intraday_data_robust(str(selected_date), "1m")
    
    # If 1-minute data is not available, try 5-minute data
    if data is None or data.empty:
        st.warning("1-minute data not available, trying 5-minute data...")
        with st.spinner("Loading 5-minute data..."):
            data = load_intraday_data_robust(str(selected_date), "5m")
    
    # Debug information
    if data is not None:
        st.info(f"Data loaded: {len(data)} records for {selected_date}")
        if not data.empty:
            # Format time display for Paris timezone
            start_time = data.index[0].strftime("%Y-%m-%d %H:%M:%S %Z")
            end_time = data.index[-1].strftime("%Y-%m-%d %H:%M:%S %Z")
            st.info(f"Time range (Paris): {start_time} to {end_time}")
        else:
            st.warning("No data found for the selected date. This might be because:")
            st.write("- The market was closed (weekends, holidays)")
            st.write("- The date is too recent (intraday data might not be available yet)")
            st.write("- There was a data service issue")
            st.write("Try selecting a different date or check if the market was open.")
    
    if data is not None and not data.empty:
        # Filter last hour of trading (assuming market closes at 4:00 PM ET)
        # Get the last 60 minutes of data
        data = data.tail(60)
        
        # Calculate technical indicators
        data = calculate_macd(data, macd_fast, macd_slow, macd_signal)
        data = calculate_ema(data, 200)
        
        # Key metrics for the hour
        st.subheader("📊 Hourly Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_price = data['Close'].iloc[-1]
            price_change = data['Close'].iloc[-1] - data['Open'].iloc[0]
            st.metric(
                label="Current Price",
                value=f"${current_price:.2f}",
                delta=f"${price_change:.2f}"
            )
        
        with col2:
            high_hour = data['High'].max()
            st.metric(
                label="Hour High",
                value=f"${high_hour:.2f}"
            )
        
        with col3:
            low_hour = data['Low'].min()
            st.metric(
                label="Hour Low",
                value=f"${low_hour:.2f}"
            )
        
        with col4:
            volume_hour = data['Volume'].sum()
            st.metric(
                label="Hour Volume",
                value=f"{volume_hour:,.0f}"
            )
        
        # Charts
        st.subheader("📈 Intraday Analysis")
        
        # Candlestick chart
        candlestick_chart = create_candlestick_chart(data)
        st.plotly_chart(candlestick_chart, use_container_width=True)
        
        # MACD chart
        macd_chart = create_macd_chart(data)
        st.plotly_chart(macd_chart, use_container_width=True)
        
        # Additional analysis
        st.subheader("📊 Technical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Price vs EMA 200**")
            if 'EMA_200' in data.columns:
                price_above_ema = data['Close'].iloc[-1] > data['EMA_200'].iloc[-1]
                ema_distance = ((data['Close'].iloc[-1] - data['EMA_200'].iloc[-1]) / data['EMA_200'].iloc[-1]) * 100
                
                if price_above_ema:
                    st.success(f"Price is {ema_distance:.2f}% above EMA 200")
                else:
                    st.error(f"Price is {abs(ema_distance):.2f}% below EMA 200")
        
        with col2:
            st.write("**MACD Signal**")
            if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
                macd_current = data['MACD'].iloc[-1]
                signal_current = data['MACD_Signal'].iloc[-1]
                macd_above_signal = macd_current > signal_current
                
                if macd_above_signal:
                    st.success("MACD above Signal Line (Bullish)")
                else:
                    st.error("MACD below Signal Line (Bearish)")
        
        # Data table
        st.subheader("📋 Recent 1-Minute Data")
        st.dataframe(data.tail(20), use_container_width=True)
        
    else:
        st.error(f"No intraday data available for {selected_date}. Please select a different date or check if the market was open on that day.")

def main():
    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        ["Daily Analysis", "Intraday Analysis"]
    )
    
    if page == "Daily Analysis":
        daily_analysis_page()
    elif page == "Intraday Analysis":
        intraday_analysis_page()

if __name__ == "__main__":
    main()
