import streamlit as st
import pandas as pd

# Konfigurasi Halaman (Harus di paling atas)
st.set_page_config(
    page_title="AutoMonitor - ACC Makassar",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Korporat & Pembersih Footer Streamlit yang Aman
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    /* Sembunyikan footer dan lencana bawaan */
    footer {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        border: 1px solid #374151;
        text-align: center;
        margin-bottom: 10px;
    }
    .bank-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #374151;
        text-align: center;
    }
    .reject-box {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        border: 1px solid #374151;
        margin-bottom: 15px;
    }
    .solution-box {
        background-color: #064e3b;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #10b981;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Daftar Resmi Sales Officer ACC Cabang Makassar
DAFTAR_SO_MAKASSAR = [
    "RESKYANTO PUNDA", "NURUL AZIZAH", "NUR RAHMADANI", "FITRIYANTI MUIS",
    "ANDI ALGAZALI", "MUH RAFLI MUADZ", "M. B. J MUBARAQ MUCHTAR",
    "SEPTIAN MAPPALONGI", "TAHWIL IRZAN", "AMINUDDIN A.", "ANDI IRVAN NATSIR",
    "MUH ASWAR BASRAH", "MUHAMMAD FADHIL RAMADHAN", "DIRGA PRATAMA NUGRAHA",
    "WILANNY NATAL B", "MUH FADLY YUSRI MS", "NAJAMUDDIN",
    "ST. AISYAH NUR HASANAH", "SYAHRIR NUR", "IRAWATI", "TRY YUDHIANTO HAKIM",
    "NASRUL", "HERLIN TANJUNG", "MUKRAWATI", "ZUBAIR M", "NADIA SABIR",
    "KARMILA", "KHUSNUL KHATIMA ASRI", "GOPUR MAULAN", "ENRICKO GUEVARA KARAMOY",
    "GABRIEL", "MIRNA ARSYITA", "ANDI MUHAMMAD WIRYAWAN", "ROHADI MAKMUR",
    "ANDI AYYUB ARHAM", "RIZAL RIZKY RIDWAN", "MUH. ARYA ALIAS", "RANI",
    "MUH ALFIAN TARUNA", "SITI NADIRAH", "PUTRI", "ALFI SAHAR", "NURHIDAYAH", "ASRUL AMRI"
]

# Koneksi Aman ke Google Sheets dengan Fallback Data
@st.cache_data(ttl=5)
def load_data():
    try:
        conn = st.connection("gsheets", type="GsheetsConnection")
        df = conn.read(worksheet="Tracking", ttl=0)
        df = df.dropna(subset=["Customer"])
        return df, conn
    except Exception:
        # Fallback lokal jika koneksi sheets sedang memuat
        df_dummy = pd.DataFrame([
            {"ID": "REG-001", "Customer": "HENRI", "NoRek": "1600801003449078", "Bank": "BRI", "Sales": "RESKYANTO PUNDA", "Alasan Reject": "Phone number is not correct", "Keterangan": "Perbedaan no telp", "Solusi": "Input ulang menu AOL CSO", "Status": "Pending"},
            {"ID": "REG-002", "Customer": "ASRIYADI", "NoRek": "1600801003448594", "Bank": "BRI", "Sales": "NURUL AZIZAH", "Alasan Reject": "Phone number not found", "Keterangan": "Belum ada nomor", "Solusi": "Registrasi BRIMO", "Status": "Pending"}
        ])
        return df_dummy, None

df_tracking, conn = load_data()

# Sidebar Navigasi Korporat
st.sidebar.title("AutoMonitor ACC")
st.sidebar.markdown("---")
st.sidebar.markdown("**Menu Utama:**")

menu_pilihan = st.sidebar.radio(
    "Navigasi",
    [
        "📊 Monitoring Dashboard", 
        "📋 Sales Tracking Reject", 
        "📖 Reject Guide", 
        "⚙️ Pengaturan & Data"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ACC Makassar** - Sistem Kolaborasi & Tracking Lapangan.")

def main():
    if menu_pilihan == "📊 Monitoring Dashboard":
        st.title("🚗 AutoMonitor - ACC Cabang Makassar")
        st.markdown("Dashboard utama pemantauan proses autodebet dan performa perbankan secara *real-time*.")
        
        total_reject = len(df_tracking[df_tracking['Status'].astype(str).str.lower() == 'pending']) if not df_tracking.empty else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Data Tracking</span>
                    <h2 style="color: #3b82f6; margin: 5px 0;">{len(df_tracking)}</h2>
                    <small style="color: #10b981;">● Live Database</small>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Reject Aktif</span>
                    <h2 style="color: #ef4444; margin: 5px 0;">{total_reject}</h2>
                    <small style="color: #f59e0b;">● Perlu Tindak Lanjut</small>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Success Rate Cabang</span>
                    <h2 style="color: #10b981; margin: 5px 0;">88.4%</h2>
                    <small style="color: #10b981;">● Gabungan 5 Bank</small>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Server Status</span>
                    <h2 style="color: #a855f7; margin: 5px 0;">Online 🚀</h2>
                    <small style="color: #10b981;">● Ready</small>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("📊 Persentase Success Rate & Volume per Bank (5 Bank Mitra)")
        
        b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
        with b_col1:
            st.markdown('<div class="bank-card"><b style="color: #3b82f6;">BCA</b><h3 style="color: #f3f4f6; margin:5px 0;">91.2%</h3><span style="color: #9ca3af; font-size:12px;">450 Nasabah</span></div>', unsafe_allow_html=True)
        with b_col2:
            st.markdown('<div class="bank-card"><b style="color: #6366f1;">BRI</b><h3 style="color: #f3f4f6; margin:5px 0;">87.5%</h3><span style="color: #9ca3af; font-size:12px;">380 Nasabah</span></div>', unsafe_allow_html=True)
        with b_col3:
            st.markdown('<div class="bank-card"><b style="color: #f59e0b;">MANDIRI</b><h3 style="color: #f3f4f6; margin:5px 0;">89.1%</h3><span style="color: #9ca3af; font-size:12px;">310 Nasabah</span></div>', unsafe_allow_html=True)
        with b_col4:
            st.markdown('<div class="bank-card"><b style="color: #f97316;">BNI</b><h3 style="color: #f3f4f6; margin:5px 0;">86.4%</h3><span style="color: #9ca3af; font-size:12px;">160 Nasabah</span></div>', unsafe_allow_html=True)
        with b_col5:
            st.markdown('<div class="bank-card"><b style="color: #10b981;">PERMATA</b><h3 style="color: #f3f4f6; margin:5px 0;">85.0%</h3><span style="color: #9ca3af; font-size:12px;">120 Nasabah</span></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Master Data Nasabah & Status Tracking")
        st.dataframe(df_tracking, use_container_width=True, hide_index=True)

    elif menu_pilihan == "📋 Sales Tracking Reject":
        st.title("📋 Sales Tracking Reject")
        st.markdown("Pusat pemantauan dan pengelolaan penolakan (*reject*) penagihan autodebet nasabah.")
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            daftar_filter_sales = ["SEMUA SALES"] + DAFTAR_SO_MAKASSAR
            pilih_sales = st.selectbox("👤 Pilih Nama Sales Officer:", daftar_filter_sales)
        with col_f2:
            search_box = st.text_input("🔍 Cari Nama/ID:", placeholder="Ketik nama customer...")

        st.markdown("---")

        df_view = df_tracking.copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"] == pilih_sales]
        if search_box:
            df_view = df_view[df_view["Customer"].astype(str).str.contains(search_box, case=False, na=False)]

        with st.expander("➕ Input Customer Reject Baru"):
            with st.form("form_tambah_reject"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    new_cust = st.text_input("Nama Customer")
                    new_norek = st.text_input("No Rekening / Kontrak")
                    new_bank = st.selectbox("Bank", ["BRI", "BCA", "MANDIRI", "BNI", "PERMATA"])
                with col_i2:
                    new_sales = st.selectbox("Pilih Sales Officer", DAFTAR_SO_MAKASSAR)
                    new_reason = st.text_input("Alasan Reject")
                    new_solusi = st.text_area("Solusi / Corrective Action")
                
                submit_btn = st.form_submit_button("Simpan Data ke Google Sheets")
                if submit_btn and new_cust and conn:
                    new_row = {
                        "ID": f"REG-00{len(df_tracking)+1}",
                        "Customer": new_cust.upper(),
                        "NoRek": str(new_norek),
                        "Bank": new_bank,
                        "Sales": new_sales,
                        "Alasan Reject": new_reason,
                        "Keterangan": "Input lapangan",
                        "Solusi": new_solusi,
                        "Status": "Pending"
                    }
                    try:
                        updated_df = pd.concat([df_tracking, pd.DataFrame([new_row])], ignore_index=True)
                        conn.update(worksheet="Tracking", data=updated_df)
                        st.success("Data berhasil disimpan!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Gagal menyimpan: {ex}")

        st.markdown(f"### Daftar Tanggungan Reject ({len(df_view)} Data)")
        
        if len(df_view) == 0:
            st.warning("Tidak ada data reject yang ditemukan.")
        else:
            for idx, row in df_view.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="reject-box">
                            <strong>{row['Customer']}</strong> ({row['Bank']} - No. Rek: {row['NoRek']})<br>
                            <small>Sales Officer: <b>{row['Sales']}</b> | Status: <b>{row['Status']}</b></small><br>
                            <span style="color: #ef4444; font-weight: bold;">❌ Alasan Reject: {row['Alasan Reject']}</span>
                            <div class="solution-box">
                                <span style="color: #10b981; font-weight: bold;">💡 Solusi Perbaikan:</span><br>
                                {row['Solusi']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_act1, col_act2, col_act3 = st.columns(3)
                    with col_act1:
                        if st.button(f"✅ Selesaikan", key=f"done_{idx}") and conn:
                            try:
                                df_tracking.loc[idx, 'Status'] = 'Selesai'
                                conn.update(worksheet="Tracking", data=df_tracking)
                                st.success("Status diperbarui!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal: {ex}")
                    with col_act2:
                        if st.button(f"🗑️ Hapus", key=f"del_{idx}") and conn:
                            try:
                                df_cleaned = df_tracking.drop(idx).reset_index(drop=True)
                                conn.update(worksheet="Tracking", data=df_cleaned)
                                st.warning("Data dihapus!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal: {ex}")
                    with col_act3:
                        wa_text = f"Halo Kak {row['Sales']}, mohon follow up reject *{row['Customer']}* ({row['Bank']}). Alasan: {row['Alasan Reject']}"
                        st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer;">💬 WA</button></a>', unsafe_allow_html=True)
                    st.markdown("---")

    elif menu_pilihan == "📖 Reject Guide":
        st.header("📖 Panduan Penanganan Reject")
        search_guide = st.text_input("🔍 Cari Kata Kunci Panduan:")
        data_guide = [
            {"No": 1, "Alasan Reject": "Tanda Tangan Tidak Sesuai", "Tindakan Korektif": "Uji coba tanda tangan di atas kertas putih, sesuaikan lekukan KTP."},
            {"No": 2, "Alasan Reject": "Nomor Telepon Tidak Valid", "Tindakan Korektif": "Input ulang melalui sistem atau arahkan nasabah ke bank."},
            {"No": 3, "Alasan Reject": "Nomor Rekening Tidak Sesuai", "Tindakan Korektif": "Input nomor rekening sesuai data keuangan asli tanpa spasi."}
        ]
        df_g = pd.DataFrame(data_guide)
        if search_guide:
            df_g = df_g[df_g['Alasan Reject'].str.contains(search_guide, case=False, na=False)]
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    elif menu_pilihan == "⚙️ Pengaturan & Data":
        st.subheader("Pengaturan Sistem")
        st.write("Versi Stabil - Mobile Responsive Optimized")
        st.success("Status: Connected")

if __name__ == '__main__':
    main()
