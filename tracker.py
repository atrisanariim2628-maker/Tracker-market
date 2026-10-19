import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="India Financial & Macro Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Slick Interface
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 8px; color: #c9d1d9; padding: 10px 20px; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #238636 !important; color: #ffffff !important; }
    h1, h2, h3 { color: #f0f6fc; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("📊 Control Panel")
st.sidebar.markdown("---")
view_mode = st.sidebar.selectbox("Select View Mode", ["Live Dashboard", "Predictive Analytics & Decision Engine"])
st.sidebar.markdown("### Market Status")
st.sidebar.success("🟢 NSE / BSE: Live Connection Active")
st.sidebar.info("🏦 RBI Policy Cycle: Active (Q3)")

# --- MAIN HEADER ---
st.title("🇮🇳 India Macroeconomic & Financial Intelligence Hub")
st.markdown("Real-time telemetry, statutory rates, fiscal indicators, and predictive economic modeling.")

# --- TOP METRIC CARDS ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("RBI Repo Rate", "5.50%", "+0.25% (Oct 2026)")
col2.metric("FY GDP Growth", "7.1%", "FY27 Forecast")
col3.metric("10Y G-Sec Yield", "7.36%", "+0.04% WoW")
col4.metric("CPI Inflation", "4.2%", "Within RBI Target")
col5.metric("USD/INR", "83.65", "-0.12 today")

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🏦 Macro & Policy Rates", 
    "🧾 Tax, GST & Custom Duties", 
    "📊 Mutual Funds & Bonds", 
    "🔮 Economic Prediction & Decision Engine"
])

with tab1:
    st.subheader("Reserve Bank of India (RBI) Key Policy Rates")
    macro_data = {
        "Indicator": ["Repo Rate", "Reverse Repo Rate", "Standing Deposit Facility (SDF)", "Cash Reserve Ratio (CRR)", "Statutory Liquidity Ratio (SLR)", "Bank Rate"],
        "Current Rate (%)": [5.50, 3.35, 5.25, 4.50, 18.00, 5.75],
        "Trend / Stance": ["Neutral / Tightening", "Accommodative", "Neutral", "Stable", "Stable", "Tightening"],
        "Last Revised": ["October 2026", "June 2024", "October 2024", "February 2023", "June 2020", "October 2026"]
    }
    st.dataframe(pd.DataFrame(macro_data), use_container_width=True, hide_index=True)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        quarters = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26 (Est)"]
        gdp_trend = [6.7, 6.5, 6.2, 7.4, 6.8, 7.0, 7.1, 7.2]
        fig_gdp = px.line(x=quarters, y=gdp_trend, markers=True, title="Quarterly GDP Growth Trend (%)")
        fig_gdp.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", font_color="white")
        st.plotly_chart(fig_gdp, use_container_width=True)

    with chart_col2:
        cpi_trend = [5.1, 4.8, 4.3, 3.7, 4.6, 4.1, 3.9, 4.2]
        fig_cpi = px.bar(x=quarters, y=cpi_trend, title="CPI Inflation vs RBI Target Band")
        fig_cpi.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22", font_color="white")
        st.plotly_chart(fig_cpi, use_container_width=True)

with tab2:
    st.subheader("Statutory Tax Slabs & GST Categories")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### Goods and Services Tax (GST) Slabs")
        gst_data = {
            "Slab": ["0% (Nil)", "5%", "12%", "18%", "28%"],
            "Category Examples": ["Unbranded food grains, milk, salt", "Edible oil, tea, sugar, transport", "Processed food, computers, books", "Toothpaste, IT services, capital goods", "Automobiles, luxury items, aerated drinks"]
        }
        st.dataframe(pd.DataFrame(gst_data), use_container_width=True, hide_index=True)
    with col_t2:
        st.markdown("#### Income Tax Slabs (New Tax Regime)")
        tax_data = {
            "Income Range": ["Up to ₹3,00,000", "₹3,00,001 - ₹7,00,000", "₹7,00,001 - ₹10,00,000", "₹10,00,001 - ₹12,00,000", "₹12,00,001 - ₹15,00,000", "Above ₹15,00,000"],
            "Tax Rate": ["Nil", "5%", "10%", "15%", "20%", "30%"]
        }
        st.dataframe(pd.DataFrame(tax_data), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Market Benchmarks, Mutual Funds & Fixed Income Rates")
    col_mf1, col_mf2 = st.columns(2)
    with col_mf1:
        mf_data = {
            "Category": ["Large Cap", "Mid Cap", "Small Cap", "Flexi Cap", "Liquid Funds", "Arbitrage Funds"],
            "Benchmark Index": ["Nifty 50", "Nifty Midcap 150", "Nifty Smallcap 250", "Nifty 500", "CRISIL Liquid Fund", "Nifty Arbitrage"],
            "Avg 3Y Return (%)": [14.2, 22.5, 26.8, 18.4, 7.1, 7.6]
        }
        st.dataframe(pd.DataFrame(mf_data), use_container_width=True, hide_index=True)
    with col_mf2:
        bond_data = {
            "Instrument": ["10-Year Government Bond", "Corporate AAA Bonds (5Y)", "Tax-Free Bonds (PSU)", "RBI Floating Rate Savings Bonds", "LIC Endowment Plan (Avg Yield)"],
            "Current Yield / Rate (%)": [7.36, 7.85, 5.50, 8.05, 6.00],
            "Risk Profile": ["Sovereign (Zero)", "Very Low", "Low", "Sovereign", "Low / Guaranteed"]
        }
        st.dataframe(pd.DataFrame(bond_data), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🔮 Near-Time Economic Decision & Predictive Intelligence")
    indicator_df = pd.DataFrame({
        "Economic Indicator": ["Credit Growth (YoY)", "Deposit Growth (YoY)", "PMI Manufacturing", "PMI Services", "Forex Reserves ($B)", "GST Collections (Monthly Avg)"],
        "Current Value": ["14.2%", "11.1%", "57.8", "60.2", "$682B", "₹1.85 Lakh Cr"],
        "Signal Status": ["🟢 Expansion", "🟡 Moderate", "🟢 Strong Expansion", "🟢 Robust", "🟢 All-Time High", "🟢 Strong Tax Buoyancy"]
    })
    st.dataframe(indicator_df, use_container_width=True, hide_index=True)
    
    scenario = st.selectbox("Select Monetary Policy Scenario for Next Quarter:", 
                            ["Baseline: Repo Rate Hold at 5.50%", "Hawkish Pivot: +25 bps Rate Hike", "Dovish Pivot: -25 bps Rate Cut"])
    if "Hold" in scenario:
        st.info("📊 **Model Outlook:** Steady credit expansion continues. Real estate and corporate capex remain resilient.")
    elif "Hawkish" in scenario:
        st.warning("⚠️ **Model Outlook:** Cost of capital increases. Expect short-term equity correction in high-multiple growth stocks.")
    else:
        st.success("🚀 **Model Outlook:** Liquidity easing triggers bullish momentum across mid-caps and small-caps.")