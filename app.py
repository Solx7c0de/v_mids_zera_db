import streamlit as st
import sys
import os

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
/* ══════════════════════════════════════════
   ZERA ANALYTICS — THEME-NEUTRAL STYLING
   All cards use dark backgrounds with light
   text so they look identical in both modes.
   Sidebar and page text left untouched so
   Streamlit's native theme handles them.
   ══════════════════════════════════════════ */

/* ── Hero ── */
.hero-wrap {
    padding: 20px 0 4px 0;
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 6px 0;
    color: #0ea5e9;
}

.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    margin: 0 0 4px 0;
}

/* ── Section dividers ── */
.section-head {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    color: #64748b;
    margin: 24px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
}

/* ── KPI Cards: always dark bg + light text ── */
.kpi-row {
    display: flex;
    gap: 14px;
    margin: 8px 0 24px 0;
    flex-wrap: wrap;
}

.kpi-card {
    flex: 1;
    min-width: 150px;
    padding: 20px 14px 16px 14px;
    border-radius: 14px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}

.kpi-icon  { font-size: 26px; margin-bottom: 6px; }
.kpi-label { font-size: 11px; font-weight: 600; text-transform: uppercase;
             letter-spacing: 1px; margin-bottom: 6px; }
.kpi-value { font-size: 26px; font-weight: 800; line-height: 1.15;
             letter-spacing: -0.3px; }
.kpi-sub   { font-size: 11px; margin-top: 5px; opacity: 0.7; }

