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

# Koneksi Wajib Langsung ke Google Sheets (Database Utama)
try:
    conn = st.connection("gsheets", type="GsheetsConnection")
    df_tracking = conn.read(worksheet="Tracking", ttl=0)
    df_tracking = df_tracking.dropna(subset=["Customer"])
except Exception as e:
    st.error(f"Gagal terhubung ke Google Sheets: {e}. Pastikan pengaturan Secrets di Streamlit Cloud sudah benar.")
    df_tracking = pd.DataFrame(columns=["ID", "Customer", "NoRek", "Bank", "Sales", "Alasan Reject", "Keterangan", "Solusi", "Status"])

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
        "⚙️ Pengaturan & Backup"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ACC Cabang Makassar** - Sistem Kolaborasi & Tracking Operasional Lapangan.")

def main():
    # -------------------------------------------------------------------------
    # MENU 1: MONITORING DASHBOARD
    # -------------------------------------------------------------------------
    if menu_pilihan == "📊 Monitoring Dashboard":
        st.title("🚗 SO-Cust Tracking - ACC Cabang Makassar")
        st.markdown("Dashboard utama pemantauan proses autodebet dan performa perbankan berdasarkan data riil cabang.")
        
        total_reject = len(df_tracking[df_tracking['Status'].astype(str).str.lower() == 'pending']) if not df_tracking.empty else 0
        
        # Metrik Utama dengan Bingkai
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Data Tracking (GSheets)</span>
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
                    <h2 style="color: #10b981; margin: 5px 0;">85.0%</h2>
                    <small style="color: #10b981;">● Gabungan 5 Bank Utama</small>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Server Status</span>
                    <h2 style="color: #a855f7; margin: 5px 0;">Online 🚀</h2>
                    <small style="color: #10b981;">● GSheets Direct Sync</small>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("📊 Statistik Volume & Performa per Bank (Data Cabang Makassar)")
        
        # Grid Perbankan Berdasarkan Data Riil Excel (Total 234 Nasabah)
        b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
        with b_col1:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #3b82f6; font-size: 16px;">BRI</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">86.9%</h3>
                    <span style="color: #9ca3af; font-size: 12px;">Total: <b>122</b> Nasabah</span><br>
                    <small style="color: #10b981;">Dominan</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col2:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #f59e0b; font-size: 16px;">MANDIRI</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">85.7%</h3>
                    <span style="color: #9ca3af; font-size: 12px;">Total: <b>35</b> Nasabah</span><br>
                    <small style="color: #10b981;">Stable</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col3:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #3b82f6; font-size: 16px;">BCA</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">91.6%</h3>
                    <span style="color: #9ca3af; font-size: 12px;">Total: <b>24</b> Nasabah</span><br>
                    <small style="color: #10b981;">Top Rate</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col4:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #f97316; font-size: 16px;">BNI</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">83.3%</h3>
                    <span style="color: #9ca3af; font-size: 12px;">Total: <b>24</b> Nasabah</span><br>
                    <small style="color: #10b981;">Stable</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col5:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #10b981; font-size: 16px;">PERMATA</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">100.0%</h3>
                    <span style="color: #9ca3af; font-size: 12px;">Total: <b>3</b> Nasabah</span><br>
                    <small style="color: #10b981;">Perfect</small>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Master Data Nasabah & Status Tracking (Live Google Sheets)")
        st.dataframe(df_tracking, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------------
    # MENU 2: SALES TRACKING REJECT (INTERAKTIF LANGSUNG KE SHEETS)
    # -------------------------------------------------------------------------
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

        # Tombol Tambah Data Reject Baru langsung ke Google Sheets
        with st.expander("➕ Input Customer Reject Baru"):
            with st.form("form_tambah_reject"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    new_cust = st.text_input("Nama Customer")
                    new_norek = st.text_input("No Rekening / Kontrak")
                    new_bank = st.selectbox("Bank", ["BRI", "BCA", "MANDIRI", "BNI", "PERMATA"])
                with col_i2:
                    new_sales = st.selectbox("Pilih Sales Officer Penanggung Jawab", DAFTAR_SO_MAKASSAR)
                    new_reason = st.text_input("Alasan Reject")
                    new_solusi = st.text_area("Solusi / Corrective Action")
                
                submit_btn = st.form_submit_button("Simpan ke Google Sheets")
                if submit_btn and new_cust:
                    new_row = {
                        "ID": f"REG-00{len(df_tracking)+1}",
                        "Customer": new_cust.upper(),
                        "NoRek": str(new_norek),
                        "Bank": new_bank,
                        "Sales": new_sales,
                        "Alasan Reject": new_reason,
                        "Keterangan": "Input lapangan oleh Sales Officer",
                        "Solusi": new_solusi,
                        "Status": "Pending"
                    }
                    try:
                        updated_df = pd.concat([df_tracking, pd.DataFrame([new_row])], ignore_index=True)
                        conn.update(worksheet="Tracking", data=updated_df)
                        st.success(f"Data customer **{new_cust.upper()}** berhasil disimpan langsung ke Google Sheets!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Gagal menyimpan ke Google Sheets: {ex}")

        st.markdown(f"### Daftar Tanggungan Reject ({len(df_view)} Data)")
        
        if len(df_view) == 0:
            st.warning("Tidak ada data reject yang ditemukan untuk filter tersebut.")
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
                        if st.button(f"✅ Selesaikan ({row['Customer']})", key=f"btn_done_{idx}"):
                            try:
                                df_tracking.loc[idx, 'Status'] = 'Selesai'
                                conn.update(worksheet="Tracking", data=df_tracking)
                                st.success(f"Status {row['Customer']} diperbarui di Google Sheets!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal memperbarui status: {ex}")
                    with col_act2:
                        if st.button(f"🗑️ Hapus Data ({row['Customer']})", key=f"btn_del_{idx}"):
                            try:
                                df_cleaned = df_tracking.drop(idx).reset_index(drop=True)
                                conn.update(worksheet="Tracking", data=df_cleaned)
                                st.warning(f"Data customer **{row['Customer']}** dihapus dari Google Sheets!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal menghapus data: {ex}")
                    with col_act3:
                        wa_text = f"Halo Kak {row['Sales']}, mohon bantuannya follow up reject customer *{row['Customer']}* ({row['Bank']}). Alasan: {row['Alasan Reject']}. Solusi: {row['Solusi']}"
                        st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer;">💬 Kirim WA</button></a>', unsafe_allow_html=True)
                    st.markdown("---")

    # -------------------------------------------------------------------------
    # MENU 3: REJECT GUIDE
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # MENU 4: PENGATURAN & BACKUP
    # -------------------------------------------------------------------------
    elif menu_pilihan == "⚙️ Pengaturan & Backup":
        st.subheader("⚙️ Pengaturan Sistem & Backup Data Cadangan")
        st.write("Versi Web: SO-Cust Tracking v5.0 (Strict Google Sheets Live Sync)")
        st.success("Database Utama: Terhubung ke Google Sheets (`DB_AutoMonitor_Makassar`)")
        
        st.markdown("---")
        st.subheader("📥 Download Backup Data (Excel)")
        st.markdown("Cadangkan data terkini ke file Excel (.xlsx) sebagai langkah antisipasi offline:")
        
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
