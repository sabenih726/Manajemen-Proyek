import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Dashboard Monitoring Proyek - Office Supplies",
    page_icon="📊",
    layout="wide"
)

# =============================================
# DATA
# =============================================

# Data Dokumen
@st.cache_data
def load_dokumen():
    data = {
        'No': [1, 2, 3, 4, 5, 6, 7, 8],
        'Nama Dokumen': [
            'Project Charter', 'SRS', 'ERD Database', 'Use Case Diagram',
            'Wireframe UI/UX', 'Gantt Chart', 'Risk Register', 'User Manual'
        ],
        'Fase': [
            'Inisiasi', 'Perencanaan', 'Perencanaan', 'Perencanaan',
            'Perencanaan', 'Perencanaan', 'Perencanaan', 'Penutupan'
        ],
        'Status': ['Selesai', 'Proses', 'Proses', 'Belum', 'Belum', 'Selesai', 'Proses', 'Belum'],
        'PIC': ['Andi', 'Budi', 'Citra', 'Dani', 'Eka', 'Andi', 'Budi', 'Citra'],
        'Deadline': ['2025-01-10', '2025-01-20', '2025-01-25', '2025-01-30',
                     '2025-02-05', '2025-01-15', '2025-01-28', '2025-03-01'],
        'Progress': [100, 75, 50, 0, 0, 100, 60, 0]
    }
    df = pd.DataFrame(data)
    df['Deadline'] = pd.to_datetime(df['Deadline'])
    return df

# Data Tim (RACI)
@st.cache_data
def load_tim():
    data = {
        'Nama': ['Andi', 'Budi', 'Citra', 'Dani', 'Eka'],
        'Role': ['Project Manager', 'System Analyst', 'Database Designer', 'Developer', 'UI/UX Designer'],
        'Skill': ['Leadership, Planning', 'Analysis, Documentation', 'Database, SQL', 'Python, Laravel', 'Figma, CSS'],
        'Tugas Selesai': [2, 1, 0, 0, 0],
        'Tugas Proses': [0, 2, 1, 0, 0],
        'Tugas Belum': [0, 0, 1, 1, 1]
    }
    return pd.DataFrame(data)

# Data Risiko
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

# Data EVM
@st.cache_data
def load_evm():
    data = {
        'Minggu': [1, 2, 3, 4, 5, 6, 7, 8],
        'PV': [40000, 80000, 140000, 200000, 280000, 360000, 440000, 500000],
        'EV': [40000, 75000, 130000, 185000, 260000, 340000, 0, 0],
        'AC': [45000, 90000, 150000, 210000, 295000, 380000, 0, 0]
    }
    return pd.DataFrame(data)

df_dokumen = load_dokumen()
df_tim = load_tim()
df_risiko = load_risiko()
df_evm = load_evm()

# =============================================
# HEADER
# =============================================
st.title("📊 Dashboard Monitoring Proyek Office Supplies")
st.markdown("Sistem manajemen perlengkapan kantor berbasis web")

# =============================================
# TAB NAVIGATION (menggantikan sidebar)
# =============================================
tab_overview, tab_sdm, tab_risiko, tab_evm, tab_dokumen = st.tabs([
    "🏠 Overview", 
    "👥 SDM", 
    "⚠️ Risiko", 
    "📈 EVM", 
    "📋 Dokumen"
])

