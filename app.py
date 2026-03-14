import streamlit as st
import sys
import os

# Ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_db
from modules.data_loader import load_all_procurement_data
from modules.pdf_parser import load_all_meter_data

st.set_page_config(
    page_title="ZERA Analytics Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ── Global dark-mode fix: make all text visible ── */
[data-testid="stAppViewContainer"] {
    color: #E0E0E0;
}

/* ── Header styling ── */
.main-header {
    font-size: 2.2rem;
    font-weight: 700;
    color: #E0E0E0;
    margin-bottom: 0.2rem;
}
.sub-header {
    font-size: 1.1rem;
    color: #9CA3AF;
    margin-bottom: 1.5rem;
}

/* ── KPI Card Styling ── */
.kpi-container {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.kpi-card {
    flex: 1;
    min-width: 160px;
    padding: 20px 16px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
}

.kpi-card .kpi-icon {
    font-size: 22px;
    margin-bottom: 6px;
}

.kpi-card .kpi-label {
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
    opacity: 0.85;
}

.kpi-card .kpi-value {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    word-break: break-all;
    line-height: 1.2;
}

.kpi-card .kpi-sub {
    font-size: 11px;
    margin-top: 4px;
    opacity: 0.6;
}

/* Card color themes */
.kpi-teal    { background: linear-gradient(135deg, #0d3b3e 0%, #14555a 100%); color: #5eead4; }
.kpi-teal    .kpi-value { color: #5eead4; }
.kpi-teal    .kpi-label { color: #99f6e4; }

.kpi-blue    { background: linear-gradient(135deg, #0c2d48 0%, #145374 100%); color: #7dd3fc; }
.kpi-blue    .kpi-value { color: #7dd3fc; }
.kpi-blue    .kpi-label { color: #bae6fd; }

.kpi-purple  { background: linear-gradient(135deg, #2d1b4e 0%, #44277a 100%); color: #c4b5fd; }
.kpi-purple  .kpi-value { color: #c4b5fd; }
.kpi-purple  .kpi-label { color: #ddd6fe; }

.kpi-amber   { background: linear-gradient(135deg, #3b2507 0%, #6b4410 100%); color: #fcd34d; }
.kpi-amber   .kpi-value { color: #fcd34d; }
.kpi-amber   .kpi-label { color: #fde68a; }

.kpi-rose    { background: linear-gradient(135deg, #3b0d1a 0%, #6b1530 100%); color: #fda4af; }
.kpi-rose    .kpi-value { color: #fda4af; }
.kpi-rose    .kpi-label { color: #fecdd3; }

/* ── Fix default metric overflow ── */
[data-testid="stMetric"] {
    overflow: visible !important;
    white-space: normal !important;
}

[data-testid="stMetricValue"] {
    font-size: 20px !important;
    overflow: visible !important;
    white-space: normal !important;
    word-break: break-all !important;
    color: #E0E0E0 !important;
}

[data-testid="stMetricLabel"] {
    color: #A0A0A0 !important;
}

/* ── Fix containers blending in dark mode ── */
[data-testid="stVerticalBlock"] > div:has(> [data-testid="stMetric"]) {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 12px;
}

/* ── Plotly charts: ensure visible in dark mode ── */
.stPlotlyChart {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 8px;
}

/* ── Sidebar contrast fix ── */
[data-testid="stSidebar"] {
    background: #0e1117;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* ── Tab labels visible ── */
.stTabs [data-baseweb="tab"] {
    color: #A0A0A0 !important;
}
.stTabs [aria-selected="true"] {
    color: #5eead4 !important;
}

/* ── Tables readable ── */
.stDataFrame {
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
}

/* ── Navigation cards ── */
.nav-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading procurement data...")
def init_procurement():
    return load_all_procurement_data()


@st.cache_data(show_spinner="Parsing meter PDFs...")
def init_meter():
    return load_all_meter_data()


def render_kpi_cards(proc_kpis, meter_kpis):
    total_spend = proc_kpis.get('grand_total_spend', 0)
    if total_spend >= 1_00_00_000:
        spend_display = f"₹{total_spend / 1_00_00_000:.2f} Cr"
        spend_sub = f"₹{total_spend:,.0f}"
    elif total_spend >= 1_00_000:
        spend_display = f"₹{total_spend / 1_00_000:.2f} L"
        spend_sub = f"₹{total_spend:,.0f}"
    else:
        spend_display = f"₹{total_spend:,.0f}"
        spend_sub = ""

    line_items = proc_kpis.get('total_line_items', 0)
    meters_tested = meter_kpis.get('total_meters_tested', 0)
    pass_rate = meter_kpis.get('pass_rate', 0)
    voltage_events = meter_kpis.get('total_voltage_events', 0)

    passed_count = int(meters_tested * pass_rate / 100) if meters_tested > 0 else 0

    cards_html = f"""
    <div class="kpi-container">
        <div class="kpi-card kpi-teal">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Spend</div>
            <div class="kpi-value">{spend_display}</div>
            <div class="kpi-sub">{spend_sub}</div>
        </div>
        <div class="kpi-card kpi-blue">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Line Items</div>
            <div class="kpi-value">{line_items:,}</div>
            <div class="kpi-sub">across 4 categories</div>
        </div>
        <div class="kpi-card kpi-purple">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-label">Meters Tested</div>
            <div class="kpi-value">{meters_tested}</div>
            <div class="kpi-sub">Session S-14</div>
        </div>
        <div class="kpi-card kpi-amber">
            <div class="kpi-icon">✅</div>
            <div class="kpi-label">Pass Rate</div>
            <div class="kpi-value">{pass_rate:.0f}%</div>
            <div class="kpi-sub">{passed_count} of {meters_tested} passed</div>
        </div>
        <div class="kpi-card kpi-rose">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">Voltage Events</div>
            <div class="kpi-value">{voltage_events}</div>
            <div class="kpi-sub">from PDF extraction</div>
        </div>
    </div>
    """
    st.markdown(cards_html, unsafe_allow_html=True)


def main():
    # Sidebar
    st.sidebar.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=60)
    st.sidebar.markdown("### ⚡ ZERA Analytics")
    st.sidebar.markdown("*Intelligence Platform*")
    st.sidebar.divider()

    # Initialize data
    with st.spinner("Initializing database..."):
        init_db()
        proc_results = init_procurement()
        meter_results = init_meter()

    st.sidebar.success("Data loaded successfully!")
    st.sidebar.markdown("**Data Sources:**")
    for table, count in {**proc_results, **meter_results}.items():
        st.sidebar.caption(f"📊 {table}: {count} records")

    # Main page content
    st.markdown('<p class="main-header">⚡ ZERA Analytics Intelligence Platform</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Procurement Intelligence & Smart Meter Analytics for ZERA India Pvt. Ltd., Gandhinagar</p>', unsafe_allow_html=True)

    # Quick KPIs
    from modules.analytics import get_procurement_summary, get_meter_summary
    proc_kpis = get_procurement_summary()
    meter_kpis = get_meter_summary()

    st.markdown("### 📈 Executive Overview")
    render_kpi_cards(proc_kpis, meter_kpis)

    st.divider()

    # Navigation cards
    st.markdown("### 🗂️ Navigate to Modules")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("#### 📊 Dashboard")
        st.caption("KPIs, spend overview, trend charts")
        st.page_link("pages/1_Dashboard.py", label="Open Dashboard →")
    with c2:
        st.markdown("#### 📦 Procurement")
        st.caption("Supplier analysis, cost breakdowns")
        st.page_link("pages/2_Procurement.py", label="Open Procurement →")
    with c3:
        st.markdown("#### ⚡ Meter Analytics")
        st.caption("Voltage events, meter health, anomaly detection")
        st.page_link("pages/3_Meter_Analytics.py", label="Open Meter Analytics →")
    with c4:
        st.markdown("#### 🤖 AI Insights")
        st.caption("ML predictions, risk scoring, forecasting")
        st.page_link("pages/4_AI_Insights.py", label="Open AI Insights →")

    st.divider()
    st.caption("Built by Vishvam | ZERA India Pvt. Ltd. Internship 2025-26 | Powered by Python, Streamlit, scikit-learn")


if __name__ == "__main__":
    main()