/* Card 1: Spend — emerald */
.kpi-spend {
    background: #064e3b; border: 1px solid #059669;
}
.kpi-spend::before { background: #10b981; }
.kpi-spend .kpi-label { color: #a7f3d0; }
.kpi-spend .kpi-value { color: #6ee7b7; }
.kpi-spend .kpi-sub   { color: #a7f3d0; }
.kpi-spend .kpi-icon  { filter: none; }

/* Card 2: Items — slate blue */
.kpi-items {
    background: #1e3a5f; border: 1px solid #2563eb;
}
.kpi-items::before { background: #3b82f6; }
.kpi-items .kpi-label { color: #bfdbfe; }
.kpi-items .kpi-value { color: #93c5fd; }
.kpi-items .kpi-sub   { color: #bfdbfe; }

/* Card 3: Meters — deep purple */
.kpi-meters {
    background: #3b0764; border: 1px solid #7c3aed;
}
.kpi-meters::before { background: #a855f7; }
.kpi-meters .kpi-label { color: #e9d5ff; }
.kpi-meters .kpi-value { color: #d8b4fe; }
.kpi-meters .kpi-sub   { color: #e9d5ff; }

/* Card 4: Pass — amber */
.kpi-pass {
    background: #78350f; border: 1px solid #d97706;
}
.kpi-pass::before { background: #f59e0b; }
.kpi-pass .kpi-label { color: #fde68a; }
.kpi-pass .kpi-value { color: #fcd34d; }
.kpi-pass .kpi-sub   { color: #fde68a; }

/* Card 5: Events — rose */
.kpi-events {
    background: #7f1d1d; border: 1px solid #dc2626;
}
.kpi-events::before { background: #ef4444; }
.kpi-events .kpi-label { color: #fecaca; }
.kpi-events .kpi-value { color: #fca5a5; }
.kpi-events .kpi-sub   { color: #fecaca; }

/* ── Navigation Grid ── */
.nav-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 8px 0 12px 0;
}

@media (max-width: 768px) {
    .nav-grid { grid-template-columns: repeat(2, 1fr); }
    .kpi-row  { gap: 10px; }
}

.nav-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 22px 16px;
    text-align: center;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.nav-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    border-color: #0ea5e9;
}

.nav-icon  { font-size: 34px; margin-bottom: 10px; }
.nav-title { font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
.nav-desc  { font-size: 11.5px; color: #94a3b8; line-height: 1.5; }

/* ── Footer ── */
.zera-footer {
    text-align: center;
    font-size: 12px;
    color: #94a3b8;
    padding: 16px 0 4px 0;
    margin-top: 28px;
    border-top: 1px solid #e2e8f0;
}

/* ── Plotly / table polish ── */
.stPlotlyChart {
    border-radius: 10px;
}

.stDataFrame {
    border-radius: 8px;
}

/* ── Fix st.metric overflow (for subpages) ── */
[data-testid="stMetricValue"] {
    font-size: 20px !important;
    overflow: visible !important;
    white-space: normal !important;
    word-break: break-all !important;
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

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card kpi-spend">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Spend</div>
            <div class="kpi-value">{spend_display}</div>
            <div class="kpi-sub">{spend_sub}</div>
        </div>
        <div class="kpi-card kpi-items">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Line Items</div>
            <div class="kpi-value">{line_items:,}</div>
            <div class="kpi-sub">across 4 categories</div>
        </div>
        <div class="kpi-card kpi-meters">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-label">Meters Tested</div>
            <div class="kpi-value">{meters_tested}</div>
            <div class="kpi-sub">Session S-14</div>
        </div>
        <div class="kpi-card kpi-pass">
            <div class="kpi-icon">✅</div>
            <div class="kpi-label">Pass Rate</div>
            <div class="kpi-value">{pass_rate:.0f}%</div>
            <div class="kpi-sub">{passed_count} of {meters_tested} passed</div>
        </div>
        <div class="kpi-card kpi-events">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">Voltage Events</div>
            <div class="kpi-value">{voltage_events}</div>
            <div class="kpi-sub">parsed from PDF</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_nav_section():
    st.markdown("""
    <div class="nav-grid">
        <div class="nav-card">
            <div class="nav-icon">📊</div>
            <div class="nav-title">Dashboard</div>
            <div class="nav-desc">KPIs, spend overview, and trend charts</div>
        </div>
        <div class="nav-card">
            <div class="nav-icon">📦</div>
            <div class="nav-title">Procurement</div>
            <div class="nav-desc">Supplier analysis, cost breakdowns, GST</div>
        </div>
        <div class="nav-card">
            <div class="nav-icon">⚡</div>
            <div class="nav-title">Meter Analytics</div>
            <div class="nav-desc">Voltage events, accuracy, power profiles</div>
        </div>
        <div class="nav-card">
            <div class="nav-icon">🤖</div>
            <div class="nav-title">AI Insights</div>
            <div class="nav-desc">Risk scoring, clustering, forecasting</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.page_link("pages/1_Dashboard.py", label="Open Dashboard →", icon="📊")
    with c2:
        st.page_link("pages/2_Procurement.py", label="Open Procurement →", icon="📦")
    with c3:
        st.page_link("pages/3_Meter_Analytics.py", label="Open Meter Analytics →", icon="⚡")
    with c4:
        st.page_link("pages/4_AI_Insights.py", label="Open AI Insights →", icon="🤖")


def main():
    # ── Sidebar (no custom CSS — uses Streamlit native colors) ──
    st.sidebar.markdown("## ⚡ ZERA Analytics")
    st.sidebar.markdown("**Intelligence Platform**")
    st.sidebar.caption("Procurement & Smart Meter Analytics")
    st.sidebar.divider()

    with st.spinner("Initializing database..."):
        init_db()
        proc_results = init_procurement()
        meter_results = init_meter()

    st.sidebar.success("✅ Data loaded")
    st.sidebar.divider()
    st.sidebar.markdown("**Loaded Tables**")
    for table, count in {**proc_results, **meter_results}.items():
        st.sidebar.caption(f"📊 {table}: **{count}** records")
    st.sidebar.divider()
    st.sidebar.caption("ZERA India Pvt. Ltd., Gandhinagar")
    st.sidebar.caption("Internship 2025–26 | Vishvam Chaudhari")

    # ── Hero Header ──
    st.markdown("""
        <div class="hero-wrap">
            <p class="hero-title">⚡ ZERA Analytics Intelligence Platform</p>
            <p class="hero-sub">Procurement Intelligence & Smart Meter Analytics for ZERA India Pvt. Ltd., Gandhinagar</p>
        </div>
    """, unsafe_allow_html=True)

    # ── KPI Section ──
    from modules.analytics import get_procurement_summary, get_meter_summary
    proc_kpis = get_procurement_summary()
    meter_kpis = get_meter_summary()

    st.markdown('<div class="section-head">Executive Overview</div>', unsafe_allow_html=True)
    render_kpi_cards(proc_kpis, meter_kpis)

    # ── Navigation Section ──
    st.markdown('<div class="section-head">Navigate to Modules</div>', unsafe_allow_html=True)
    render_nav_section()

    # ── Footer ──
    st.markdown("""
        <div class="zera-footer">
            Built by Vishvam Chaudhari · ZERA India Pvt. Ltd. Internship 2025–26 · Python, Streamlit & scikit-learn
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
import streamlit as st
import sys
import os

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
/* ══════════════════════════════════════════
   ZERA ANALYTICS — THEME-NEUTRAL STYLING
   All cards use dark backgrounds with light
   text so they look identical in both modes.
   Sidebar and page text left untouched so
   Streamlit's native theme handles them.
   ══════════════════════════════════════════ */

/* ── Hero ── */
.hero-wrap {
    padding: 20px 0 4px 0;
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 6px 0;
    color: #0ea5e9;
}

.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    margin: 0 0 4px 0;
}

/* ── Section dividers ── */
.section-head {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    color: #64748b;
    margin: 24px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
}

/* ── KPI Cards: always dark bg + light text ── */
.kpi-row {
    display: flex;
    gap: 14px;
    margin: 8px 0 24px 0;
    flex-wrap: wrap;
}

.kpi-card {
    flex: 1;
    min-width: 150px;
    padding: 20px 14px 16px 14px;
    border-radius: 14px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}

.kpi-icon  { font-size: 26px; margin-bottom: 6px; }
.kpi-label { font-size: 11px; font-weight: 600; text-transform: uppercase;
             letter-spacing: 1px; margin-bottom: 6px; }
.kpi-value { font-size: 26px; font-weight: 800; line-height: 1.15;
             letter-spacing: -0.3px; }
.kpi-sub   { font-size: 11px; margin-top: 5px; opacity: 0.7; }

/* Card 1: Spend — emerald */
.kpi-spend {
    background: #064e3b; border: 1px solid #059669;
}
.kpi-spend::before { background: #10b981; }
.kpi-spend .kpi-label { color: #a7f3d0; }
.kpi-spend .kpi-value { color: #6ee7b7; }
.kpi-spend .kpi-sub   { color: #a7f3d0; }
.kpi-spend .kpi-icon  { filter: none; }

/* Card 2: Items — slate blue */
.kpi-items {
    background: #1e3a5f; border: 1px solid #2563eb;
}
.kpi-items::before { background: #3b82f6; }
.kpi-items .kpi-label { color: #bfdbfe; }
.kpi-items .kpi-value { color: #93c5fd; }
.kpi-items .kpi-sub   { color: #bfdbfe; }

/* Card 3: Meters — deep purple */
.kpi-meters {
    background: #3b0764; border: 1px solid #7c3aed;
}
.kpi-meters::before { background: #a855f7; }
.kpi-meters .kpi-label { color: #e9d5ff; }
.kpi-meters .kpi-value { color: #d8b4fe; }
.kpi-meters .kpi-sub   { color: #e9d5ff; }

/* Card 4: Pass — amber */
.kpi-pass {
    background: #78350f; border: 1px solid #d97706;
}
.kpi-pass::before { background: #f59e0b; }
.kpi-pass .kpi-label { color: #fde68a; }
.kpi-pass .kpi-value { color: #fcd34d; }
.kpi-pass .kpi-sub   { color: #fde68a; }

/* Card 5: Events — rose */
.kpi-events {
    background: #7f1d1d; border: 1px solid #dc2626;
}
.kpi-events::before { background: #ef4444; }
.kpi-events .kpi-label { color: #fecaca; }
.kpi-events .kpi-value { color: #fca5a5; }
.kpi-events .kpi-sub   { color: #fecaca; }

/* ── Navigation Grid ── */
.nav-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 8px 0 12px 0;
}

@media (max-width: 768px) {
    .nav-grid { grid-template-columns: repeat(2, 1fr); }
    .kpi-row  { gap: 10px; }
}

.nav-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 22px 16px;
    text-align: center;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.nav-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    border-color: #0ea5e9;
}

.nav-icon  { font-size: 34px; margin-bottom: 10px; }
.nav-title { font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
.nav-desc  { font-size: 11.5px; color: #94a3b8; line-height: 1.5; }

/* ── Footer ── */
.zera-footer {
    text-align: center;
    font-size: 12px;
    color: #94a3b8;
    padding: 16px 0 4px 0;
    margin-top: 28px;
    border-top: 1px solid #e2e8f0;
}

/* ── Plotly / table polish ── */
.stPlotlyChart {
    border-radius: 10px;
}

.stDataFrame {
    border-radius: 8px;
}

/* ── Fix st.metric overflow (for subpages) ── */
[data-testid="stMetricValue"] {
    font-size: 20px !important;
    overflow: visible !important;
    white-space: normal !important;
    word-break: break-all !important;
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

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card kpi-spend">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Spend</div>
            <div class="kpi-value">{spend_display}</div>
            <div class="kpi-sub">{spend_sub}</div>
        </div>
        <div class="kpi-card kpi-items">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Line Items</div>
            <div class="kpi-value">{line_items:,}</div>
            <div class="kpi-sub">across 4 categories</div>
        </div>
        <div class="kpi-card kpi-meters">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-label">Meters Tested</div>
            <div class="kpi-value">{meters_tested}</div>
            <div class="kpi-sub">Session S-14</div>
        </div>
        <div class="kpi-card kpi-pass">
            <div class="kpi-icon">✅</div>
            <div class="kpi-label">Pass Rate</div>
            <div class="kpi-value">{pass_rate:.0f}%</div>
            <div class="kpi-sub">{passed_count} of {meters_tested} passed</div>
        </div>
        <div class="kpi-card kpi-events">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">Voltage Events</div>
            <div class="kpi-value">{voltage_events}</div>
            <div class="kpi-sub">parsed from PDF</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_nav_section():
    st.markdown("""
    <div class="nav-grid">
        <div class="nav-card">
            <div class="nav-icon">📊</div>
            <div class="nav-title">Dashboard</div>
            <div class="nav-desc">KPIs, spend overview, and trend charts</div>
        </div>
        <div class="nav-card">
            <div class="nav-icon">📦</div>
            <div class="nav-title">Procurement</div>
            <div class="nav-desc">Supplier analysis, cost breakdowns, GST</div>
        </div>
        <div class="nav-card">
            <div class="nav-icon">⚡</div>
            <div class="nav-title">Meter Analytics</div>
            <div class="nav-desc">Voltage events, accuracy, power profiles</div>
        </div>
        <div class="nav-card">
            <div class="nav-icon">🤖</div>
            <div class="nav-title">AI Insights</div>
            <div class="nav-desc">Risk scoring, clustering, forecasting</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.page_link("pages/1_Dashboard.py", label="Open Dashboard →", icon="📊")
    with c2:
        st.page_link("pages/2_Procurement.py", label="Open Procurement →", icon="📦")
    with c3:
        st.page_link("pages/3_Meter_Analytics.py", label="Open Meter Analytics →", icon="⚡")
    with c4:
        st.page_link("pages/4_AI_Insights.py", label="Open AI Insights →", icon="🤖")


def main():
    # ── Sidebar (no custom CSS — uses Streamlit native colors) ──
    st.sidebar.markdown("## ⚡ ZERA Analytics")
    st.sidebar.markdown("**Intelligence Platform**")
    st.sidebar.caption("Procurement & Smart Meter Analytics")
    st.sidebar.divider()

    with st.spinner("Initializing database..."):
        init_db()
        proc_results = init_procurement()
        meter_results = init_meter()

    st.sidebar.success("✅ Data loaded")
    st.sidebar.divider()
    st.sidebar.markdown("**Loaded Tables**")
    for table, count in {**proc_results, **meter_results}.items():
        st.sidebar.caption(f"📊 {table}: **{count}** records")
    st.sidebar.divider()
    st.sidebar.caption("ZERA India Pvt. Ltd., Gandhinagar")
    st.sidebar.caption("Internship 2025–26 | Vishvam Chaudhari")

    # ── Hero Header ──
    st.markdown("""
        <div class="hero-wrap">
            <p class="hero-title">⚡ ZERA Analytics Intelligence Platform</p>
            <p class="hero-sub">Procurement Intelligence & Smart Meter Analytics for ZERA India Pvt. Ltd., Gandhinagar</p>
        </div>
    """, unsafe_allow_html=True)

    # ── KPI Section ──
    from modules.analytics import get_procurement_summary, get_meter_summary
    proc_kpis = get_procurement_summary()
    meter_kpis = get_meter_summary()

    st.markdown('<div class="section-head">Executive Overview</div>', unsafe_allow_html=True)
    render_kpi_cards(proc_kpis, meter_kpis)

    # ── Navigation Section ──
    st.markdown('<div class="section-head">Navigate to Modules</div>', unsafe_allow_html=True)
    render_nav_section()

    # ── Footer ──
    st.markdown("""
        <div class="zera-footer">
            Built by Vishvam Chaudhari · ZERA India Pvt. Ltd. Internship 2025–26 · Python, Streamlit & scikit-learn
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
