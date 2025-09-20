import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
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

def load_spx_data(period="1y"):
    """Load S&P 500 data from Yahoo Finance"""
    try:
        spx = yf.Ticker("^GSPC")
        data = spx.history(period=period)
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def calculate_technical_indicators(data):
    """Calculate common technical indicators"""
    # Moving averages
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['MA_200'] = data['Close'].rolling(window=200).mean()
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    data['BB_Middle'] = data['Close'].rolling(window=20).mean()
    bb_std = data['Close'].rolling(window=20).std()
    data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
    data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
    
    return data

def create_price_chart(data):
    """Create interactive price chart with technical indicators"""
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='SPX Close',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Moving averages
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_20'],
        mode='lines',
        name='MA 20',
        line=dict(color='orange', width=1, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_50'],
        mode='lines',
        name='MA 50',
        line=dict(color='red', width=1, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_200'],
        mode='lines',
        name='MA 200',
        line=dict(color='purple', width=1, dash='dash')
    ))
    
    # Bollinger Bands
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['BB_Upper'],
        mode='lines',
        name='BB Upper',
        line=dict(color='gray', width=1, dash='dot'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['BB_Lower'],
        mode='lines',
        name='BB Lower',
        line=dict(color='gray', width=1, dash='dot'),
        fill='tonexty',
        fillcolor='rgba(128,128,128,0.1)',
        showlegend=False
    ))
    
    fig.update_layout(
        title="S&P 500 Price Chart with Technical Indicators",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode='x unified',
        height=600
    )
    
    return fig

def create_volume_chart(data):
    """Create volume chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        height=300
    )
    
    return fig

def create_rsi_chart(data):
    """Create RSI chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='purple', width=2)
    ))
    
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    
    fig.update_layout(
        title="Relative Strength Index (RSI)",
        xaxis_title="Date",
        yaxis_title="RSI",
        yaxis=dict(range=[0, 100]),
        height=300
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">📈 SPX Analysis Dashboard</h1>', unsafe_allow_html=True)
    
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
    
    # Load data
    with st.spinner("Loading SPX data..."):
        data = load_spx_data(period_options[selected_period])
    
    if data is not None and not data.empty:
        # Calculate technical indicators
        data = calculate_technical_indicators(data)
        
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
            high_52w = data['High'].max()
            st.metric(
                label="52-Week High",
                value=f"${high_52w:.2f}"
            )
        
        with col3:
            low_52w = data['Low'].min()
            st.metric(
                label="52-Week Low", 
                value=f"${low_52w:.2f}"
            )
        
        with col4:
            avg_volume = data['Volume'].mean()
            st.metric(
                label="Avg Volume",
                value=f"{avg_volume:,.0f}"
            )
        
        # Charts
        st.subheader("📈 Price Analysis")
        
        # Price chart
        price_chart = create_price_chart(data)
        st.plotly_chart(price_chart, use_container_width=True)
        
        # Volume and RSI charts
        col1, col2 = st.columns(2)
        
        with col1:
            volume_chart = create_volume_chart(data)
            st.plotly_chart(volume_chart, use_container_width=True)
        
        with col2:
            rsi_chart = create_rsi_chart(data)
            st.plotly_chart(rsi_chart, use_container_width=True)
        
        # Statistical Analysis
        st.subheader("📊 Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Returns Distribution**")
            returns = data['Close'].pct_change().dropna()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(returns, kde=True, ax=ax)
            ax.set_title("Daily Returns Distribution")
            ax.set_xlabel("Daily Return")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        
        with col2:
            st.write("**Rolling Volatility**")
            rolling_vol = returns.rolling(window=30).std() * np.sqrt(252)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data.index[29:], rolling_vol[29:])
            ax.set_title("30-Day Rolling Volatility")
            ax.set_xlabel("Date")
            ax.set_ylabel("Volatility")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
        
        # Data table
        st.subheader("📋 Recent Data")
        st.dataframe(data.tail(10), use_container_width=True)
        
    else:
        st.error("Failed to load data. Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
