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
    layout="wide"
)

# =============================================
# KONFIGURASI DATA
# =============================================
LOG_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEpBx0Eg1x3unaxVVQWJVFfzmH9Z8qKQPevp87cnsfP-nhyNYfhQvVc3Vpd0sDfkNRaNs7R4VH1nOa/pub?gid=1285157492&single=true&output=csv"

PROJECT_START = date(2025, 11, 10)  # minggu ke-1 dimulai 10 Nov 2025

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
STATUS_COLORS = {"Selesai": "#28a745", "Proses": "#ffc107", "Belum": "#dc3545"}

# =============================================
# HELPER FUNCTIONS
# =============================================
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to lowercase and rename common variations."""
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
    """Load log data from Google Sheets CSV."""
    df = pd.read_csv(url)
    df = normalize_columns(df)
    
    # Check required columns
    required = {"timestamp", "week_no", "document", "status", "progress"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing}. Tersedia: {list(df.columns)}")
    
    # Parse data types
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "week_start" in df.columns:
        df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce")
    
    df["week_no"] = pd.to_numeric(df["week_no"], errors="coerce")
    df["progress"] = pd.to_numeric(df["progress"], errors="coerce")
    
    # Clean status
    df["status"] = df["status"].astype(str).str.strip().str.title()
    df.loc[~df["status"].isin(STATUS_ORDER), "status"] = "Proses"
    
    # Clean document
    df["document"] = df["document"].astype(str).str.strip()
    
    return df.dropna(subset=["week_no", "document"])


def compute_current_week(project_start: date) -> int:
    """Calculate current project week based on start date."""
    today = date.today()
    delta_days = (today - project_start).days
    if delta_days < 0:
        return 1
    return min(12, max(1, delta_days // 7 + 1))


def get_latest_status(df_log: pd.DataFrame, df_baseline: pd.DataFrame) -> pd.DataFrame:
    """Get latest status per document from log, merged with baseline."""
    
    # Get latest entry per document from log
    if len(df_log) > 0:
        df_latest = (
            df_log.sort_values("timestamp", ascending=True)
                  .groupby("document", as_index=False)
                  .tail(1)
        )
    else:
        df_latest = pd.DataFrame(columns=["document", "status", "progress", "timestamp", "notes"])
    
    # Start with baseline as the foundation
    df_result = df_baseline.copy()
    
    # Merge with latest log data
    if len(df_latest) > 0:
        # Select only needed columns from log to avoid conflicts
        log_cols = ["document"]
        if "status" in df_latest.columns:
            log_cols.append("status")
        if "progress" in df_latest.columns:
            log_cols.append("progress")
        if "timestamp" in df_latest.columns:
            log_cols.append("timestamp")
        if "notes" in df_latest.columns:
            log_cols.append("notes")
        if "updated_by" in df_latest.columns:
            log_cols.append("updated_by")
        if "week_no" in df_latest.columns:
            log_cols.append("week_no")
        
        df_log_subset = df_latest[log_cols].copy()
        
        # Rename columns to avoid conflicts
        rename_dict = {}
        for col in log_cols:
            if col != "document":
                rename_dict[col] = f"{col}_log"
        df_log_subset = df_log_subset.rename(columns=rename_dict)
        
        # Merge
        df_result = df_result.merge(df_log_subset, on="document", how="left")
        
        # Use log values if available, otherwise use baseline/default
        if "status_log" in df_result.columns:
            df_result["status"] = df_result["status_log"].fillna("Belum")
        else:
            df_result["status"] = "Belum"
            
        if "progress_log" in df_result.columns:
            df_result["progress"] = df_result["progress_log"].fillna(0)
        else:
            df_result["progress"] = 0
            
        if "timestamp_log" in df_result.columns:
            df_result["timestamp"] = df_result["timestamp_log"]
        
        if "notes_log" in df_result.columns:
            df_result["notes"] = df_result["notes_log"]
            
        if "updated_by_log" in df_result.columns:
            df_result["updated_by"] = df_result["updated_by_log"]
            
        if "week_no_log" in df_result.columns:
            df_result["last_update_week"] = df_result["week_no_log"]
        
        # Drop temporary columns
        cols_to_drop = [c for c in df_result.columns if c.endswith("_log")]
        df_result = df_result.drop(columns=cols_to_drop, errors="ignore")
    else:
        # No log data, use defaults
        df_result["status"] = "Belum"
        df_result["progress"] = 0
    
    return df_result


# =============================================
# LOAD DATA
# =============================================
st.title("📊 Dashboard Monitoring Proyek Office Supplies")
st.markdown("Sistem manajemen perlengkapan kantor berbasis web")

# Load log dari Google Sheets
try:
    df_log = load_log(LOG_URL)
    data_loaded = True
except Exception as e:
    st.error(f"⚠️ Gagal load data dari Google Sheets: {e}")
    st.info("Menggunakan data baseline saja (tanpa log histori)")
    df_log = pd.DataFrame(columns=["timestamp", "week_no", "document", "status", "progress", "pic_role", "updated_by", "notes"])
    data_loaded = False

# Baseline dokumen
df_baseline = pd.DataFrame(BASELINE)
df_baseline["target_date"] = df_baseline["target_week"].apply(
    lambda w: PROJECT_START + timedelta(days=(w - 1) * 7)
)

# Latest status per dokumen
df_dokumen = get_latest_status(df_log, df_baseline)

# Current week
auto_week = compute_current_week(PROJECT_START)

# =============================================
# DATA TIM (RACI) - berbasis Role
# =============================================
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

df_tim = load_tim()

# =============================================
# DATA RISIKO
# =============================================
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

df_risiko = load_risiko()

# =============================================
# DATA EVM
# =============================================
@st.cache_data
def load_evm():
    data = {
        'Minggu': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'PV': [40000, 80000, 130000, 180000, 240000, 300000, 360000, 410000, 450000, 480000, 500000, 500000],
        'EV': [40000, 75000, 125000, 170000, 230000, 290000, 0, 0, 0, 0, 0, 0],
        'AC': [45000, 85000, 140000, 195000, 260000, 330000, 0, 0, 0, 0, 0, 0]
    }
    return pd.DataFrame(data)

df_evm = load_evm()

# =============================================
# TAB NAVIGATION
# =============================================
tab_overview, tab_sdm, tab_risiko, tab_evm, tab_dokumen, tab_log = st.tabs([
    "🏠 Overview", 
    "👥 SDM", 
    "⚠️ Risiko", 
    "📈 EVM", 
    "📋 Dokumen",
    "🧾 Log Histori"
])

# =============================================
# TAB 1: OVERVIEW
# =============================================
with tab_overview:
    # Minggu saat ini
    current_week = st.number_input("📅 Minggu saat ini", min_value=1, max_value=12, value=auto_week, step=1)
    
    st.markdown("---")
    
    # Metrics
    total = len(df_dokumen)
    selesai = int((df_dokumen['status'] == 'Selesai').sum())
    proses = int((df_dokumen['status'] == 'Proses').sum())
    belum = int((df_dokumen['status'] == 'Belum').sum())
    avg_progress = float(df_dokumen['progress'].mean())
    
    # Overdue calculation
    df_dokumen["overdue"] = (current_week > df_dokumen["target_week"]) & (df_dokumen["status"] != "Selesai")
    overdue_count = int(df_dokumen["overdue"].sum())
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📄 Total Dokumen", total)
    with col2:
        st.metric("✅ Selesai", selesai, f"{(selesai/total)*100:.0f}%")
    with col3:
        st.metric("🔄 Proses", proses, f"{(proses/total)*100:.0f}%")
    with col4:
        st.metric("⏳ Belum", belum, f"-{(belum/total)*100:.0f}%", delta_color="inverse")
    with col5:
        st.metric("⚠️ Overdue", overdue_count, delta_color="inverse" if overdue_count > 0 else "off")
    
    st.markdown("---")
    
    # Progress Bar
    st.subheader("📈 Progress Keseluruhan")
    st.progress(int(avg_progress) / 100)
    st.markdown(f"**{avg_progress:.1f}%** rata-rata progress dokumen")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Status Dokumen (RAG)")
        status_count = df_dokumen['status'].value_counts().reindex(STATUS_ORDER, fill_value=0).reset_index()
        status_count.columns = ['Status', 'Jumlah']
        fig = px.pie(status_count, values='Jumlah', names='Status', 
                     color='Status', color_discrete_map=STATUS_COLORS, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("👥 Beban Kerja per Role (PIC)")
        role_count = df_dokumen.groupby('pic_role').size().reset_index(name='Jumlah Tugas')
        fig2 = px.bar(role_count, x='pic_role', y='Jumlah Tugas', color='Jumlah Tugas',
                      color_continuous_scale='Blues', text='Jumlah Tugas')
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Progress per dokumen
    st.subheader("📋 Progress Setiap Dokumen")
    fig3 = px.bar(df_dokumen.sort_values('progress', ascending=True),
                  x='progress', y='document', orientation='h',
                  color='status', color_discrete_map=STATUS_COLORS, text='progress')
    fig3.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig3.update_layout(xaxis_range=[0, 110], height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Overdue Warning
    st.subheader("⚠️ Dokumen Overdue (berdasarkan target minggu)")
    overdue_df = df_dokumen[df_dokumen["overdue"]].copy()
    if overdue_df.empty:
        st.success("✅ Tidak ada dokumen overdue. Semua sesuai jadwal!")
    else:
        for _, row in overdue_df.iterrows():
            weeks_late = current_week - row["target_week"]
            st.error(f"🔴 **{row['document']}** - Terlambat {weeks_late} minggu (target: minggu {row['target_week']}) - PIC: {row['pic_role']}")

# =============================================
# TAB 2: MANAJEMEN SDM
# =============================================
with tab_sdm:
    st.header("👥 Manajemen Sumber Daya Manusia")
    
    # Tim Overview
    st.subheader("📋 Struktur Tim Proyek (Berbasis Role)")
    st.dataframe(df_tim, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # RACI Matrix
    st.subheader("📊 Matriks RACI")
    
    raci_data = {
        'Dokumen': [
            'Project Charter', 
            'Gantt Chart / Schedule', 
            'SRS', 
            'Use Case Diagram + Deskripsi', 
            'ERD + Data Dictionary',
            'Wireframe / Mockup UI', 
            'Risk Register', 
            'User Manual'
        ],
        'PM': ['R/A', 'R/A', 'C', 'C', 'I', 'I', 'R/A', 'C'],
        'BA/SA': ['C', 'C', 'R/A', 'R/A', 'C', 'C', 'C', 'R/A'],
        'UI/UX': ['I', 'I', 'C', 'C', 'I', 'R/A', 'I', 'I'],
        'Backend/DB': ['I', 'I', 'C', 'C', 'R/A', 'I', 'I', 'C']
    }
    df_raci = pd.DataFrame(raci_data)
    
    # Styling RACI
    def style_raci(val):
        if 'A' in str(val):
            return 'background-color: #ff6b6b; color: white; font-weight: bold'
        elif 'R' in str(val):
            return 'background-color: #4ecdc4; color: white; font-weight: bold'
        elif val == 'C':
            return 'background-color: #ffe66d; color: black'
        elif val == 'I':
            return 'background-color: #95e1d3; color: black'
        return ''
    
    st.dataframe(df_raci.style.map(style_raci, subset=['PM', 'BA/SA', 'UI/UX', 'Backend/DB']),
                 use_container_width=True, hide_index=True)
    
    st.markdown("""
    **Keterangan:**
    - 🔴 **R/A (Responsible/Accountable)**: Pelaksana & penanggung jawab utama
    - 🟢 **R (Responsible)**: Pelaksana tugas
    - 🟡 **C (Consulted)**: Dimintai pendapat
    - 🟢 **I (Informed)**: Diberi informasi
    """)
    
    st.markdown("---")
    
    # Workload Chart
    st.subheader("📊 Distribusi Beban Kerja per Role")
    
    # Hitung tugas per role dari data dokumen
    workload_data = []
    for role in ['PM', 'BA/SA', 'UI/UX', 'Backend/DB']:
        role_docs = df_dokumen[df_dokumen['pic_role'] == role]
        workload_data.append({
            'Role': role,
            'Selesai': int((role_docs['status'] == 'Selesai').sum()),
            'Proses': int((role_docs['status'] == 'Proses').sum()),
            'Belum': int((role_docs['status'] == 'Belum').sum())
        })
    
    df_workload = pd.DataFrame(workload_data)
    workload_melted = df_workload.melt(id_vars=['Role'], var_name='Status', value_name='Jumlah')
    
    fig = px.bar(workload_melted, x='Role', y='Jumlah', color='Status',
                 barmode='stack', color_discrete_map={
                     'Selesai': '#28a745',
                     'Proses': '#ffc107',
                     'Belum': '#dc3545'
                 })
    st.plotly_chart(fig, use_container_width=True)

# =============================================
# TAB 3: MANAJEMEN RISIKO
# =============================================
with tab_risiko:
    st.header("⚠️ Manajemen Risiko Proyek")
    
    # Risk Summary
    col1, col2, col3 = st.columns(3)
    
    open_risks = len(df_risiko[df_risiko['Status Risiko'] == 'Open'])
    mitigated = len(df_risiko[df_risiko['Status Risiko'] == 'Mitigated'])
    high_prob = len(df_risiko[df_risiko['Probabilitas'] == 'Tinggi'])
    
    with col1:
        st.metric("🔴 Risiko Open", open_risks)
    with col2:
        st.metric("✅ Risiko Mitigated", mitigated)
    with col3:
        st.metric("⚠️ Probabilitas Tinggi", high_prob)
    
    st.markdown("---")
    
    # Risk Register Table
    st.subheader("📋 Risk Register")
    st.dataframe(df_risiko, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Matriks Risiko")
        fig = px.scatter(df_risiko, x='Dampak', y='Probabilitas', 
                         size='Skor', color='Status Risiko',
                         hover_name='Risiko', size_max=40,
                         color_discrete_map={'Open': '#dc3545', 'Mitigated': '#28a745'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("📈 Distribusi Strategi Respon")
        strategi_count = df_risiko['Strategi'].value_counts().reset_index()
        strategi_count.columns = ['Strategi', 'Jumlah']
        fig2 = px.pie(strategi_count, values='Jumlah', names='Strategi', hole=0.3)
        st.plotly_chart(fig2, use_container_width=True)

# =============================================
# TAB 4: EVM & CONTROLLING
# =============================================
with tab_evm:
    st.header("📈 Earned Value Management & Controlling")
    
    # Current Week (from overview)
    current_week_evm = st.number_input("Minggu evaluasi EVM", min_value=1, max_value=12, value=min(6, auto_week), step=1, key="evm_week")
    
    # Calculate EVM metrics
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
        st.warning("Data EVM belum tersedia untuk minggu ini.")
        PV, EV, AC = 0, 0, 0
        SV, CV, SPI, CPI, EAC, VAC = 0, 0, 0, 0, BAC, 0
    
    st.markdown("---")
    
    # Metrics Display
    st.subheader(f"📊 Status Proyek (Minggu ke-{current_week_evm})")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 BAC (Budget)", f"Rp {BAC:,}")
        st.metric("📅 Planned Value (PV)", f"Rp {PV:,}")
    
    with col2:
        st.metric("✅ Earned Value (EV)", f"Rp {EV:,}")
        st.metric("💸 Actual Cost (AC)", f"Rp {AC:,}")
    
    with col3:
        sv_delta = "On Schedule" if SV >= 0 else "Behind Schedule"
        cv_delta = "Under Budget" if CV >= 0 else "Over Budget"
        st.metric("📆 Schedule Variance (SV)", f"Rp {SV:,}", sv_delta, 
                  delta_color="normal" if SV >= 0 else "inverse")
        st.metric("💵 Cost Variance (CV)", f"Rp {CV:,}", cv_delta,
                  delta_color="normal" if CV >= 0 else "inverse")
    
    with col4:
        spi_status = "Baik" if SPI >= 1 else "Terlambat"
        cpi_status = "Baik" if CPI >= 1 else "Boros"
        st.metric("⏱️ SPI", f"{SPI:.2f}", spi_status,
                  delta_color="normal" if SPI >= 1 else "inverse")
        st.metric("💹 CPI", f"{CPI:.2f}", cpi_status,
                  delta_color="normal" if CPI >= 1 else "inverse")
    
    st.markdown("---")
    
    # EVM Chart
    st.subheader("📈 Grafik EVM (S-Curve)")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_evm['Minggu'], y=df_evm['PV'], 
                             mode='lines+markers', name='Planned Value (PV)',
                             line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=df_evm_current['Minggu'], y=df_evm_current['EV'], 
                             mode='lines+markers', name='Earned Value (EV)',
                             line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df_evm_current['Minggu'], y=df_evm_current['AC'], 
                             mode='lines+markers', name='Actual Cost (AC)',
                             line=dict(color='red')))
    
    fig.update_layout(
        xaxis_title='Minggu',
        yaxis_title='Nilai (Rp)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast & RAG
    col_forecast1, col_forecast2 = st.columns(2)
    
    with col_forecast1:
        st.subheader("🔮 Forecast / Proyeksi")
        st.info(f"""
        **Estimate at Completion (EAC):** Rp {EAC:,.0f}
        
        **Variance at Completion (VAC):** Rp {VAC:,.0f}
        
        **Interpretasi:** {"Proyek diperkirakan sesuai budget" if VAC >= 0 else f"Proyek diperkirakan over budget Rp {abs(VAC):,.0f}"}
        """)
    
    with col_forecast2:
        st.subheader("🚦 Status RAG")
        if SPI >= 0.95 and CPI >= 0.95:
            st.success("🟢 **GREEN** - Proyek berjalan sesuai rencana")
        elif SPI >= 0.8 and CPI >= 0.8:
            st.warning("🟡 **AMBER** - Proyek memerlukan perhatian")
        else:
            st.error("🔴 **RED** - Proyek memerlukan tindakan korektif segera")
    
    st.markdown("---")
    
    # Change Control Log
    st.subheader("📝 Change Request Log")
    cr_data = {
        'CR ID': ['CR-001', 'CR-002'],
        'Deskripsi': ['Penambahan fitur notifikasi email', 'Perubahan desain UI dashboard'],
        'Diajukan': ['2025-11-20', '2025-11-25'],
        'Status': ['Approved', 'Pending Review'],
        'Dampak Biaya': ['Rp 50.000', 'Rp 0'],
        'Dampak Waktu': ['+3 hari', '+1 hari']
    }
    st.dataframe(pd.DataFrame(cr_data), use_container_width=True, hide_index=True)

# =============================================
# TAB 5: DATA DOKUMEN
# =============================================
with tab_dokumen:
    st.header("📋 Data Dokumen Proyek")
    
    # Filter
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        status_filter = st.multiselect("Filter Status:", STATUS_ORDER, default=STATUS_ORDER)
    with col_filter2:
        role_list = sorted(df_dokumen['pic_role'].dropna().unique().tolist())
        role_filter = st.multiselect("Filter PIC Role:", role_list, default=role_list)
    
    df_filtered = df_dokumen[
        (df_dokumen['status'].isin(status_filter)) & 
        (df_dokumen['pic_role'].isin(role_filter))
    ].copy()
    
    # Table - select available columns
    available_cols = df_filtered.columns.tolist()
    display_cols = []
    for col in ['document', 'phase', 'pic_role', 'target_week', 'target_date', 'status', 'progress', 'timestamp', 'notes']:
        if col in available_cols:
            display_cols.append(col)
    
    df_display = df_filtered[display_cols].copy()
    
    # Format columns
    if 'target_date' in df_display.columns:
        df_display['target_date'] = pd.to_datetime(df_display['target_date']).dt.strftime('%d/%m/%Y')
    if 'progress' in df_display.columns:
        df_display['progress'] = df_display['progress'].astype(int).astype(str) + '%'
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Deadline Warning (berdasarkan target minggu)
    st.subheader("⚠️ Target Deadline Terdekat")
    
    current_week_dok = auto_week
    df_upcoming = df_dokumen[
        (df_dokumen['status'] != 'Selesai') & 
        (df_dokumen['target_week'] >= current_week_dok)
    ].sort_values('target_week')
    
    if df_upcoming.empty:
        st.success("✅ Semua dokumen sudah selesai atau tidak ada deadline mendatang.")
    else:
        for _, row in df_upcoming.head(5).iterrows():
            weeks_left = row['target_week'] - current_week_dok
            if weeks_left <= 0:
                st.error(f"🔴 **{row['document']}** - Target minggu {row['target_week']} (sekarang!) - PIC: {row['pic_role']}")
            elif weeks_left <= 1:
                st.warning(f"🟡 **{row['document']}** - Target minggu {row['target_week']} ({weeks_left} minggu lagi) - PIC: {row['pic_role']}")
            else:
                st.info(f"🔵 **{row['document']}** - Target minggu {row['target_week']} ({weeks_left} minggu lagi) - PIC: {row['pic_role']}")

# =============================================
# TAB 6: LOG HISTORI
# =============================================
with tab_log:
    st.header("🧾 Log Histori (Audit Trail)")
    
    if not data_loaded or df_log.empty:
        st.warning("⚠️ Belum ada data log histori. Submit update via Google Form untuk mulai mencatat.")
    else:
        # Filter minggu
        max_week = int(df_log["week_no"].max()) if df_log["week_no"].notna().any() else 1
        week_options = list(range(1, max_week + 1))
        week_pick = st.multiselect("Filter minggu", week_options, default=[max_week])
        
        df_view = df_log[df_log["week_no"].isin(week_pick)].copy()
        
        # Summary
        col1, col2, col3 = st.columns(3)
        col1.metric("📝 Total update (filter)", len(df_view))
        col2.metric("📄 Dokumen diupdate", df_view["document"].nunique())
        col3.metric("📊 Total semua log", len(df_log))
        
        st.markdown("---")
        
        # Tabel log - show available columns
        available_log_cols = df_view.columns.tolist()
        show_cols = []
        for c in ["timestamp", "email", "week_no", "week_start", "document", "phase", "status", "progress", "pic_role", "updated_by", "notes"]:
            if c in available_log_cols:
                show_cols.append(c)
        
        st.dataframe(df_view.sort_values("timestamp", ascending=False)[show_cols], use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Chart aktivitas mingguan
        st.subheader("📈 Aktivitas Update per Minggu")
        week_counts = df_log.groupby("week_no").size().reset_index(name="jumlah_update")
        fig = px.bar(week_counts, x="week_no", y="jumlah_update", text="jumlah_update")
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title="Minggu ke-", yaxis_title="Jumlah update", height=350)
        st.plotly_chart(fig, use_container_width=True)

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 10px;'>
    📊 Dashboard Monitoring Proyek | Office Supplies Management System<br>
    Mata Kuliah: Manajemen Proyek TI | 2025<br>
    Data: Google Form (Log Histori) + Baseline Target Mingguan (Start: 10 Nov 2025)
</div>
""", unsafe_allow_html=True)
