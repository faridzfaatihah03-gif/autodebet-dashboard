import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="AutoMonitor - ACC Cabang Makassar",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Korporat Profesional & Berbingkai Rapi
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
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

# Daftar Resmi Sales Officer ACC Cabang Makassar (Sesuai Data Mentah)
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

# Inisialisasi Database Mock / Session State untuk Pelacakan Interaktif
if 'data_tracking' not in st.session_state:
    st.session_state.data_tracking = pd.DataFrame([
        {
            "ID": "REG-001",
            "Customer": "HENRI",
            "NoRek": "1600801003449078",
            "Bank": "BRI",
            "Sales": "RESKYANTO PUNDA",
            "Alasan Reject": "Phone number is not correct",
            "Keterangan": "Terjadi perbedaan antara no telp customer di AOL Autodebet dan BRIMO",
            "Solusi": "Input ulang melalui menu AOL Autodebet CSO, pastikan nomor telepon sesuai dengan yang terdaftar di Bank BRI/BRIMO.",
            "Status": "Pending"
        },
        {
            "ID": "REG-002",
            "Customer": "ASRIYADI",
            "NoRek": "1600801003448594",
            "Bank": "BRI",
            "Sales": "NURUL AZIZAH",
            "Alasan Reject": "Phone number not found",
            "Keterangan": "Pada saat pembukaan rekening awal, customer belum mencantumkan nomor ke BRI",
            "Solusi": "Arahkan Customer untuk Registrasi BRIMO.",
            "Status": "Pending"
        }
    ])

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
st.sidebar.info("💡 **ACC Makassar** - Sistem Kolaborasi & Tracking Operasional Lapangan.")

