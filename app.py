"""
Metal Prices Streamlit App - Real-time commodity price tracking with charts
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from api_client import MetalsLiveClient, MockMetalsClient
from database import PriceDatabase
from config import METALS, CURRENCY, PRICE_UPDATE_INTERVAL, CHART_DAYS
import time

# Page config
st.set_page_config(
    page_title="Metal Prices Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = PriceDatabase()

if 'last_update' not in st.session_state:
    st.session_state.last_update = None

# Header
st.title("💰 International Metal Prices Tracker")
st.markdown("Real-time commodity prices with historical tracking")

# API Client selection
@st.cache_resource
def get_api_client():
    try:
        client = MetalsLiveClient()
        # Test connection
        test_data = client.get_spot_prices()
        if test_data:
            return client
    except Exception as e:
        st.warning(f"Could not connect to Metals.live API: {e}")
    return MockMetalsClient()

api_client = get_api_client()
db = st.session_state.db

# Sidebar controls
st.sidebar.header("🔧 Controls")

col1, col2 = st.sidebar.columns(2)
with col1:
    refresh_btn = st.button("🔄 Refresh Prices", use_container_width=True)
with col2:
    auto_refresh = st.checkbox("Auto-refresh", value=False)

# Metal selection
selected_metals = st.sidebar.multiselect(
    "Select metals to track:",
    list(METALS.keys()),
    default=list(METALS.keys())[:3]
)

# Time range for charts
chart_days = st.sidebar.slider(
    "Days of history to display:",
    min_value=1,
    max_value=90,
    value=CHART_DAYS
)

st.sidebar.divider()
st.sidebar.info("📊 This app tracks metal prices from Metals.live and caches historical data.")

# Main content
# Refresh prices if button clicked or auto-refresh enabled
if refresh_btn or (auto_refresh and time.time() - (st.session_state.last_update or 0) > PRICE_UPDATE_INTERVAL):
    with st.spinner("Updating prices..."):
        prices = api_client.get_all_prices()
        if prices:
            db.insert_batch_prices(prices)
            st.session_state.last_update = time.time()
            st.success("✅ Prices updated!")

# Display current prices
st.header("📈 Current Prices")

latest_prices = db.get_latest_prices()

if latest_prices:
    # Create columns for price cards
    cols = st.columns(min(3, len(selected_metals)))
    
    for idx, metal in enumerate(selected_metals):
        if metal in latest_prices:
            price_info = latest_prices[metal]
            with cols[idx % len(cols)]:
                st.metric(
                    label=metal,
                    value=f"${price_info['price']:.2f}",
                    delta=f"Updated: {price_info['timestamp'][-8:]}"
                )
else:
    st.info("No price data available yet. Click 'Refresh Prices' to fetch the latest data.")

st.divider()

# Price history charts
st.header("📊 Price History")

if selected_metals:
    # Create tabs for each metal
    tabs = st.tabs(selected_metals)
    
    for tab, metal in zip(tabs, selected_metals):
        with tab:
            # Get history data
            history = db.get_price_history(metal, days=chart_days)
            
            if history:
                # Convert to DataFrame
                df = pd.DataFrame(history)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                
                # Create interactive Plotly chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['price'],
                    mode='lines+markers',
                    name=metal,
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=4),
                    fill='tozeroy',
                    fillcolor='rgba(31, 119, 180, 0.2)'
                ))
                
                # Calculate stats
                min_price = df['price'].min()
                max_price = df['price'].max()
                avg_price = df['price'].mean()
                latest_price = df['price'].iloc[-1]
                price_change = latest_price - df['price'].iloc[0]
                price_change_pct = (price_change / df['price'].iloc[0]) * 100 if df['price'].iloc[0] > 0 else 0
                
                fig.update_layout(
                    title=f"{metal} Price Trend ({chart_days} days)",
                    xaxis_title="Date",
                    yaxis_title=f"Price ({CURRENCY})",
                    hovermode='x unified',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Current", f"${latest_price:.2f}")
                with col2:
                    st.metric("Min (30d)", f"${min_price:.2f}")
                with col3:
                    st.metric("Max (30d)", f"${max_price:.2f}")
                with col4:
                    st.metric("Average", f"${avg_price:.2f}")
                with col5:
                    st.metric(
                        "Change",
                        f"${price_change:.2f}",
                        f"{price_change_pct:+.2f}%"
                    )
            else:
                st.info(f"No history available for {metal} yet. Refresh prices first.")
else:
    st.warning("Please select at least one metal from the sidebar.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85em;'>
    <p>📊 Metal Prices Tracker | Data from Metals.live API | Updated regularly</p>
    <p><small>Prices are in USD | Historical data cached locally</small></p>
</div>
""", unsafe_allow_html=True)
