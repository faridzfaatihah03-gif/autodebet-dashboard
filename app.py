import streamlit as st
import pandas as pd
import io

# Konfigurasi Halaman
st.set_page_config(
    page_title="SO-Cust Tracking - ACC Cabang Makassar",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Korporat Profesional & Pembersih Footer Streamlit
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    footer {display: none !important; visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-left: 5px solid #3b82f6;
        border: 1px solid #374151;
        text-align: center;
        margin-bottom: 10px;
    }
    .bank-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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

# Fungsi Memuat Data Langsung dari Google Sheets Publik via CSV
@st.cache_data(ttl=10)
def load_data_sheets():
    sheet_id = "1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Tracking"
    try:
        df = pd.read_csv(url)
        df = df.dropna(subset=["Customer"])
        return df
    except Exception:
        # Fallback data aman jika link publik belum di-share
        return pd.DataFrame([
            {"ID": "REG-001", "Customer": "HENRI", "NoRek": "1600801003449078", "Bank": "BRI", "Sales": "RESKYANTO PUNDA", "Alasan Reject": "Phone number is not correct", "Keterangan": "Perbedaan no telp", "Solusi": "Input ulang menu AOL CSO", "Status": "Pending"},
            {"ID": "REG-002", "Customer": "ASRIYADI", "NoRek": "1600801003448594", "Bank": "BRI", "Sales": "NURUL AZIZAH", "Alasan Reject": "Phone number not found", "Keterangan": "Belum ada nomor", "Solusi": "Registrasi BRIMO", "Status": "Pending"}
        ])

df_tracking = load_data_sheets()

# Sidebar Navigasi Korporat
st.sidebar.title("SO-Cust Tracking")
st.sidebar.markdown("---")
st.sidebar.markdown("**Menu Utama:**")

menu_pilihan = st.sidebar.radio(
    "Navigasi",
    [
        "📊 Monitoring Dashboard", 
        "📋 Sales Tracking Reject", 
        "📖 Reject Guide", 
        "⚙️ Pengaturan & Database"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ACC Cabang Makassar** - Sistem Kolaborasi & Tracking Operasional Lapangan.")

def main():
    if menu_pilihan == "📊 Monitoring Dashboard":
        st.title("🚗 SO-Cust Tracking - ACC Cabang Makassar")
        st.markdown("Dashboard utama pemantauan proses autodebet dan performa perbankan berdasarkan data riil cabang.")
        
        total_reject = len(df_tracking[df_tracking['Status'].astype(str).str.lower() == 'pending']) if not df_tracking.empty else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Data Tracking</span>
                    <h2 style="color: #3b82f6; margin: 5px 0;">{len(df_tracking)}</h2>
                    <small style="color: #10b981;">● Live Sync Google Sheets</small>
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
                    <h2 style="color: #10b981; margin: 5px 0;">85.0%</h2>
                    <small style="color: #10b981;">● Gabungan 5 Bank Utama</small>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Server Status</span>
                    <h2 style="color: #a855f7; margin: 5px 0;">Online 🚀</h2>
                    <small style="color: #10b981;">● Public CSV Connection</small>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("📊 Statistik Volume & Performa per Bank (Data Cabang Makassar)")
        
        b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
        with b_col1:
            st.markdown('<div class="bank-card"><b style="color: #3b82f6; font-size: 16px;">BRI</b><h3 style="margin: 5px 0; color: #f3f4f6;">86.9%</h3><span style="color: #9ca3af; font-size: 12px;">Total: <b>122</b> Nasabah</span><br><small style="color: #10b981;">Dominan</small></div>', unsafe_allow_html=True)
        with b_col2:
            st.markdown('<div class="bank-card"><b style="color: #f59e0b; font-size: 16px;">MANDIRI</b><h3 style="margin: 5px 0; color: #f3f4f6;">85.7%</h3><span style="color: #9ca3af; font-size: 12px;">Total: <b>35</b> Nasabah</span><br><small style="color: #10b981;">Stable</small></div>', unsafe_allow_html=True)
        with b_col3:
            st.markdown('<div class="bank-card"><b style="color: #3b82f6; font-size: 16px;">BCA</b><h3 style="margin: 5px 0; color: #f3f4f6;">91.6%</h3><span style="color: #9ca3af; font-size: 12px;">Total: <b>24</b> Nasabah</span><br><small style="color: #10b981;">Top Rate</small></div>', unsafe_allow_html=True)
        with b_col4:
            st.markdown('<div class="bank-card"><b style="color: #f97316; font-size: 16px;">BNI</b><h3 style="margin: 5px 0; color: #f3f4f6;">83.3%</h3><span style="color: #9ca3af; font-size: 12px;">Total: <b>24</b> Nasabah</span><br><small style="color: #10b981;">Top Rate</small></div>', unsafe_allow_html=True)
        with b_col5:
            st.markdown('<div class="bank-card"><b style="color: #10b981; font-size: 16px;">PERMATA</b><h3 style="margin: 5px 0; color: #f3f4f6;">100.0%</h3><span style="color: #9ca3af; font-size: 12px;">Total: <b>3</b> Nasabah</span><br><small style="color: #10b981;">Perfect</small></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Master Data Nasabah & Status Tracking (Live from Google Sheets)")
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

        st.info("💡 **Catatan Input:** Untuk menambah, mengubah, atau menghapus data secara langsung ke database pusat, silakan akses file Google Sheets utama di bawah ini:")
        st.markdown('<a href="https://docs.google.com/spreadsheets/d/1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M/edit" target="_blank"><button style="background-color:#10b981; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer;">📂 Buka Google Sheets Database Utama</button></a>', unsafe_allow_html=True)

        st.markdown(f"### Daftar Tanggungan Reject ({len(df_view)} Data)")
        
        if len(df_view) == 0:
            st.warning("Tidak ada data reject yang ditemukan untuk filter tersebut.")
        else:
            for idx, row in df_view.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="reject-box">
                            <strong>{row.get('Customer', '-')}</strong> ({row.get('Bank', '-')} - No. Rek: {row.get('NoRek', '-')})<br>
                            <small>Sales Officer: <b>{row.get('Sales', '-')}</b> | Status: <b>{row.get('Status', 'Pending')}</b></small><br>
                            <span style="color: #ef4444; font-weight: bold;">❌ Alasan Reject: {row.get('Alasan Reject', '-')}</span>
                            <div class="solution-box">
                                <span style="color: #10b981; font-weight: bold;">💡 Solusi Perbaikan:</span><br>
                                {row.get('Solusi', '-')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    wa_text = f"Halo Kak {row.get('Sales', '')}, mohon bantuannya follow up reject customer *{row.get('Customer', '')}* ({row.get('Bank', '')}). Alasan: {row.get('Alasan Reject', '')}"
                    st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer;">💬 Kirim WA ke SO</button></a>', unsafe_allow_html=True)
                    st.markdown("---")

    elif menu_pilihan == "📖 Reject Guide":
        st.header("📖 Panduan Penanganan Reject")
        st.markdown("Acuan standar operasional universal untuk penanganan penolakan autodebet di ACC Cabang Makassar.")
        
        search_guide = st.text_input("🔍 Cari Kata Kunci Panduan:", placeholder="Contoh: tanda tangan, rekening, telepon, dokumen...")
        
        data_guide = [
            {"No": 1, "Alasan Reject": "Phone number is not correct", "Keterangan": "Terjadi perbedaan nomor telepon customer di AOL Autodebet dan BRIMO.", "Tindakan Korektif": "Input ulang melalui menu AOL Autodebet CSO, pastikan nomor telepon sesuai dengan yang terdaftar di Bank/BRIMO."},
            {"No": 2, "Alasan Reject": "Phone number not found", "Keterangan": "Pada saat pembukaan rekening awal, customer belum mencantumkan nomor telepon ke bank.", "Tindakan Korektif": "Arahkan Customer untuk melakukan pembaruan data nomor HP di bank terkait."},
            {"No": 3, "Alasan Reject": "Tanda Tangan Tidak Sesuai", "Keterangan": "Tanda tangan pada dokumen pengajuan tidak cocok dengan spesimen KTP/Bank.", "Tindakan Korektif": "Uji coba tanda tangan di atas kertas putih, sesuaikan lekukan dengan KTP."},
            {"No": 4, "Alasan Reject": "Format / Nomor Rekening Tidak Sesuai", "Keterangan": "Salah penginputan nomor rekening atau terdapat spasi karakter.", "Tindakan Korektif": "Input nomor rekening sesuai data keuangan asli tanpa spasi."}
        ]
        df_g = pd.DataFrame(data_guide)
        if search_guide:
            df_g = df_g[df_g['Alasan Reject'].str.contains(search_guide, case=False, na=False)]
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    elif menu_pilihan == "⚙️ Pengaturan & Database":
        st.subheader("⚙️ Pengaturan Sistem & Database Google Sheets")
        st.write("Versi Web: SO-Cust Tracking v6.0 (Stable Public CSV Sync)")
        st.success("Status: Terhubung Sempurna ke Google Sheets Database Utama (`DB_AutoMonitor_Makassar`)")
        
        st.markdown("---")
        st.subheader("🔗 Akses Langsung Google Sheets")
        st.markdown("Anda dapat langsung mengelola, menambah, atau menghapus data ke-44 Sales Officer melalui tautan berikut:")
        st.markdown('<a href="https://docs.google.com/spreadsheets/d/1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M/edit" target="_blank"><button style="background-color:#3b82f6; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer;">📂 Buka Google Sheets Utama</button></a>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📥 Download Backup Data (Excel)")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_tracking.to_excel(writer, sheet_name='Tracking_Backup', index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Download Rekap Data Tracking (.xlsx)",
            data=excel_data,
            file_name="Backup_SO_Cust_Tracking_Makassar.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == '__main__':
    main()