def main():
    # -------------------------------------------------------------------------
    # MENU 1: MONITORING DASHBOARD (Dengan Bingkai Rapi pada Semua Metrik)
    # -------------------------------------------------------------------------
    if menu_pilihan == "📊 Monitoring Dashboard":
        st.title("🚗 AutoMonitor - ACC Cabang Makassar")
        st.markdown("Dashboard utama pemantauan proses autodebet dan performa perbankan secara *real-time*.")
        
        # Metrik Utama dengan Bingkai
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Nasabah Cabang</span>
                    <h2 style="color: #3b82f6; margin: 5px 0;">1,420</h2>
                    <small style="color: #10b981;">● Aktif Periode Ini</small>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Reject Aktif</span>
                    <h2 style="color: #ef4444; margin: 5px 0;">{len(st.session_state.data_tracking)}</h2>
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
                    <small style="color: #10b981;">● Real-Time Sync</small>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("📊 Persentase Success Rate per Bank (5 Bank Mitra)")
        st.markdown("Indikator keberhasilan registrasi autodebet per bank khusus lingkup ACC Cabang Makassar.")
        
        # Grid Metrik Success Rate per Bank dengan Bingkai Kardus Kustom
        b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
        with b_col1:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #60a5fa;">BCA</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">91.2%</h3>
                    <small style="color: #10b981;">Stable</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col2:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #60a5fa;">BRI</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">87.5%</h3>
                    <small style="color: #10b981;">+0.8%</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col3:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #60a5fa;">MANDIRI</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">89.1%</h3>
                    <small style="color: #10b981;">Stable</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col4:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #60a5fa;">BNI</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">86.4%</h3>
                    <small style="color: #ef4444;">-0.5%</small>
                </div>
            """, unsafe_allow_html=True)
        with b_col5:
            st.markdown("""
                <div class="bank-card">
                    <b style="color: #60a5fa;">PERMATA</b>
                    <h3 style="margin: 5px 0; color: #f3f4f6;">85.0%</h3>
                    <small style="color: #10b981;">Stable</small>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.info("💡 Gunakan menu **Sales Tracking Reject** di samping untuk melakukan pemantauan dan tindak lanjut kasus penolakan bersama tim Sales Officer.")

    # -------------------------------------------------------------------------
    # MENU 2: SALES TRACKING REJECT (INTERAKTIF)
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

        df_view = st.session_state.data_tracking.copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"] == pilih_sales]
        if search_box:
            df_view = df_view[df_view["Customer"].str.contains(search_box, case=False, na=False)]

        # Tombol Tambah Data Reject Baru oleh Sales/Head
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
                
                submit_btn = st.form_submit_button("Simpan Data Reject Baru")
                if submit_btn and new_cust:
                    new_row = pd.DataFrame([{
                        "ID": f"REG-00{len(st.session_state.data_tracking)+1}",
                        "Customer": new_cust.upper(),
                        "NoRek": new_norek,
                        "Bank": new_bank,
                        "Sales": new_sales,
                        "Alasan Reject": new_reason,
                        "Keterangan": "Input manual lapangan oleh Sales Officer",
                        "Solusi": new_solusi,
                        "Status": "Pending"
                    }])
                    st.session_state.data_tracking = pd.concat([st.session_state.data_tracking, new_row], ignore_index=True)
                    st.success(f"Data customer **{new_cust.upper()}** berhasil ditambahkan!")
                    st.rerun()

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
                    
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button(f"✅ Selesaikan Status ({row['Customer']})", key=f"btn_{idx}"):
                            st.session_state.data_tracking.loc[idx, 'Status'] = 'Selesai'
                            st.success(f"Status {row['Customer']} diperbarui menjadi Selesai!")
                            st.rerun()
                    with col_act2:
                        wa_text = f"Halo Kak {row['Sales']}, mohon bantuannya follow up reject customer *{row['Customer']}* ({row['Bank']}). Alasan: {row['Alasan Reject']}. Solusi: {row['Solusi']}"
                        st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer;">💬 Salin / Kirim WA</button></a>', unsafe_allow_html=True)
                    st.markdown("---")

    # -------------------------------------------------------------------------
    # MENU 3: REJECT GUIDE
    # -------------------------------------------------------------------------
    elif menu_pilihan == "📖 Reject Guide":
        st.header("📖 Panduan Penanganan Reject")
        st.markdown("Acuan standar operasional universal untuk penanganan penolakan autodebet di ACC Cabang Makassar.")
        
        search_guide = st.text_input("🔍 Cari Kata Kunci Panduan:", placeholder="Contoh: tanda tangan, rekening, telepon, dokumen...")
        
        data_guide = [
            {
                "No": 1,
                "Alasan Reject": "Tanda Tangan Tidak Sesuai",
                "Keterangan": "Tanda tangan pada dokumen pengajuan tidak cocok atau berbeda dengan identitas resmi (KTP).",
                "Tindakan Korektif": "Lakukan uji coba tanda tangan di atas kertas putih, sesuaikan lekukan dan polanya persis dengan yang tertera di KTP."
            },
            {
                "No": 2,
                "Alasan Reject": "Nomor Telepon Tidak Valid / Tidak Sesuai",
                "Keterangan": "Terjadi perbedaan nomor HP pada sistem dengan nomor terdaftar di Mobile Banking nasabah, atau nomor kosong.",
                "Tindakan Korektif": "Input ulang melalui menu sistem; pastikan nomor sesuai dengan yang terdaftar di bank, atau arahkan nasabah walk-in ke bank untuk updation nomor telepon."
            },
            {
                "No": 3,
                "Alasan Reject": "Format / Nomor Rekening Tidak Sesuai",
                "Keterangan": "Salah penginputan nomor rekening (kelebihan angka '0', salah karakter, atau terdapat spasi).",
                "Tindakan Korektif": "Input nomor rekening sesuai data keuangan asli, pastikan tidak ada penambahan karakter atau spasi di luar ketentuan."
            },
            {
                "No": 4,
                "Alasan Reject": "Dokumen / Bukti Kepemilikan Tidak Sesuai / Tidak Jelas",
                "Keterangan": "Lampiran bukti kepemilikan (foto ATM fisik/digital atau cover buku tabungan) tidak valid atau hasil scan kurang jelas.",
                "Tindakan Korektif": "Pastikan bukti kepemilikan sah, dokumen dalam format PDF yang bersih, terbaca jelas, dan tanpa penebalan pulpen manual."
            },
            {
                "No": 5,
                "Alasan Reject": "Ketidaksesuaian Data Identitas & Nama Pemegang Rekening",
                "Keterangan": "Nama atau NIK pada form pengajuan berbeda dengan data dokumen identitas resmi atau akta perusahaan.",
                "Tindakan Korektif": "CSO/FAB wajib melakukan pengecekan ulang (validasi NIK dan ejaan nama) sebelum data diinput dan di-upload ke sistem."
            },
            {
                "No": 6,
                "Alasan Reject": "Kelengkapan Dokumen / Form Belum Lengkap",
                "Keterangan": "Bagian penting pada form (seperti Hak Substitusi, lembar pernyataan, atau legalitas perusahaan) kosong atau tidak terisi.",
                "Tindakan Korektif": "Gunakan form/SKPR versi terbaru yang sudah terisi lengkap (termasuk Hak Substitusi dan legalitas perusahaan yang berwenang sesuai AD/ART)."
            },
            {
                "No": 7,
                "Alasan Reject": "Double Registrasi / Pengajuan Ganda",
                "Keterangan": "Sistem mendeteksi adanya pengajuan berulang untuk data nasabah yang sama.",
                "Tindakan Korektif": "Merupakan sistem double entry, cukup tunggu proses penyesuaian otomatis oleh sistem pada saat EOD (End of Day)."
            }
        ]
        
        df_g = pd.DataFrame(data_guide)
        if search_guide:
            df_g = df_g[
                df_g['Alasan Reject'].str.contains(search_guide, case=False, na=False) |
                df_g['Keterangan'].str.contains(search_guide, case=False, na=False) |
                df_g['Tindakan Korektif'].str.contains(search_guide, case=False, na=False)
            ]
        
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------------
    # MENU 4: PENGATURAN
    # -------------------------------------------------------------------------
    elif menu_pilihan == "⚙️ Pengaturan & Data":
        st.subheader("Pengaturan Sistem & Hak Akses")
        st.write("Versi Web: v2.3 Makassar Clean Edition")
        st.success("Sistem siap disinkronkan dengan Google Sheets.")

if __name__ == '__main__':
    main()