# =============================================
# TAB 1: OVERVIEW
# =============================================
with tab_overview:
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(df_dokumen)
    selesai = len(df_dokumen[df_dokumen['Status'] == 'Selesai'])
    proses = len(df_dokumen[df_dokumen['Status'] == 'Proses'])
    belum = len(df_dokumen[df_dokumen['Status'] == 'Belum'])
    avg_progress = df_dokumen['Progress'].mean()
    
    with col1:
        st.metric("📄 Total Dokumen", total)
    with col2:
        st.metric("✅ Selesai", selesai, f"{(selesai/total)*100:.0f}%")
    with col3:
        st.metric("🔄 Proses", proses, f"{(proses/total)*100:.0f}%")
    with col4:
        st.metric("⏳ Belum", belum, f"-{(belum/total)*100:.0f}%", delta_color="inverse")
    
    st.markdown("---")
    
    # Progress Bar
    st.subheader("📈 Progress Keseluruhan")
    st.progress(int(avg_progress) / 100)
    st.markdown(f"**{avg_progress:.1f}%** selesai")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Status Dokumen (RAG)")
        status_count = df_dokumen['Status'].value_counts().reset_index()
        status_count.columns = ['Status', 'Jumlah']
        colors = {'Selesai': '#28a745', 'Proses': '#ffc107', 'Belum': '#dc3545'}
        fig = px.pie(status_count, values='Jumlah', names='Status', 
                     color='Status', color_discrete_map=colors, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("👥 Beban Kerja per PIC")
        pic_count = df_dokumen.groupby('PIC').size().reset_index(name='Jumlah Tugas')
        fig2 = px.bar(pic_count, x='PIC', y='Jumlah Tugas', color='Jumlah Tugas',
                      color_continuous_scale='Blues', text='Jumlah Tugas')
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Progress per dokumen
    st.subheader("📋 Progress Setiap Dokumen")
    fig3 = px.bar(df_dokumen.sort_values('Progress', ascending=True),
                  x='Progress', y='Nama Dokumen', orientation='h',
                  color='Status', color_discrete_map=colors, text='Progress')
    fig3.update_traces(texttemplate='%{text}%', textposition='outside')
    fig3.update_layout(xaxis_range=[0, 110])
    st.plotly_chart(fig3, use_container_width=True)

# =============================================
# TAB 2: MANAJEMEN SDM
# =============================================
with tab_sdm:
    st.header("👥 Manajemen Sumber Daya Manusia")
    
    # Tim Overview
    st.subheader("📋 Struktur Tim Proyek")
    st.dataframe(df_tim, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # RACI Matrix
    st.subheader("📊 Matriks RACI")
    
    raci_data = {
        'Dokumen': ['Project Charter', 'SRS', 'ERD Database', 'Use Case', 
                    'Wireframe UI', 'Gantt Chart', 'Risk Register', 'User Manual'],
        'Andi': ['A', 'C', 'I', 'I', 'I', 'R/A', 'C', 'I'],
        'Budi': ['C', 'R/A', 'C', 'C', 'I', 'C', 'R/A', 'C'],
        'Citra': ['I', 'C', 'R/A', 'C', 'C', 'I', 'C', 'R/A'],
        'Dani': ['I', 'I', 'I', 'R/A', 'C', 'I', 'I', 'I'],
        'Eka': ['I', 'I', 'I', 'C', 'R/A', 'I', 'I', 'I']
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
    
    st.dataframe(df_raci.style.applymap(style_raci, subset=['Andi', 'Budi', 'Citra', 'Dani', 'Eka']),
                 use_container_width=True, hide_index=True)
    
    st.markdown("""
    **Keterangan:**
    - 🔴 **A (Accountable)**: Penanggung jawab utama
    - 🟢 **R (Responsible)**: Pelaksana tugas
    - 🟡 **C (Consulted)**: Dimintai pendapat
    - 🟢 **I (Informed)**: Diberi informasi
    """)
    
    # Workload Chart
    st.subheader("📊 Distribusi Beban Kerja")
    
    workload = df_tim[['Nama', 'Tugas Selesai', 'Tugas Proses', 'Tugas Belum']]
    workload_melted = workload.melt(id_vars=['Nama'], var_name='Status', value_name='Jumlah')
    
    fig = px.bar(workload_melted, x='Nama', y='Jumlah', color='Status',
                 barmode='stack', color_discrete_map={
                     'Tugas Selesai': '#28a745',
                     'Tugas Proses': '#ffc107',
                     'Tugas Belum': '#dc3545'
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
    
    # Risk Register Table
    st.subheader("📋 Risk Register")
    
    def style_risk(row):
        styles = [''] * len(row)
        if row['Status Risiko'] == 'Open':
            styles[6] = 'background-color: #ffcccc'
        else:
            styles[6] = 'background-color: #ccffcc'
        
        if row['Probabilitas'] == 'Tinggi':
            styles[2] = 'background-color: #ff6b6b; color: white'
        elif row['Probabilitas'] == 'Sedang':
            styles[2] = 'background-color: #ffc107'
        else:
            styles[2] = 'background-color: #28a745; color: white'
        
        return styles
    
    st.dataframe(df_risiko.style.apply(style_risk, axis=1), 
                 use_container_width=True, hide_index=True)
    
    # Risk Matrix
    st.subheader("📊 Matriks Risiko (Probabilitas x Dampak)")
    
    # Heatmap data
    risk_matrix = pd.DataFrame({
        'Probabilitas': ['Tinggi', 'Tinggi', 'Sedang', 'Sedang', 'Rendah', 'Rendah'],
        'Dampak': ['Tinggi', 'Sedang', 'Tinggi', 'Sedang', 'Tinggi', 'Sedang'],
        'Jumlah': [0, 1, 2, 1, 2, 0]
    })
    
    fig = px.scatter(df_risiko, x='Dampak', y='Probabilitas', 
                     size='Skor', color='Status Risiko',
                     hover_name='Risiko', size_max=40,
                     color_discrete_map={'Open': '#dc3545', 'Mitigated': '#28a745'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategi Respon
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
    
    # Current Week (simulated)
    current_week = 6
    
    # Calculate EVM metrics
    BAC = 500000
    PV = df_evm[df_evm['Minggu'] <= current_week]['PV'].iloc[-1]
    EV = df_evm[df_evm['Minggu'] <= current_week]['EV'].iloc[-1]
    AC = df_evm[df_evm['Minggu'] <= current_week]['AC'].iloc[-1]
    
    SV = EV - PV
    CV = EV - AC
    SPI = EV / PV if PV > 0 else 0
    CPI = EV / AC if AC > 0 else 0
    EAC = BAC / CPI if CPI > 0 else BAC
    VAC = BAC - EAC
    
    # Metrics Display
    st.subheader(f"📊 Status Proyek (Minggu ke-{current_week})")
    
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
    
    # EVM Chart
    st.subheader("📈 Grafik EVM (S-Curve)")
    
    df_evm_plot = df_evm[df_evm['Minggu'] <= current_week]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_evm['Minggu'], y=df_evm['PV'], 
                             mode='lines+markers', name='Planned Value (PV)',
                             line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=df_evm_plot['Minggu'], y=df_evm_plot['EV'], 
                             mode='lines+markers', name='Earned Value (EV)',
                             line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df_evm_plot['Minggu'], y=df_evm_plot['AC'], 
                             mode='lines+markers', name='Actual Cost (AC)',
                             line=dict(color='red')))
    
    fig.update_layout(
        xaxis_title='Minggu',
        yaxis_title='Nilai (Rp)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast
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
        # RAG Status
        if SPI >= 0.95 and CPI >= 0.95:
            st.success("🟢 **GREEN** - Proyek berjalan sesuai rencana")
        elif SPI >= 0.8 and CPI >= 0.8:
            st.warning("🟡 **AMBER** - Proyek memerlukan perhatian")
        else:
            st.error("🔴 **RED** - Proyek memerlukan tindakan korektif segera")
    
    # Change Control Log
    st.subheader("📝 Change Request Log")
    
    cr_data = {
        'CR ID': ['CR-001', 'CR-002'],
        'Deskripsi': ['Penambahan fitur notifikasi email', 'Perubahan desain UI dashboard'],
        'Diajukan': ['2025-01-15', '2025-01-18'],
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
    status_filter = st.multiselect("Filter Status:", df_dokumen['Status'].unique(), 
                                   default=df_dokumen['Status'].unique())
    df_filtered = df_dokumen[df_dokumen['Status'].isin(status_filter)]
    
    # Table
    def highlight_status(val):
        if val == 'Selesai':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Proses':
            return 'background-color: #fff3cd; color: #856404'
        else:
            return 'background-color: #f8d7da; color: #721c24'
    
    df_display = df_filtered.copy()
    df_display['Deadline'] = df_display['Deadline'].dt.strftime('%d/%m/%Y')
    df_display['Progress'] = df_display['Progress'].astype(str) + '%'
    
    st.dataframe(df_display.style.applymap(highlight_status, subset=['Status']),
                 use_container_width=True, hide_index=True)
    
    # Deadline Warning
    st.subheader("⚠️ Deadline Terdekat")
    today = datetime.now()
    df_upcoming = df_dokumen[(df_dokumen['Status'] != 'Selesai') & 
                             (df_dokumen['Deadline'] >= today)].sort_values('Deadline')
    
    for _, row in df_upcoming.head(5).iterrows():
        days_left = (row['Deadline'] - today).days
        if days_left <= 7:
            st.error(f"🔴 **{row['Nama Dokumen']}** - {days_left} hari lagi - PIC: {row['PIC']}")
        elif days_left <= 14:
            st.warning(f"🟡 **{row['Nama Dokumen']}** - {days_left} hari lagi - PIC: {row['PIC']}")
        else:
            st.info(f"🔵 **{row['Nama Dokumen']}** - {days_left} hari lagi - PIC: {row['PIC']}")

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 10px;'>
    📊 Dashboard Monitoring Proyek | Office Supplies Management System<br>
    Mata Kuliah: Manajemen Proyek TI | 2025
</div>
""", unsafe_allow_html=True)
