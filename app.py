import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Dashboard Monitoring Proyek - Office Supplies",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS
# =============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    html, body, [class*="css"] {
        font-size: 16px;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .main {
        background-color: #FFFFFF;
    }
    
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    .dashboard-header {
        background: #FFFFFF;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid #F1F5F9;
    }
    
    .dashboard-header h1 {
        margin: 0;
        font-size: 2.25rem;
        font-weight: 700;
        color: #0F172A;
    }
    
    .dashboard-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.125rem;
        color: #64748B;
    }
    
    .kpi-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        height: 100%;
    }
    
    .kpi-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    
    .kpi-change {
        font-size: 0.95rem;
        font-weight: 500;
        color: #64748B;
    }
    
    .kpi-change.positive { color: #059669; }
    .kpi-change.negative { color: #DC2626; }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0F172A;
        margin: 2.5rem 0 1.25rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .chart-container {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    
    .chart-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 1rem;
    }
    
    .alert {
        padding: 1rem 1.25rem;
        border-radius: 6px;
        margin: 0.75rem 0;
        font-size: 1rem;
        border-left: 4px solid;
        line-height: 1.5;
    }
    
    .alert-success {
        background: #F0FDF4;
        border-left-color: #10B981;
        color: #065F46;
    }
    
    .alert-warning {
        background: #FFFBEB;
        border-left-color: #F59E0B;
        color: #92400E;
    }
    
    .alert-error {
        background: #FEF2F2;
        border-left-color: #EF4444;
        color: #991B1B;
    }
    
    .alert-info {
        background: #F0F9FF;
        border-left-color: #3B82F6;
        color: #1E40AF;
    }
    
    .progress-container {
        margin: 1.25rem 0;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.75rem;
        font-size: 1.05rem;
        color: #475569;
        font-weight: 500;
    }
    
    .progress-bar-bg {
        height: 12px;
        background: #F1F5F9;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: #0F172A;
        border-radius: 6px;
    }
    
    .filter-section {
        background: #F8FAFC;
        padding: 1.25rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #64748B;
        font-weight: 500;
        padding: 1rem 1.75rem;
        font-size: 1.05rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0F172A;
        border-bottom: 2px solid #0F172A;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# =============================================
# COLOR PALETTE
# =============================================
COLORS = {
    'primary': '#0F172A',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'neutral': '#64748B',
}

STATUS_COLORS = {
    "Selesai": COLORS['success'],
    "Proses": COLORS['warning'],
    "Belum": COLORS['neutral']
}

# =============================================
# DATA CONFIGURATION
# =============================================
LOG_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEpBx0Eg1x3unaxVVQWJVFfzmH9Z8qKQPevp87cnsfP-nhyNYfhQvVc3Vpd0sDfkNRaNs7R4VH1nOa/pub?gid=1285157492&single=true&output=csv"
PROJECT_START = date(2025, 11, 10)
STATUS_ORDER = ["Belum", "Proses", "Selesai"]

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

# =============================================
# HELPER FUNCTIONS
# =============================================
def normalize_columns(df):
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    rename_map = {
        "week": "week_no", "mingguke": "week_no", "minggu_ke": "week_no",
        "doc": "document", "nama dokumen": "document",
        "fase": "phase", "pic": "pic_role", "role": "pic_role",
        "updatedby": "updated_by", "catatan": "notes",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df

@st.cache_data(ttl=60)
def load_log(url):
    df = pd.read_csv(url)
    df = normalize_columns(df)
    required = {"timestamp", "week_no", "document", "status", "progress"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "week_start" in df.columns:
        df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce")
    df["week_no"] = pd.to_numeric(df["week_no"], errors="coerce")
    df["progress"] = pd.to_numeric(df["progress"], errors="coerce")
    df["status"] = df["status"].astype(str).str.strip().str.title()
    df.loc[~df["status"].isin(STATUS_ORDER), "status"] = "Proses"
    df["document"] = df["document"].astype(str).str.strip()
    return df.dropna(subset=["week_no", "document"])

def compute_current_week(project_start):
    today = date.today()
    delta_days = (today - project_start).days
    if delta_days < 0:
        return 1
    return min(12, max(1, delta_days // 7 + 1))

def get_latest_status(df_log, df_baseline):
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
        
        cols_to_drop = [c for c in df_result.columns if c.endswith("_log")]
        df_result = df_result.drop(columns=cols_to_drop, errors="ignore")
    else:
        df_result["status"] = "Belum"
        df_result["progress"] = 0
    
    return df_result

@st.cache_data
def load_tim():
    return pd.DataFrame({
        'Role': ['PM', 'BA/SA', 'UI/UX', 'Backend/DB'],
        'Deskripsi': ['Project Manager', 'Business/System Analyst', 'UI/UX Designer', 'Backend/Database Engineer'],
        'Skill': ['Leadership, Planning, Risk Management', 'Analysis, Documentation, Communication', 
                  'Figma, CSS, User Research', 'Database, SQL, Python/Laravel']
    })

@st.cache_data
def load_risiko():
    return pd.DataFrame({
        'ID': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'],
        'Risiko': ['Requirement berubah-ubah', 'Deadline tidak tercapai', 'Skill tim kurang memadai',
                   'Anggota tim berhalangan', 'Server down saat demo', 'Data/code hilang'],
        'Probabilitas': ['Tinggi', 'Sedang', 'Sedang', 'Sedang', 'Rendah', 'Rendah'],
        'Dampak': ['Sedang', 'Tinggi', 'Tinggi', 'Sedang', 'Tinggi', 'Tinggi'],
        'Skor': [6, 6, 6, 4, 4, 4],
        'Strategi': ['Mitigasi', 'Mitigasi', 'Mitigasi', 'Acceptance', 'Transfer', 'Avoidance'],
        'Status': ['Open', 'Open', 'Mitigated', 'Open', 'Mitigated', 'Mitigated']
    })

@st.cache_data
def load_evm():
    return pd.DataFrame({
        'Minggu': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'PV': [40000, 80000, 130000, 180000, 240000, 300000, 360000, 410000, 450000, 480000, 500000, 500000],
        'EV': [40000, 75000, 125000, 170000, 230000, 290000, 0, 0, 0, 0, 0, 0],
        'AC': [45000, 85000, 140000, 195000, 260000, 330000, 0, 0, 0, 0, 0, 0]
    })

# =============================================
# UI COMPONENTS
# =============================================
def kpi_card(label, value, change=None):
    change_html = ""
    if change:
        change_class = "positive" if "✓" in str(change) else "negative" if "⚠" in str(change) else ""
        change_html = f'<div class="kpi-change {change_class}">{change}</div>'
    return f'''
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {change_html}
    </div>
    '''

def alert_box(message, alert_type="info"):
    return f'<div class="alert alert-{alert_type}">{message}</div>'

def progress_bar(label, current, total):
    pct = (current / total * 100) if total > 0 else 0
    return f'''
    <div class="progress-container">
        <div class="progress-header">
            <span>{label}</span>
            <span>{pct:.1f}%</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {pct}%"></div>
        </div>
    </div>
    '''

# =============================================
# LOAD DATA
# =============================================
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Project Monitoring Dashboard</h1>
    <p>Office Supplies Management System — Real-time project tracking</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    auto_week = compute_current_week(PROJECT_START)
    st.info(f"**📅 Current Week:** {auto_week}")
    st.caption(f"Project Start: {PROJECT_START.strftime('%d %b %Y')}")

try:
    df_log = load_log(LOG_URL)
    data_loaded = True
    with st.sidebar:
        st.success(f"✅ {len(df_log)} records loaded")
except Exception as e:
    st.warning(f"⚠️ Data load error: {str(e)}")
    df_log = pd.DataFrame(columns=["timestamp", "week_no", "document", "status", "progress"])
    data_loaded = False

df_baseline = pd.DataFrame(BASELINE)
df_baseline["target_date"] = df_baseline["target_week"].apply(lambda w: PROJECT_START + timedelta(days=(w - 1) * 7))
df_dokumen = get_latest_status(df_log, df_baseline)
df_tim = load_tim()
df_risiko = load_risiko()
df_evm = load_evm()

# =============================================
# TABS
# =============================================
tabs = st.tabs(["📊 Overview", "👥 Team", "⚠️ Risk", "💰 EVM", "📄 Documents", "📝 Log"])

# =============================================
# TAB 1: OVERVIEW
# =============================================
with tabs[0]:
    col_w, _ = st.columns([1, 3])
    with col_w:
        current_week = st.number_input("📅 Current Week", 1, 12, auto_week, key="week_overview")
    
    st.markdown("---")
    
    total = len(df_dokumen)
    selesai = int((df_dokumen['status'] == 'Selesai').sum())
    proses = int((df_dokumen['status'] == 'Proses').sum())
    belum = int((df_dokumen['status'] == 'Belum').sum())
    avg_progress = float(df_dokumen['progress'].mean())
    df_dokumen["overdue"] = (current_week > df_dokumen["target_week"]) & (df_dokumen["status"] != "Selesai")
    overdue = int(df_dokumen["overdue"].sum())
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(kpi_card("Total Documents", total, "All deliverables"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Completed", selesai, f"✓ {selesai/total*100:.0f}% done"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("In Progress", proses, f"{proses/total*100:.0f}% active"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("Not Started", belum, f"{belum/total*100:.0f}% pending"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_card("Overdue", overdue, "⚠️ Attention" if overdue > 0 else "✓ On track"), unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📈 Overall Progress</div>', unsafe_allow_html=True)
    st.markdown(progress_bar("Project Completion", avg_progress, 100), unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📊 Analytics</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown('<div class="chart-container"><div class="chart-header">Status Distribution</div>', unsafe_allow_html=True)
        status_count = df_dokumen['status'].value_counts().reindex(STATUS_ORDER, fill_value=0)
        
        fig = go.Figure(data=[go.Bar(
            x=status_count.index,
            y=status_count.values,
            text=status_count.values,
            textposition='outside',
            textfont=dict(size=14),
            marker_color=[STATUS_COLORS[s] for s in status_count.index]
        )])
        fig.update_layout(
            height=320, 
            font=dict(size=14),
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis=dict(title="", tickfont=dict(size=13)),
            yaxis=dict(title="Count", tickfont=dict(size=13), gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_c2:
        st.markdown('<div class="chart-container"><div class="chart-header">Workload by Role</div>', unsafe_allow_html=True)
        role_count = df_dokumen.groupby('pic_role').size()
        
        fig2 = go.Figure(data=[go.Bar(
            x=role_count.index,
            y=role_count.values,
            text=role_count.values,
            textposition='outside',
            textfont=dict(size=14),
            marker_color=COLORS['primary']
        )])
        fig2.update_layout(
            height=320,
            font=dict(size=14),
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis=dict(title="", tickfont=dict(size=13)),
            yaxis=dict(title="Tasks", tickfont=dict(size=13), gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📋 Document Progress</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    df_sorted = df_dokumen.sort_values('progress', ascending=True)
    
    fig3 = go.Figure(data=[go.Bar(
        x=df_sorted['progress'],
        y=df_sorted['document'],
        orientation='h',
        text=df_sorted['progress'].apply(lambda x: f'{x:.0f}%'),
        textposition='outside',
        textfont=dict(size=13),
        marker_color=[STATUS_COLORS[s] for s in df_sorted['status']]
    )])
    fig3.update_layout(
        height=max(400, len(df_sorted) * 45),
        font=dict(size=14),
        plot_bgcolor='white',
        margin=dict(l=20, r=40, t=20, b=40),
        xaxis=dict(range=[0, 115], title="Progress (%)", tickfont=dict(size=13), gridcolor='#F1F5F9'),
        yaxis=dict(title="", tickfont=dict(size=13))
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">⚠️ Alerts</div>', unsafe_allow_html=True)
    overdue_df = df_dokumen[df_dokumen["overdue"]]
    if overdue_df.empty:
        st.markdown(alert_box("✓ All documents are on track.", "success"), unsafe_allow_html=True)
    else:
        for _, row in overdue_df.iterrows():
            weeks_late = current_week - row["target_week"]
            st.markdown(alert_box(
                f"<strong>{row['document']}</strong> — {weeks_late} week(s) overdue — PIC: {row['pic_role']}",
                "error"
            ), unsafe_allow_html=True)

# =============================================
# TAB 2: TEAM
# =============================================
with tabs[1]:
    st.markdown('<div class="section-title">👥 Team Overview</div>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, (_, row) in enumerate(df_tim.iterrows()):
        with cols[idx]:
            tasks = df_dokumen[df_dokumen['pic_role'] == row['Role']]
            completed = len(tasks[tasks['status'] == 'Selesai'])
            st.markdown(kpi_card(row['Role'], len(tasks), f"✓ {completed} completed"), unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📋 Team Details</div>', unsafe_allow_html=True)
    st.dataframe(df_tim, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="section-title">📊 Workload Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
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
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Completed', x=df_workload['Role'], y=df_workload['Completed'],
                         marker_color=COLORS['success'], text=df_workload['Completed'], textposition='inside'))
    fig.add_trace(go.Bar(name='In Progress', x=df_workload['Role'], y=df_workload['In Progress'],
                         marker_color=COLORS['warning'], text=df_workload['In Progress'], textposition='inside'))
    fig.add_trace(go.Bar(name='Not Started', x=df_workload['Role'], y=df_workload['Not Started'],
                         marker_color=COLORS['neutral'], text=df_workload['Not Started'], textposition='inside'))
    fig.update_layout(
        barmode='stack', height=380, font=dict(size=14),
        plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=40),
        legend=dict(orientation='h', y=1.1, font=dict(size=13)),
        xaxis=dict(tickfont=dict(size=13)),
        yaxis=dict(tickfont=dict(size=13), gridcolor='#F1F5F9')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# TAB 3: RISK
# =============================================
with tabs[2]:
    st.markdown('<div class="section-title">⚠️ Risk Summary</div>', unsafe_allow_html=True)
    
    open_risks = len(df_risiko[df_risiko['Status'] == 'Open'])
    mitigated = len(df_risiko[df_risiko['Status'] == 'Mitigated'])
    high_score = len(df_risiko[df_risiko['Skor'] >= 6])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("Open Risks", open_risks, "⚠️ Action needed"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Mitigated", mitigated, "✓ Under control"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("High Score (≥6)", high_score, "Critical"), unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📋 Risk Register</div>', unsafe_allow_html=True)
    st.dataframe(df_risiko, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="section-title">📊 Risk Analysis</div>', unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.markdown('<div class="chart-container"><div class="chart-header">By Status</div>', unsafe_allow_html=True)
        status_count = df_risiko['Status'].value_counts()
        
        fig = go.Figure(data=[go.Bar(
            x=status_count.index, y=status_count.values,
            text=status_count.values, textposition='outside', textfont=dict(size=14),
            marker_color=[COLORS['danger'] if x == 'Open' else COLORS['success'] for x in status_count.index]
        )])
        fig.update_layout(
            height=300, font=dict(size=14), plot_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis=dict(tickfont=dict(size=13)),
            yaxis=dict(tickfont=dict(size=13), gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_r2:
        st.markdown('<div class="chart-container"><div class="chart-header">By Strategy</div>', unsafe_allow_html=True)
        strategy_count = df_risiko['Strategi'].value_counts()
        
        fig2 = go.Figure(data=[go.Bar(
            x=strategy_count.index, y=strategy_count.values,
            text=strategy_count.values, textposition='outside', textfont=dict(size=14),
            marker_color=COLORS['primary']
        )])
        fig2.update_layout(
            height=300, font=dict(size=14), plot_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis=dict(tickfont=dict(size=13)),
            yaxis=dict(tickfont=dict(size=13), gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# TAB 4: EVM
# =============================================
with tabs[3]:
    st.markdown('<div class="section-title">💰 Earned Value Management</div>', unsafe_allow_html=True)
    
    current_week_evm = st.slider("📅 Select Week", 1, 12, min(6, auto_week), key="evm_week")
    
    BAC = 500000
    df_evm_current = df_evm[df_evm['Minggu'] <= current_week_evm]
    
    if len(df_evm_current) > 0 and df_evm_current['EV'].iloc[-1] > 0:
        PV = df_evm_current['PV'].iloc[-1]
        EV = df_evm_current['EV'].iloc[-1]
        AC = df_evm_current['AC'].iloc[-1]
        SV, CV = EV - PV, EV - AC
        SPI = EV / PV if PV > 0 else 0
        CPI = EV / AC if AC > 0 else 0
        EAC = BAC / CPI if CPI > 0 else BAC
    else:
        PV, EV, AC, SV, CV, SPI, CPI, EAC = 0, 0, 0, 0, 0, 0, 0, BAC
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Budget (BAC)", f"Rp {BAC/1000:.0f}K", "Total"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Earned Value", f"Rp {EV/1000:.0f}K", f"✓ {EV/BAC*100:.0f}%"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Actual Cost", f"Rp {AC/1000:.0f}K", f"{AC/BAC*100:.0f}% spent"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("EAC", f"Rp {EAC/1000:.0f}K", "Forecast"), unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown(kpi_card("CPI", f"{CPI:.2f}", "✓ Efficient" if CPI >= 1 else "⚠️ Over budget"), unsafe_allow_html=True)
    with col6:
        st.markdown(kpi_card("SPI", f"{SPI:.2f}", "✓ On time" if SPI >= 1 else "⚠️ Behind"), unsafe_allow_html=True)
    with col7:
        health = "🟢 Green" if (SPI >= 0.95 and CPI >= 0.95) else "🟡 Amber" if (SPI >= 0.8 and CPI >= 0.8) else "🔴 Red"
        st.markdown(kpi_card("Health", health, "RAG Status"), unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📈 S-Curve Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_evm['Minggu'], y=df_evm['PV'], mode='lines+markers',
                             name='PV', line=dict(color=COLORS['neutral'], width=2, dash='dash'), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=df_evm_current['Minggu'], y=df_evm_current['EV'], mode='lines+markers',
                             name='EV', line=dict(color=COLORS['primary'], width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=df_evm_current['Minggu'], y=df_evm_current['AC'], mode='lines+markers',
                             name='AC', line=dict(color=COLORS['danger'], width=2), marker=dict(size=8)))
    fig.update_layout(
        height=420, font=dict(size=14), plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=40),
        legend=dict(orientation='h', y=1.1, font=dict(size=13)),
        xaxis=dict(title='Week', tickfont=dict(size=13), gridcolor='#F1F5F9'),
        yaxis=dict(title='Value (Rp)', tickfont=dict(size=13), gridcolor='#F1F5F9')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# TAB 5: DOCUMENTS
# =============================================
with tabs[4]:
    st.markdown('<div class="section-title">📄 Document Tracker</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        status_filter = st.multiselect("Status", STATUS_ORDER, default=STATUS_ORDER)
    with col_f2:
        role_filter = st.multiselect("Role", sorted(df_dokumen['pic_role'].unique()), 
                                     default=sorted(df_dokumen['pic_role'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    df_filtered = df_dokumen[(df_dokumen['status'].isin(status_filter)) & (df_dokumen['pic_role'].isin(role_filter))]
    st.markdown(f"**Showing {len(df_filtered)} of {len(df_dokumen)} documents**")
    
    display_cols = ['document', 'phase', 'pic_role', 'target_week', 'status', 'progress']
    df_display = df_filtered[display_cols].copy()
    df_display['progress'] = df_display['progress'].apply(lambda x: f"{x:.0f}%")
    st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)

# =============================================
# TAB 6: LOG
# =============================================
with tabs[5]:
    st.markdown('<div class="section-title">📝 Activity Log</div>', unsafe_allow_html=True)
    
    if not data_loaded or df_log.empty:
        st.markdown(alert_box("No log data available.", "warning"), unsafe_allow_html=True)
    else:
        max_week = int(df_log["week_no"].max())
        week_pick = st.multiselect("📅 Filter Week", list(range(1, max_week + 1)), default=[max_week])
        df_view = df_log[df_log["week_no"].isin(week_pick)]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(kpi_card("Updates", len(df_view), "Filtered"), unsafe_allow_html=True)
        with col2:
            st.markdown(kpi_card("Documents", df_view["document"].nunique(), "Updated"), unsafe_allow_html=True)
        with col3:
            st.markdown(kpi_card("Total Logs", len(df_log), "All time"), unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">📋 Log Entries</div>', unsafe_allow_html=True)
        show_cols = [c for c in ["timestamp", "week_no", "document", "status", "progress", "pic_role"] if c in df_view.columns]
        st.dataframe(df_view.sort_values("timestamp", ascending=False)[show_cols], use_container_width=True, hide_index=True, height=400)

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.95rem; padding: 1rem 0;">
    📊 <strong>Manajemen Proyek - Rizki Fermanta</strong> | Office Supplies Management System | © 2026
</div>
""", unsafe_allow_html=True)
