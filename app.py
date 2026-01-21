import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
from plotly.subplots import make_subplots

# =============================================
# KONFIGURASI HALAMAN & STYLING
# =============================================
st.set_page_config(
    page_title="Dashboard Monitoring Proyek - Office Supplies",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS - POWER BI STYLE
# =============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .header-banner h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-banner p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .kpi-card.blue { border-left-color: #3b82f6; }
    .kpi-card.green { border-left-color: #10b981; }
    .kpi-card.yellow { border-left-color: #f59e0b; }
    .kpi-card.red { border-left-color: #ef4444; }
    .kpi-card.purple { border-left-color: #8b5cf6; }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    
    .kpi-delta.positive {
        background: #d1fae5;
        color: #065f46;
    }
    
    .kpi-delta.negative {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .kpi-delta.neutral {
        background: #e0e7ff;
        color: #3730a3;
    }
    
    /* Section Header */
    .section-header {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .section-header h2 {
        margin: 0;
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Data Table Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Progress Bar Custom */
    .custom-progress {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .progress-bar {
        height: 25px;
        background: #e2e8f0;
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 15px;
        transition: width 0.6s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 10px;
        color: white;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Alert Styling */
    .alert-card {
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .alert-card:hover {
        transform: translateX(5px);
    }
    
    .alert-card.error {
        background: #fee2e2;
        border-left-color: #dc2626;
        color: #991b1b;
    }
    
    .alert-card.warning {
        background: #fef3c7;
        border-left-color: #f59e0b;
        color: #92400e;
    }
    
    .alert-card.success {
        background: #d1fae5;
        border-left-color: #10b981;
        color: #065f46;
    }
    
    .alert-card.info {
        background: #dbeafe;
        border-left-color: #3b82f6;
        color: #1e40af;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #64748b;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e2e8f0;
        color: #3b82f6;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white !important;
    }
    
    /* Metric Badge */
    .metric-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    
    .badge-success { background: #d1fae5; color: #065f46; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .badge-danger { background: #fee2e2; color: #991b1b; }
    .badge-info { background: #dbeafe; color: #1e40af; }
    
    /* Filter Panel */
    .filter-panel {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Footer */
    .footer {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.05);
        color: #64748b;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .kpi-value { font-size: 2rem; }
        .header-banner h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# KONFIGURASI DATA (sama seperti sebelumnya)
# =============================================
LOG_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEpBx0Eg1x3unaxVVQWJVFfzmH9Z8qKQPevp87cnsfP-nhyNYfhQvVc3Vpd0sDfkNRaNs7R4VH1nOa/pub?gid=1285157492&single=true&output=csv"

PROJECT_START = date(2025, 11, 10)

BASELINE = [
    {"document": "Project Charter", "phase": "Inisiasi", "pic_role": "PM", "target_week": 1},
    {"document": "Gantt Chart / Schedule", "phase": "Perencanaan", "pic_role": "PM", "target_week": 2},
    {"document": "SRS", "phase": "Perencanaan", "pic_role": "BA/SA", "target_week": 3},
    {"document": "Use Case Diagram + Deskripsi", "phase": "Perencanaan", "pic_role": "BA/SA", "target_week": 4},
    {"document": "ERD + Data Dictionary", "phase": "Perencanaan", "pic_role": "Backend/DB", "target_week": 5},
    {"document": "Wireframe / Mockup UI", "phase": "Perencanaan", "pic_role": "UI/UX", "target_week": 6},
    {"document": "Risk Register", "phase": "Controlling", "pic_role": "PM", "target_week": 6},
    {"document": "User Manual", "phase": "Penutupan", "pic_role": "BA/SA", "target_week": 11},
]

STATUS_ORDER = ["Belum", "Proses", "Selesai"]
STATUS_COLORS = {"Selesai": "#10b981", "Proses": "#f59e0b", "Belum": "#ef4444"}

# =============================================
# HELPER FUNCTIONS (sama seperti sebelumnya)
# =============================================
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    rename_map = {
        "week": "week_no",
        "mingguke": "week_no",
        "minggu_ke": "week_no",
        "doc": "document",
        "nama dokumen": "document",
        "fase": "phase",
        "pic": "pic_role",
        "role": "pic_role",
        "updatedby": "updated_by",
        "catatan": "notes",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df

@st.cache_data(ttl=60)
def load_log(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df = normalize_columns(df)
    required = {"timestamp", "week_no", "document", "status", "progress"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "week_start" in df.columns:
        df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce")
    df["week_no"] = pd.to_numeric(df["week_no"], errors="coerce")
    df["progress"] = pd.to_numeric(df["progress"], errors="coerce")
    df["status"] = df["status"].astype(str).str.strip().str.title()
    df.loc[~df["status"].isin(STATUS_ORDER), "status"] = "Proses"
    df["document"] = df["document"].astype(str).str.strip()
    return df.dropna(subset=["week_no", "document"])

def compute_current_week(project_start: date) -> int:
    today = date.today()
    delta_days = (today - project_start).days
    if delta_days < 0:
        return 1
    return min(12, max(1, delta_days // 7 + 1))

def get_latest_status(df_log: pd.DataFrame, df_baseline: pd.DataFrame) -> pd.DataFrame:
    if len(df_log) > 0:
        df_latest = (df_log.sort_values("timestamp", ascending=True)
                    .groupby("document", as_index=False).tail(1))
    else:
        df_latest = pd.DataFrame(columns=["document", "status", "progress"])
    
    df_result = df_baseline.copy()
    
    if len(df_latest) > 0:
        log_cols = ["document"]
        for col in ["status", "progress", "timestamp", "notes", "updated_by", "week_no"]:
            if col in df_latest.columns:
                log_cols.append(col)
        
        df_log_subset = df_latest[log_cols].copy()
        rename_dict = {col: f"{col}_log" for col in log_cols if col != "document"}
        df_log_subset = df_log_subset.rename(columns=rename_dict)
        
        df_result = df_result.merge(df_log_subset, on="document", how="left")
        
        df_result["status"] = df_result.get("status_log", "Belum").fillna("Belum")
        df_result["progress"] = df_result.get("progress_log", 0).fillna(0)
        
        if "timestamp_log" in df_result.columns:
            df_result["timestamp"] = df_result["timestamp_log"]
        if "notes_log" in df_result.columns:
            df_result["notes"] = df_result["notes_log"]
        if "updated_by_log" in df_result.columns:
            df_result["updated_by"] = df_result["updated_by_log"]
        if "week_no_log" in df_result.columns:
            df_result["last_update_week"] = df_result["week_no_log"]
        
        cols_to_drop = [c for c in df_result.columns if c.endswith("_log")]
        df_result = df_result.drop(columns=cols_to_drop, errors="ignore")
    else:
        df_result["status"] = "Belum"
        df_result["progress"] = 0
    
    return df_result

@st.cache_data
def load_tim():
    data = {
        'Role': ['PM', 'BA/SA', 'UI/UX', 'Backend/DB'],
        'Deskripsi': [
            'Project Manager - Penanggung jawab proyek',
            'Business/System Analyst - Analisis & dokumentasi',
            'UI/UX Designer - Desain antarmuka',
            'Backend/Database Engineer - Database & sistem'
        ],
        'Skill': [
            'Leadership, Planning, Risk Management',
            'Analysis, Documentation, Communication',
            'Figma, CSS, User Research',
            'Database, SQL, Python/Laravel'
        ],
        'Dokumen Ditangani': [
            'Project Charter, Gantt Chart, Risk Register',
            'SRS, Use Case, User Manual',
            'Wireframe / Mockup UI',
            'ERD + Data Dictionary'
        ]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_risiko():
    data = {
        'ID': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
        'Risiko': [
            'Requirement berubah-ubah',
            'Deadline tidak tercapai',
            'Skill tim kurang memadai',
            'Anggota tim berhalangan',
            'Server down saat demo',
            'Data/code hilang'
        ],
        'Probabilitas': ['Tinggi', 'Sedang', 'Sedang', 'Sedang', 'Rendah', 'Rendah'],
        'Dampak': ['Sedang', 'Tinggi', 'Tinggi', 'Sedang', 'Tinggi', 'Tinggi'],
        'Skor': [6, 6, 6, 4, 4, 4],
        'Strategi': ['Mitigasi', 'Mitigasi', 'Mitigasi', 'Acceptance', 'Transfer', 'Avoidance'],
        'Tindakan': [
            'Dokumentasi detail, gunakan Agile',
            'Buffer time 20%, prioritas fitur MVP',
            'Pelatihan, pair programming',
            'Siapkan backup PIC untuk setiap tugas',
            'Gunakan cloud hosting (Streamlit Cloud)',
            'Backup ke GitHub setiap hari'
        ],
        'Status Risiko': ['Open', 'Open', 'Mitigated', 'Open', 'Mitigated', 'Mitigated']
    }
    return pd.DataFrame(data)

@st.cache_data
def load_evm():
    data = {
        'Minggu': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'PV': [40000, 80000, 130000, 180000, 240000, 300000, 360000, 410000, 450000, 480000, 500000, 500000],
        'EV': [40000, 75000, 125000, 170000, 230000, 290000, 0, 0, 0, 0, 0, 0],
        'AC': [45000, 85000, 140000, 195000, 260000, 330000, 0, 0, 0, 0, 0, 0]
    }
    return pd.DataFrame(data)

# =============================================
# CUSTOM COMPONENTS
# =============================================
def create_kpi_card(title, value, delta=None, delta_type="neutral", color="blue", icon="📊"):
    delta_class = f"kpi-delta {delta_type}" if delta else ""
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    
    return f"""
    <div class="kpi-card {color}">
        <div class="kpi-title">{icon} {title}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

def create_alert(message, alert_type="info", icon="ℹ️"):
    return f"""
    <div class="alert-card {alert_type}">
        <span style="font-size: 1.5rem;">{icon}</span>
        <span>{message}</span>
    </div>
    """

def create_progress_bar(label, value, max_value=100):
    percentage = (value / max_value) * 100
    return f"""
    <div class="custom-progress">
        <div class="progress-label">
            <span>{label}</span>
            <span>{value}/{max_value}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%">
                {percentage:.0f}%
            </div>
        </div>
    </div>
    """

# =============================================
# LOAD DATA
# =============================================
# Header Banner
st.markdown("""
<div class="header-banner">
    <h1>📊 Project Control Dashboard</h1>
    <p>Office Supplies Management System - Real-time Monitoring & Analytics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Dashboard Settings")
    st.markdown("---")
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Auto Refresh", value=False)
    if auto_refresh:
        refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, 60)
        st.info(f"Dashboard akan refresh setiap {refresh_interval} detik")
    
    st.markdown("---")
    
    # Date Range
    st.markdown("### 📅 Project Timeline")
    st.info(f"**Start Date:** {PROJECT_START.strftime('%d %b %Y')}")
    auto_week = compute_current_week(PROJECT_START)
    st.success(f"**Current Week:** Week {auto_week}")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Quick Stats")

# Load Data
try:
    df_log = load_log(LOG_URL)
    data_loaded = True
    with st.sidebar:
        st.success(f"✅ Data loaded: {len(df_log)} records")
except Exception as e:
    with st.sidebar:
        st.error(f"⚠️ Load error")
    st.warning(f"⚠️ Gagal load data: {e}")
    df_log = pd.DataFrame(columns=["timestamp", "week_no", "document", "status", "progress"])
    data_loaded = False

df_baseline = pd.DataFrame(BASELINE)
df_baseline["target_date"] = df_baseline["target_week"].apply(
    lambda w: PROJECT_START + timedelta(days=(w - 1) * 7)
)

df_dokumen = get_latest_status(df_log, df_baseline)
df_tim = load_tim()
df_risiko = load_risiko()
df_evm = load_evm()

# =============================================
# TAB NAVIGATION
# =============================================
tab_overview, tab_sdm, tab_risiko_tab, tab_evm_tab, tab_dokumen, tab_log = st.tabs([
    "🏠 Executive Overview", 
    "👥 Team & Resources", 
    "⚠️ Risk Management", 
    "📈 Financial Control", 
    "📋 Documents Tracker",
    "📊 Activity Log"
])

# =============================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================
with tab_overview:
    # Week Selector
    col_week, col_spacer = st.columns([1, 3])
    with col_week:
        current_week = st.number_input("📅 Current Week", min_value=1, max_value=12, 
                                      value=auto_week, step=1, key="overview_week")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Calculate Metrics
    total = len(df_dokumen)
    selesai = int((df_dokumen['status'] == 'Selesai').sum())
    proses = int((df_dokumen['status'] == 'Proses').sum())
    belum = int((df_dokumen['status'] == 'Belum').sum())
    avg_progress = float(df_dokumen['progress'].mean())
    
    df_dokumen["overdue"] = (current_week > df_dokumen["target_week"]) & (df_dokumen["status"] != "Selesai")
    overdue_count = int(df_dokumen["overdue"].sum())
    
    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(create_kpi_card(
            "Total Documents", 
            total, 
            "All Deliverables", 
            "neutral",
            "blue",
            "📄"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            "Completed", 
            selesai, 
            f"{(selesai/total)*100:.0f}% Done", 
            "positive",
            "green",
            "✅"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card(
            "In Progress", 
            proses, 
            f"{(proses/total)*100:.0f}% Active", 
            "neutral",
            "yellow",
            "🔄"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card(
            "Not Started", 
            belum, 
            f"{(belum/total)*100:.0f}% Pending", 
            "negative",
            "red",
            "⏳"
        ), unsafe_allow_html=True)
    
    with col5:
        delta_type = "negative" if overdue_count > 0 else "positive"
        st.markdown(create_kpi_card(
            "Overdue", 
            overdue_count, 
            "Items Behind" if overdue_count > 0 else "On Track",
            delta_type,
            "red" if overdue_count > 0 else "green",
            "⚠️"
        ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress Overview
    st.markdown('<div class="section-header"><h2>📈 Overall Project Progress</h2></div>', 
                unsafe_allow_html=True)
    
    st.markdown(create_progress_bar("Project Completion", avg_progress, 100), 
                unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<div class="section-header"><h2>📊 Analytics Dashboard</h2></div>', 
                unsafe_allow_html=True)
    
    col_chart1, col_chart2, col_chart3 = st.columns(3)
    
    with col_chart1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Status Distribution (RAG)</div>', unsafe_allow_html=True)
        
        status_count = df_dokumen['status'].value_counts().reindex(STATUS_ORDER, fill_value=0).reset_index()
        status_count.columns = ['Status', 'Jumlah']
        
        fig = px.pie(status_count, values='Jumlah', names='Status', 
                     color='Status', color_discrete_map=STATUS_COLORS, hole=0.5)
        fig.update_traces(textposition='inside', textinfo='percent+label',
                         textfont_size=12, marker=dict(line=dict(color='white', width=2)))
        fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Workload by Role</div>', unsafe_allow_html=True)
        
        role_count = df_dokumen.groupby('pic_role').size().reset_index(name='Tasks')
        
        fig2 = go.Figure(data=[go.Bar(
            x=role_count['pic_role'],
            y=role_count['Tasks'],
            text=role_count['Tasks'],
            textposition='outside',
            marker=dict(
                color=role_count['Tasks'],
                colorscale='Blues',
                line=dict(color='rgb(8,48,107)', width=1.5)
            )
        )])
        fig2.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=250,
            yaxis=dict(showgrid=True, gridcolor='#e2e8f0')
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Phase Distribution</div>', unsafe_allow_html=True)
        
        phase_count = df_dokumen.groupby('phase').size().reset_index(name='Count')
        
        fig3 = go.Figure(data=[go.Pie(
            labels=phase_count['phase'],
            values=phase_count['Count'],
            hole=0.5,
            marker=dict(colors=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'])
        )])
        fig3.update_traces(textposition='inside', textinfo='percent+label',
                          textfont_size=10)
        fig3.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            height=250
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Document Progress Bars
    st.markdown('<div class="section-header"><h2>📋 Document Progress Details</h2></div>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    df_sorted = df_dokumen.sort_values('progress', ascending=True)
    
    fig4 = go.Figure()
    
    colors = [STATUS_COLORS[status] for status in df_sorted['status']]
    
    fig4.add_trace(go.Bar(
        x=df_sorted['progress'],
        y=df_sorted['document'],
        orientation='h',
        text=df_sorted['progress'].apply(lambda x: f'{x:.0f}%'),
        textposition='outside',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Progress: %{x}%<extra></extra>'
    ))
    
    fig4.update_layout(
        height=max(400, len(df_sorted) * 40),
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(
            range=[0, 110],
            showgrid=True,
            gridcolor='#e2e8f0',
            title="Progress (%)"
        ),
        yaxis=dict(title=""),
        showlegend=False,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Alerts Section
    st.markdown('<div class="section-header"><h2>⚠️ Alerts & Notifications</h2></div>', 
                unsafe_allow_html=True)
    
    overdue_df = df_dokumen[df_dokumen["overdue"]].copy()
    
    if overdue_df.empty:
        st.markdown(create_alert(
            "All documents are on track! No overdue items.",
            "success",
            "✅"
        ), unsafe_allow_html=True)
    else:
        for _, row in overdue_df.iterrows():
            weeks_late = current_week - row["target_week"]
            st.markdown(create_alert(
                f"<b>{row['document']}</b> - {weeks_late} week(s) overdue (Target: Week {row['target_week']}) - PIC: {row['pic_role']}",
                "error",
                "🔴"
            ), unsafe_allow_html=True)

# =============================================
# TAB 2: TEAM & RESOURCES
# =============================================
with tab_sdm:
    st.markdown('<div class="section-header"><h2>👥 Team Structure & Allocation</h2></div>', 
                unsafe_allow_html=True)
    
    # Team Cards
    cols = st.columns(4)
    team_icons = ["👔", "📊", "🎨", "💻"]
    team_colors = ["blue", "green", "purple", "red"]
    
    for idx, (col, (_, row)) in enumerate(zip(cols, df_tim.iterrows())):
        with col:
            tasks = df_dokumen[df_dokumen['pic_role'] == row['Role']]
            completed = len(tasks[tasks['status'] == 'Selesai'])
            total_tasks = len(tasks)
            
            st.markdown(f"""
            <div class="kpi-card {team_colors[idx]}">
                <div class="kpi-title">{team_icons[idx]} {row['Role']}</div>
                <div class="kpi-value">{total_tasks}</div>
                <div class="kpi-delta positive">{completed} Completed</div>
                <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #64748b;">
                    {row['Deskripsi']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Details Table
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Team Member Details</div>', unsafe_allow_html=True)
    st.dataframe(df_tim, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # RACI Matrix
    st.markdown('<div class="section-header"><h2>📊 RACI Responsibility Matrix</h2></div>', 
                unsafe_allow_html=True)
    
    raci_data = {
        'Document': [
            'Project Charter', 'Gantt Chart / Schedule', 'SRS', 
            'Use Case Diagram + Deskripsi', 'ERD + Data Dictionary',
            'Wireframe / Mockup UI', 'Risk Register', 'User Manual'
        ],
        'PM': ['R/A', 'R/A', 'C', 'C', 'I', 'I', 'R/A', 'C'],
        'BA/SA': ['C', 'C', 'R/A', 'R/A', 'C', 'C', 'C', 'R/A'],
        'UI/UX': ['I', 'I', 'C', 'C', 'I', 'R/A', 'I', 'I'],
        'Backend/DB': ['I', 'I', 'C', 'C', 'R/A', 'I', 'I', 'C']
    }
    df_raci = pd.DataFrame(raci_data)
    
    def style_raci(val):
        if 'A' in str(val):
            return 'background-color: #ef4444; color: white; font-weight: bold'
        elif 'R' in str(val):
            return 'background-color: #3b82f6; color: white; font-weight: bold'
        elif val == 'C':
            return 'background-color: #fbbf24; color: black; font-weight: bold'
        elif val == 'I':
            return 'background-color: #a7f3d0; color: black'
        return ''
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(df_raci.style.map(style_raci, subset=['PM', 'BA/SA', 'UI/UX', 'Backend/DB']),
                 use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 8px;">
        <b>Legend:</b><br>
        🔴 <b>R/A</b> = Responsible & Accountable&nbsp;&nbsp;|&nbsp;&nbsp;
        🔵 <b>R</b> = Responsible&nbsp;&nbsp;|&nbsp;&nbsp;
        🟡 <b>C</b> = Consulted&nbsp;&nbsp;|&nbsp;&nbsp;
        🟢 <b>I</b> = Informed
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Workload Chart
    st.markdown('<div class="section-header"><h2>📊 Workload Distribution Analysis</h2></div>', 
                unsafe_allow_html=True)
    
    workload_data = []
    for role in ['PM', 'BA/SA', 'UI/UX', 'Backend/DB']:
        role_docs = df_dokumen[df_dokumen['pic_role'] == role]
        workload_data.append({
            'Role': role,
            'Completed': int((role_docs['status'] == 'Selesai').sum()),
            'In Progress': int((role_docs['status'] == 'Proses').sum()),
            'Not Started': int((role_docs['status'] == 'Belum').sum())
        })
    
    df_workload = pd.DataFrame(workload_data)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name='Completed', x=df_workload['Role'], y=df_workload['Completed'],
                         marker_color='#10b981', text=df_workload['Completed']))
    fig.add_trace(go.Bar(name='In Progress', x=df_workload['Role'], y=df_workload['In Progress'],
                         marker_color='#f59e0b', text=df_workload['In Progress']))
    fig.add_trace(go.Bar(name='Not Started', x=df_workload['Role'], y=df_workload['Not Started'],
                         marker_color='#ef4444', text=df_workload['Not Started']))
    
    fig.update_traces(textposition='inside', textfont_size=12)
    fig.update_layout(
        barmode='stack',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        plot_bgcolor='white',
        xaxis=dict(title="Team Role"),
        yaxis=dict(title="Number of Tasks", showgrid=True, gridcolor='#e2e8f0')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# TAB 3: RISK MANAGEMENT
# =============================================
with tab_risiko_tab:
    st.markdown('<div class="section-header"><h2>⚠️ Risk Management Dashboard</h2></div>', 
                unsafe_allow_html=True)
    
    # Risk Metrics
    open_risks = len(df_risiko[df_risiko['Status Risiko'] == 'Open'])
    mitigated = len(df_risiko[df_risiko['Status Risiko'] == 'Mitigated'])
    high_prob = len(df_risiko[df_risiko['Probabilitas'] == 'Tinggi'])
    high_impact = len(df_risiko[df_risiko['Dampak'] == 'Tinggi'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card("Open Risks", open_risks, "Requires Action", 
                                   "negative" if open_risks > 0 else "positive", "red", "🔴"),
                   unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("Mitigated", mitigated, "Under Control", "positive", "green", "✅"),
                   unsafe_allow_html=True)
    with col3:
        st.markdown(create_kpi_card("High Probability", high_prob, "Likely to Occur", "neutral", "yellow", "⚠️"),
                   unsafe_allow_html=True)
    with col4:
        st.markdown(create_kpi_card("High Impact", high_impact, "Significant Effect", "neutral", "purple", "💥"),
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Risk Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Risk Matrix (Impact vs Probability)</div>', 
                   unsafe_allow_html=True)
        
        # Create numeric mapping for scatter plot
        prob_map = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}
        impact_map = {'Sedang': 2, 'Tinggi': 3}
        
        df_risk_plot = df_risiko.copy()
        df_risk_plot['Prob_Num'] = df_risk_plot['Probabilitas'].map(prob_map)
        df_risk_plot['Impact_Num'] = df_risk_plot['Dampak'].map(impact_map)
        
        fig = px.scatter(df_risk_plot, x='Impact_Num', y='Prob_Num',
                        size='Skor', color='Status Risiko',
                        hover_name='Risiko', size_max=30,
                        color_discrete_map={'Open': '#ef4444', 'Mitigated': '#10b981'})
        
        fig.update_layout(
            xaxis=dict(title="Impact", tickmode='array', 
                      tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High']),
            yaxis=dict(title="Probability", tickmode='array',
                      tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High']),
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='#f8fafc'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Response Strategy Distribution</div>', 
                   unsafe_allow_html=True)
        
        strategi_count = df_risiko['Strategi'].value_counts().reset_index()
        strategi_count.columns = ['Strategy', 'Count']
        
        fig2 = go.Figure(data=[go.Pie(
            labels=strategi_count['Strategy'],
            values=strategi_count['Count'],
            hole=0.5,
            marker=dict(colors=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'])
        )])
        
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=True,
            legend=dict(orientation='v', yanchor='middle', y=0.5)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk Register Table
    st.markdown('<div class="section-header"><h2>📋 Complete Risk Register</h2></div>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(df_risiko, use_container_width=True, hide_index=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# TAB 4: EVM & FINANCIAL CONTROL
# =============================================
with tab_evm_tab:
    st.markdown('<div class="section-header"><h2>📈 Earned Value Management</h2></div>', 
                unsafe_allow_html=True)
    
    # Week Selector
    current_week_evm = st.slider("📅 Select Week for EVM Analysis", 
                                 min_value=1, max_value=12, value=min(6, auto_week), 
                                 key="evm_week_slider")
    
    # Calculate EVM
    BAC = 500000
    df_evm_current = df_evm[df_evm['Minggu'] <= current_week_evm]
    
    if len(df_evm_current) > 0 and df_evm_current['EV'].iloc[-1] > 0:
        PV = df_evm_current['PV'].iloc[-1]
        EV = df_evm_current['EV'].iloc[-1]
        AC = df_evm_current['AC'].iloc[-1]
        
        SV = EV - PV
        CV = EV - AC
        SPI = EV / PV if PV > 0 else 0
        CPI = EV / AC if AC > 0 else 0
        EAC = BAC / CPI if CPI > 0 else BAC
        VAC = BAC - EAC
    else:
        PV, EV, AC = 0, 0, 0
        SV, CV, SPI, CPI, EAC, VAC = 0, 0, 0, 0, BAC, 0
    
    # Financial Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(create_kpi_card("Budget (BAC)", f"Rp {BAC/1000:.0f}K", 
                                   "Total Allocated", "neutral", "blue", "💰"),
                   unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("Earned Value", f"Rp {EV/1000:.0f}K", 
                                   f"{(EV/BAC)*100:.0f}% Complete", "positive", "green", "✅"),
                   unsafe_allow_html=True)
    with col3:
        st.markdown(create_kpi_card("Actual Cost", f"Rp {AC/1000:.0f}K", 
                                   f"{(AC/BAC)*100:.0f}% Spent", "neutral", "purple", "💸"),
                   unsafe_allow_html=True)
    with col4:
        cv_type = "positive" if CV >= 0 else "negative"
        cv_label = "Under Budget" if CV >= 0 else "Over Budget"
        st.markdown(create_kpi_card("Cost Variance", f"Rp {CV/1000:.0f}K", 
                                   cv_label, cv_type, "green" if CV >= 0 else "red", "💵"),
                   unsafe_allow_html=True)
    with col5:
        sv_type = "positive" if SV >= 0 else "negative"
        sv_label = "Ahead" if SV >= 0 else "Behind"
        st.markdown(create_kpi_card("Schedule Variance", f"Rp {SV/1000:.0f}K", 
                                   sv_label, sv_type, "green" if SV >= 0 else "red", "📆"),
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance Indices
    col1, col2, col3 = st.columns(3)
    
    with col1:
        spi_type = "positive" if SPI >= 1 else "negative"
        spi_label = "On Schedule" if SPI >= 1 else "Behind Schedule"
        st.markdown(create_kpi_card("SPI (Schedule)", f"{SPI:.2f}", 
                                   spi_label, spi_type, "green" if SPI >= 1 else "red", "⏱️"),
                   unsafe_allow_html=True)
    with col2:
        cpi_type = "positive" if CPI >= 1 else "negative"
        cpi_label = "Efficient" if CPI >= 1 else "Over Budget"
        st.markdown(create_kpi_card("CPI (Cost)", f"{CPI:.2f}", 
                                   cpi_label, cpi_type, "green" if CPI >= 1 else "red", "💹"),
                   unsafe_allow_html=True)
    with col3:
        st.markdown(create_kpi_card("EAC (Forecast)", f"Rp {EAC/1000:.0f}K", 
                                   f"VAC: Rp {VAC/1000:.0f}K", 
                                   "positive" if VAC >= 0 else "negative", 
                                   "green" if VAC >= 0 else "red", "🔮"),
                   unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # S-Curve Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 S-Curve Analysis</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_evm['Minggu'], y=df_evm['PV'],
        mode='lines+markers',
        name='Planned Value (PV)',
        line=dict(color='#3b82f6', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_evm_current['Minggu'], y=df_evm_current['EV'],
        mode='lines+markers',
        name='Earned Value (EV)',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8),
        fill='tonexty'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_evm_current['Minggu'], y=df_evm_current['AC'],
        mode='lines+markers',
        name='Actual Cost (AC)',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        xaxis=dict(title='Week', showgrid=True, gridcolor='#e2e8f0'),
        yaxis=dict(title='Value (Rp)', showgrid=True, gridcolor='#e2e8f0'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
        height=450,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # RAG Status & Recommendations
    col_rag, col_rec = st.columns(2)
    
    with col_rag:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🚦 Project Health Status (RAG)</div>', 
                   unsafe_allow_html=True)
        
        if SPI >= 0.95 and CPI >= 0.95:
            st.markdown(create_alert(
                "<b>GREEN STATUS</b> - Project is performing well. Schedule and cost are on track.",
                "success", "🟢"
            ), unsafe_allow_html=True)
        elif SPI >= 0.8 and CPI >= 0.8:
            st.markdown(create_alert(
                "<b>AMBER STATUS</b> - Project needs attention. Minor deviations detected.",
                "warning", "🟡"
            ), unsafe_allow_html=True)
        else:
            st.markdown(create_alert(
                "<b>RED STATUS</b> - Project requires immediate corrective action!",
                "error", "🔴"
            ), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_rec:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💡 Recommendations</div>', unsafe_allow_html=True)
        
        recommendations = []
        if SPI < 0.9:
            recommendations.append("📅 Accelerate critical path activities")
        if CPI < 0.9:
            recommendations.append("💰 Review budget allocation and reduce costs")
        if SPI >= 0.95 and CPI >= 0.95:
            recommendations.append("✅ Maintain current performance level")
        if VAC < 0:
            recommendations.append("⚠️ Request additional budget or reduce scope")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# TAB 5: DOCUMENTS TRACKER
# =============================================
with tab_dokumen:
    st.markdown('<div class="section-header"><h2>📋 Document Tracking System</h2></div>', 
                unsafe_allow_html=True)
    
    # Filters
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.markdown("### 🔍 Filters")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        status_filter = st.multiselect("Status:", STATUS_ORDER, default=STATUS_ORDER)
    with col_f2:
        role_list = sorted(df_dokumen['pic_role'].dropna().unique().tolist())
        role_filter = st.multiselect("PIC Role:", role_list, default=role_list)
    with col_f3:
        phase_list = sorted(df_dokumen['phase'].dropna().unique().tolist())
        phase_filter = st.multiselect("Phase:", phase_list, default=phase_list)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply Filters
    df_filtered = df_dokumen[
        (df_dokumen['status'].isin(status_filter)) & 
        (df_dokumen['pic_role'].isin(role_filter)) &
        (df_dokumen['phase'].isin(phase_filter))
    ].copy()
    
    st.markdown(f"**Showing {len(df_filtered)} of {len(df_dokumen)} documents**")
    
    # Documents Table
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    available_cols = df_filtered.columns.tolist()
    display_cols = []
    for col in ['document', 'phase', 'pic_role', 'target_week', 'status', 'progress', 'timestamp']:
        if col in available_cols:
            display_cols.append(col)
    
    df_display = df_filtered[display_cols].copy()
    
    if 'progress' in df_display.columns:
        df_display['progress'] = df_display['progress'].astype(int).astype(str) + '%'
    
    st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Upcoming Deadlines
    st.markdown('<div class="section-header"><h2>📅 Upcoming Deadlines</h2></div>', 
                unsafe_allow_html=True)
    
    current_week_dok = auto_week
    df_upcoming = df_dokumen[
        (df_dokumen['status'] != 'Selesai') & 
        (df_dokumen['target_week'] >= current_week_dok)
    ].sort_values('target_week')
    
    if df_upcoming.empty:
        st.markdown(create_alert(
            "All documents completed or no upcoming deadlines!",
            "success", "✅"
        ), unsafe_allow_html=True)
    else:
        for _, row in df_upcoming.head(5).iterrows():
            weeks_left = row['target_week'] - current_week_dok
            
            if weeks_left <= 0:
                st.markdown(create_alert(
                    f"<b>{row['document']}</b> - Due THIS WEEK (Week {row['target_week']}) - PIC: {row['pic_role']}",
                    "error", "🔴"
                ), unsafe_allow_html=True)
            elif weeks_left == 1:
                st.markdown(create_alert(
                    f"<b>{row['document']}</b> - Due next week (Week {row['target_week']}) - PIC: {row['pic_role']}",
                    "warning", "🟡"
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_alert(
                    f"<b>{row['document']}</b> - Due in {weeks_left} weeks (Week {row['target_week']}) - PIC: {row['pic_role']}",
                    "info", "🔵"
                ), unsafe_allow_html=True)

# =============================================
# TAB 6: ACTIVITY LOG
# =============================================
with tab_log:
    st.markdown('<div class="section-header"><h2>📊 Activity Log & Audit Trail</h2></div>', 
                unsafe_allow_html=True)
    
    if not data_loaded or df_log.empty:
        st.markdown(create_alert(
            "No activity log data available yet. Updates will appear here once submitted via Google Form.",
            "warning", "⚠️"
        ), unsafe_allow_html=True)
    else:
        # Week Filter
        max_week = int(df_log["week_no"].max()) if df_log["week_no"].notna().any() else 1
        week_options = list(range(1, max_week + 1))
        
        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
        week_pick = st.multiselect("📅 Filter by Week", week_options, default=[max_week])
        st.markdown('</div>', unsafe_allow_html=True)
        
        df_view = df_log[df_log["week_no"].isin(week_pick)].copy()
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_kpi_card("Total Updates", len(df_view), "Filtered View", 
                                       "neutral", "blue", "📝"),
                       unsafe_allow_html=True)
        with col2:
            st.markdown(create_kpi_card("Documents Updated", df_view["document"].nunique(), 
                                       "Unique Docs", "neutral", "green", "📄"),
                       unsafe_allow_html=True)
        with col3:
            st.markdown(create_kpi_card("Total Log Entries", len(df_log), 
                                       "All Time", "neutral", "purple", "📊"),
                       unsafe_allow_html=True)
        with col4:
            if len(df_view) > 0:
                latest = df_view["timestamp"].max()
                hours_ago = (datetime.now() - latest).total_seconds() / 3600
                st.markdown(create_kpi_card("Last Update", f"{hours_ago:.0f}h ago", 
                                           latest.strftime("%d/%m %H:%M"), "neutral", "yellow", "🕐"),
                           unsafe_allow_html=True)
            else:
                st.markdown(create_kpi_card("Last Update", "N/A", "No Data", 
                                           "neutral", "yellow", "🕐"),
                           unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Activity Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Weekly Activity Trend</div>', unsafe_allow_html=True)
        
        week_counts = df_log.groupby("week_no").size().reset_index(name="updates")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=week_counts["week_no"],
            y=week_counts["updates"],
            text=week_counts["updates"],
            textposition='outside',
            marker=dict(
                color=week_counts["updates"],
                colorscale='Blues',
                showscale=False,
                line=dict(color='white', width=1)
            )
        ))
        
        fig.update_layout(
            xaxis=dict(title="Week", showgrid=False),
            yaxis=dict(title="Number of Updates", showgrid=True, gridcolor='#e2e8f0'),
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Log Table
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📋 Detailed Activity Log</div>', unsafe_allow_html=True)
        
        available_log_cols = df_view.columns.tolist()
        show_cols = []
        for c in ["timestamp", "week_no", "document", "status", "progress", "pic_role", "updated_by", "notes"]:
            if c in available_log_cols:
                show_cols.append(c)
        
        df_log_display = df_view.sort_values("timestamp", ascending=False)[show_cols]
        st.dataframe(df_log_display, use_container_width=True, hide_index=True, height=400)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# FOOTER
# =============================================
st.markdown("""
<div class="footer">
    <h3 style="margin: 0; color: #1e293b;">📊 Project Control Dashboard</h3>
    <p style="margin: 0.5rem 0; color: #64748b;">
        <b>Office Supplies Management System</b><br>
        Project Management Course | 2025<br>
        <small>Data Source: Google Forms Integration | Auto-refresh enabled</small>
    </p>
    <div style="margin-top: 1rem;">
        <span class="metric-badge badge-info">Streamlit</span>
        <span class="metric-badge badge-success">Plotly</span>
        <span class="metric-badge badge-warning">Python</span>
    </div>
</div>
""", unsafe_allow_html=True)
