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

# Custom CSS Korporat Profesional & Mobile Friendly
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
    }
    .reject-box {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
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

# Inisialisasi Database Mock / Session State untuk Simulasi Interaktif CRUD
if 'data_tracking' not in st.session_state:
    st.session_state.data_tracking = pd.DataFrame([
        {
            "ID": "REG-001",
            "Customer": "JUNAIDI",
            "NoRek": "01349791008210440",
            "Bank": "BRI",
            "Sales": "AIRLANGGA PERSADA",
            "Alasan Reject": "Phone number is not correct",
            "Keterangan": "Terjadi perbedaan antara no telp customer di AOL Autodebet dan BRIMO",
            "Solusi": "Input ulang melalui menu AOL Autodebet CSO, pastikan nomor telepon sesuai dengan yang terdaftar di Bank BRI/BRIMO.",
            "Status": "Pending"
        },
        {
            "ID": "REG-002",
            "Customer": "SULANI",
            "NoRek": "01349791008202525",
            "Bank": "BRI",
            "Sales": "AIRLANGGA PERSADA",
            "Alasan Reject": "Phone number not found",
            "Keterangan": "Pada saat pembukaan rekening awal, customer belum mencantumkan nomor ke BRI",
            "Solusi": "Arahkan Customer untuk Registrasi BRIMO.",
            "Status": "Pending"
        },
        {
            "ID": "REG-003",
            "Customer": "MADIAN FIKRI",
            "NoRek": "01349791008218734",
            "Bank": "BRI",
            "Sales": "BUDI SANTOSO",
            "Alasan Reject": "Phone number not found",
            "Keterangan": "Pada saat pembukaan rekening awal, customer belum mencantumkan nomor ke BRI",
            "Solusi": "Arahkan Customer untuk Registrasi BRIMO.",
            "Status": "Selesai"
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
        "📖 Reject Guide Universal", 
        "⚙️ Pengaturan & Data"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ACC Makassar** - Sistem Kolaborasi & Tracking Operasional Lapangan.")

def main():
    # -------------------------------------------------------------------------
    # MENU 1: MONITORING DASHBOARD
    # -------------------------------------------------------------------------
    if menu_pilihan == "📊 Monitoring Dashboard":
        st.title("🚗 AutoMonitor - ACC Cabang Makassar")
        st.markdown("Dashboard utama pemantauan proses autodebet secara *real-time*.")
        
        # Metrik Ringkasan
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Data Nasabah", "234")
        with col2:
            st.metric("Total Reject", len(st.session_state.data_tracking))
        with col3:
            st.metric("Success Rate Global", "85.2%")
        with col4:
            st.metric("Server Status", "Online 🚀")
            
        st.markdown("---")
        st.subheader("Ringkasan Performa Bank")
        st.info("Fitur filter dan grafik analitik lengkap aktif. Gunakan menu Sales Tracking untuk memperbarui data lapangan.")

    # -------------------------------------------------------------------------
    # MENU 2: SALES TRACKING REJECT (INTERAKTIF CRUD)
    # -------------------------------------------------------------------------
    elif menu_pilihan == "📋 Sales Tracking Reject":
        st.title("📋 Sales Tracking Reject")
        st.markdown("Pusat pemantauan dan pengelolaan penolakan (*reject*) penagihan autodebet nasabah.")
        
        # Filter Sales Officer di bagian atas
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            daftar_sales = ["SEMUA SALES"] + list(st.session_state.data_tracking["Sales"].unique())
            pilih_sales = st.selectbox("👤 Pilih Nama Anda (Nama SO):", daftar_sales)
        with col_f2:
            search_box = st.text_input("🔍 Cari Nama/ID:", placeholder="Ketik nama customer...")

        st.markdown("---")

        # Filter DataFrame berdasarkan pilihan Sales & Pencarian
        df_view = st.session_state.data_tracking.copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"] == pilih_sales]
        if search_box:
            df_view = df_view[df_view["Customer"].str.contains(search_box, case=False, na=False)]

        # Tombol Aksi Tambah Data Baru
        with st.expander("➕ Tambah Data / Input Customer Reject Baru"):
            with st.form("form_tambah_reject"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    new_cust = st.text_input("Nama Customer")
                    new_norek = st.text_input("No Rekening / Kontrak")
                    new_bank = st.selectbox("Bank", ["BRI", "BCA", "MANDIRI", "BNI", "PERMATA"])
                with col_i2:
                    new_sales = st.selectbox("Sales Officer Penanggung Jawab", ["AIRLANGGA PERSADA", "BUDI SANTOSO", "ANDIEN", "FARIDZ FAATIAH"])
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

        # Tampilkan Daftar Tracking dalam bentuk kartu interaktif ala UI profesional
        st.markdown(f"### Daftar Tanggungan Reject ({len(df_view)} Data)")
        
        if len(df_view) == 0:
            st.warning("Tidak ada data reject yang ditemukan untuk filter tersebut.")
        else:
            for idx, row in df_view.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="reject-box">
                            <strong>{row['Customer']}</strong> ({row['Bank']} - No. Rek: {row['NoRek']})<br>
                            <small>Sales: <b>{row['Sales']}</b> | Status: <b>{row['Status']}</b></small><br>
                            <span style="color: #ef4444; font-weight: bold;">❌ Alasan Reject: {row['Alasan Reject']}</span>
                            <div class="solution-box">
                                <span style="color: #10b981; font-weight: bold;">💡 Solusi Perbaikan:</span><br>
                                {row['Solusi']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Aksi Edit / Update Status per baris
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button(f"✅ Selesaikan Status ({row['Customer']})", key=f"btn_{idx}"):
                            st.session_state.data_tracking.loc[idx, 'Status'] = 'Selesai'
                            st.success(f"Status {row['Customer']} diperbarui menjadi Selesai!")
                            st.rerun()
                    with col_act2:
                        wa_text = f"Halo Kak, mohon bantuannya follow up reject customer *{row['Customer']}* ({row['Bank']}). Alasan: {row['Alasan Reject']}. Solusi: {row['Solusi']}"
                        st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer;">💬 Salin / Kirim WA</button></a>', unsafe_allow_html=True)
                    st.markdown("---")

    # -------------------------------------------------------------------------
    # MENU 3: REJECT GUIDE UNIVERSAL
    # -------------------------------------------------------------------------
    elif menu_pilihan == "📖 Reject Guide Universal":
        st.header("📖 Panduan Penanganan Reject Universal")
        st.markdown("Acuan standar operasional untuk seluruh bank di ACC Cabang Makassar.")
        
        search_guide = st.text_input("🔍 Cari Kata Kunci Panduan:", placeholder="Contoh: tanda tangan, rekening, telepon...")
        
        data_guide = [
            {"No": 1, "Alasan Reject": "Tanda Tangan Tidak Sesuai", "Keterangan": "Tanda tangan tidak cocok dengan KTP.", "Tindakan Korektif": "Uji coba tanda tangan di atas kertas putih, sesuaikan dengan KTP."},
            {"No": 2, "Alasan Reject": "Nomor Telepon Tidak Valid / Tidak Sesuai", "Keterangan": "Perbedaan nomor HP di sistem dengan Mobile Banking.", "Tindakan Korektif": "Input ulang melalui sistem atau arahkan nasabah walk-in ke bank."},
            {"No": 3, "Alasan Reject": "Format / Nomor Rekening Tidak Sesuai", "Keterangan": "Salah input nomor rekening atau ada spasi.", "Tindakan Korektif": "Input nomor rekening sesuai data keuangan asli tanpa spasi."},
            {"No": 4, "Alasan Reject": "Dokumen / Bukti Kepemilikan Tidak Jelas", "Keterangan": "Scan ATM atau buku tabungan kurang jelas.", "Tindakan Korektif": "Pastikan dokumen format PDF bersih dan terbaca jelas."},
        ]
        df_g = pd.DataFrame(data_guide)
        if search_guide:
            df_g = df_g[df_g['Alasan Reject'].str.contains(search_guide, case=False, na=False)]
        
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------------
    # MENU 4: PENGATURAN
    # -------------------------------------------------------------------------
    elif menu_pilihan == "⚙️ Pengaturan & Data":
        st.subheader("Pengaturan Sistem & Hak Akses")
        st.write("Versi Web: v2.0 Interactive Cloud CRUD")
        st.success("Sistem siap diakses bersama tim Sales Officer ACC Makassar.")

if __name__ == '__main__':
    main()
