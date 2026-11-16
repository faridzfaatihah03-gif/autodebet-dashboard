
import streamlit as st
import pandas as pd

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="AutoMonitor - ACC Makassar",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Lingkaran Success Rate Bank dengan Warna Khas
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .bank-circle-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        text-align: center;
        border-top: 5px solid #cbd5e1;
        margin-bottom: 10px;
    }
    .circle-progress {
        width: 85px;
        height: 85px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        margin: 0 auto 10px auto;
        color: #ffffff;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.15);
    }
    h1, h2, h3 { color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI UTAMA ---
st.sidebar.title("AutoMonitor")
st.sidebar.markdown("---")

nav_menu = st.sidebar.radio(
    "Menu Utama:",
    (
        "📊 Monitoring",
        "❌ Data Reject",
        "📞 Sales Tracking",
        "📄 Template E-SKPR",
        "📖 Reject Guide",
        "⚙️ Pengaturan"
    )
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ACC Makassar** - Silakan upload file Excel bulanan pada menu utama untuk memuat data.")

# --- KOTAK UPLOAD FILE DINAMIS ---
st.title("🚗 AutoMonitor - ACC Cabang Makassar")
st.markdown("Sistem monitoring autodebet dinamis. Upload file Excel database bulanan untuk menampilkan laporan dan analisis lengkap.")

uploaded_file = st.file_uploader("📂 Upload File Excel Database (.xlsx) Bulan Ini:", type=["xlsx"])

# --- CEK APAKAH FILE SUDAH DI-UPLOAD ---
if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        target_sheet = 'NOV' if 'NOV' in sheet_names else sheet_names[0]
        df_nov = pd.read_excel(uploaded_file, sheet_name=target_sheet)
        df_nov.columns = df_nov.columns.astype(str).str.strip()
        st.success(f"Berhasil memuat data dari sheet: `{target_sheet}` ({len(df_nov)} baris data)")
    except Exception as e:
        st.error(f"Gagal membaca file Excel: {e}")
        df_nov = None
else:
    df_nov = None

# --- JIKA DATA BELUM DIMASUKKAN ---
if df_nov is None:
    st.warning("⚠️ **Dashboard masih kosong.** Silakan upload file Excel database autodebet Anda pada tombol di atas untuk menampilkan seluruh metrik dan grafik.")
    
# --- JIKA DATA SUDAH MASUK ---
else:
    if nav_menu == "📊 Monitoring":
        st.subheader("Monitoring Proses Autodebet")
        st.caption("Status Data: Aktif & Sinkronisasi Real-Time")

        # --- BAGIAN ATAS: SUCCESS RATE & ANGKA BERHASIL PER BANK ---
        st.markdown("### Performa Keberhasilan (Success Rate) per Bank")
        st.markdown("<p style='font-size: 13px; color: gray;'>Menampilkan persentase keberhasilan serta jumlah data berhasil vs total records per bank.</p>", unsafe_allow_html=True)
        
        if 'BANK_AUTODEBET' in df_nov.columns:
            banks = df_nov['BANK_AUTODEBET'].dropna().unique()
            b_cols = st.columns(len(banks) if len(banks) > 0 else 1)
            
            # Kamus warna khas tiap bank
            bank_colors = {
                "BANK RAKYAT INDONESIA": "#1d4ed8",  # Biru BRI
                "MANDIRI": "#eab308",                # Kuning Mandiri
                "BCA": "#0284c7",                    # Biru BCA
                "BNI": "#f97316",                    # Oranye BNI
                "PERMATA": "#0d9488"                 # Hijau Tosca Permata
            }
            
            total_all_records = len(df_nov)
            total_reject_all = len(df_nov[df_nov['REASON REJECT'].notna()]) if 'REASON REJECT' in df_nov.columns else 0
            total_success_all = total_all_records - total_reject_all
            
            for idx, bank in enumerate(banks):
                b_df = df_nov[df_nov['BANK_AUTODEBET'] == bank]
                b_total = len(b_df)
                b_reject = len(b_df[b_df['REASON REJECT'].notna()]) if 'REASON REJECT' in b_df.columns else 0
                b_success = b_total - b_reject
                
                # Hitung Success Rate (%) untuk bank tersebut
                success_rate = (b_success / b_total * 100) if b_total > 0 else 0
                color_code = bank_colors.get(str(bank).upper(), "#64748b")
                
                with b_cols[idx % len(b_cols)]:
                    st.markdown(f"""
                        <div class="bank-circle-card" style="border-top-color: {color_code};">
                            <div class="circle-progress" style="background: {color_code};">
                                {success_rate:.1f}%
                            </div>
                            <p style="font-size: 13px; font-weight: bold; margin: 5px 0 2px 0; color: #1e293b;">{bank}</p>
                            <span style="font-size: 11px; color: #16a34a; font-weight: bold;">Berhasil: {b_success}</span><br>
                            <span style="font-size: 11px; color: #64748b;">Total: {b_total} Records</span>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"<div style='text-align: right; margin-top: 5px; font-weight: bold; color: #16a34a;'>Total Data Berhasil Global: {total_success_all} dari {total_all_records} Data</div>", unsafe_allow_html=True)

        st.divider()

        # --- BARIS FILTER LENGKAP ---
        st.markdown("### Filter Data")
        
        with st.container():
            f1, f2, f3, f4 = st.columns(4)
            
            with f1:
                area_opts = ["Semua Area"] + list(df_nov['AREA'].dropna().unique()) if 'AREA' in df_nov.columns else ["Semua Area"]
                sel_area = st.selectbox("Filter Area", area_opts, label_visibility="collapsed")
                
            with f2:
                cabang_opts = ["Semua Cabang"] + list(df_nov['CABANG'].dropna().unique()) if 'CABANG' in df_nov.columns else ["Semua Cabang"]
                sel_cabang = st.selectbox("Filter Cabang", cabang_opts, label_visibility="collapsed")
                
            with f3:
                cycle_opts = ["Semua Cycle"] + list(df_nov['Cycle'].dropna().unique()) if 'Cycle' in df_nov.columns else ["Semua Cycle"]
                sel_cycle = st.selectbox("Filter Cycle", cycle_opts, label_visibility="collapsed")
                
            with f4:
                status_opts = ["Semua State"] + list(df_nov['STATUS PENDAFTARAN'].dropna().unique()) if 'STATUS PENDAFTARAN' in df_nov.columns else ["Semua State"]
                sel_status = st.selectbox("Filter State", status_opts, label_visibility="collapsed")

            f5, f6 = st.columns([3, 1])
            with f5:
                so_opts = ["Semua SO"] + list(df_nov['NAME_SO'].dropna().unique()) if 'NAME_SO' in df_nov.columns else ["Semua SO"]
                sel_so = st.selectbox("Filter SO", so_opts, label_visibility="collapsed")
            with f6:
                st.button("📥 Upload Baru", use_container_width=True, type="primary")

        # Terapkan Filter
        filtered_df = df_nov.copy()
        if sel_area != "Semua Area" and 'AREA' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['AREA'] == sel_area]
        if sel_cabang != "Semua Cabang" and 'CABANG' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['CABANG'] == sel_cabang]
        if sel_cycle != "Semua Cycle" and 'Cycle' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Cycle'] == sel_cycle]
        if sel_status != "Semua State" and 'STATUS PENDAFTARAN' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['STATUS PENDAFTARAN'] == sel_status]
        if sel_so != "Semua SO" and 'NAME_SO' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['NAME_SO'] == sel_so]

        st.markdown(f"**Monitoring Data:** Menampilkan dan memantau proses autodebet nasabah ({len(filtered_df)} data ditemukan).")
        
        # Kotak Status Kecil di Bawah Filter
        if 'STATUS PENDAFTARAN' in df_nov.columns:
            status_counts = df_nov['STATUS PENDAFTARAN'].value_counts()
            scols = st.columns(6)
            statuses = ['O', 'B', 'D', 'A', 'R', 'F']
            labels = ['Open', 'Bucket Finance', 'Pengajuan ke Bank', 'Approved', 'Rejected', 'Canceled']
            
            for i, st_code in enumerate(statuses[:len(scols)]):
                count_val = status_counts.get(st_code, 0)
                with scols[i]:
                    st.markdown(f"""
                        <div style="background: white; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                            <h4 style="margin: 0; color: #1e293b;">{count_val}</h4>
                            <span style="font-size: 11px; color: #64748b;">{labels[i]}</span>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(filtered_df, use_container_width=True)

    # ==========================================
    # 2. MENU: DATA REJECT
    # ==========================================
    elif nav_menu == "❌ Data Reject":
        st.subheader("❌ Daftar Data Reject & Alasan Penolakan")
        st.markdown("Kelola dan tinjau seluruh customer yang mengalami kendala reject autodebet.")
        
        if 'REASON REJECT' in df_nov.columns:
            reject_df = df_nov[df_nov['REASON REJECT'].notna()]
            
            search_rej = st.text_input("🔍 Cari No Kontrak / Nama Customer / Alasan:")
            if search_rej:
                reject_df = reject_df[
                    reject_df.astype(str).apply(lambda row: row.str.contains(search_rej, case=False).any(), axis=1)
                ]
                
            st.dataframe(reject_df[['NOKON', 'NAMA_CUST', 'CABANG', 'NAME_SO', 'BANK_AUTODEBET', 'REASON REJECT']], use_container_width=True)

    # ==========================================
    # 3. MENU: SALES TRACKING
    # ==========================================
    elif nav_menu == "📞 Sales Tracking":
        st.subheader("📞 Sales Tracking & Follow-up")
        st.markdown("Pantau portofolio customer dan buat pesan WhatsApp otomatis untuk Sales Officer.")
        
        if 'NAME_SO' in df_nov.columns:
            so_list = sorted(df_nov['NAME_SO'].dropna().unique())
            chosen_so = st.selectbox("Pilih Sales Officer (SO):", options=so_list)
            
            so_data = df_nov[df_nov['NAME_SO'] == chosen_so]
            st.write(f"Portofolio untuk: **{chosen_so}** ({len(so_data)} Customer)")
            st.dataframe(so_data[['NOKON', 'NAMA_CUST', 'CABANG', 'BANK_AUTODEBET', 'STATUS PENDAFTARAN', 'REASON REJECT']], use_container_width=True)
            
            if st.button("💬 Generate Pesan WhatsApp Follow-up"):
                rej_cnt = len(so_data[so_data['REASON REJECT'].notna()]) if 'REASON REJECT' in so_data.columns else 0
                st.success("Pesan berhasil dibuat!")
                st.code(f"Halo {chosen_so}, mohon segera lakukan follow-up untuk customer autodebet di area Anda. Total data: {len(so_data)}, Reject: {rej_cnt}. Terima kasih.", language="text")

    # ==========================================
    # 4. MENU: TEMPLATE E-SKPR
    # ==========================================
    elif nav_menu == "📄 Template E-SKPR":
        st.subheader("📄 Template Dokumen E-SKPR")
        space_col1, space_col2 = st.columns(2)
        with space_col1:
            st.info("Unduh dokumen panduan dan template E-SKPR resmi ACC.")
            st.download_button("Download Template Excel", data=b"Dummy Data", file_name="Template_ESKPR.xlsx")
        with space_col2:
            st.success("Status Template: Terverifikasi HO.")

    # ==========================================
    # 5. MENU: REJECT GUIDE
    # ==========================================
    elif nav_menu == "📖 Reject Guide":
        st.subheader("📖 Panduan Penanganan Alasan Reject (Reject Guide)")
        st.markdown("""
        Berikut adalah panduan standar penanganan kode reject autodebet:
        * **Phone number is not correct**: Lakukan konfirmasi ulang nomor HP customer yang terdaftar di sistem.
        * **Format Account Tidak Sesuai**: Pastikan nomor rekening dan nama pemilik rekening di bank sesuai dengan KTP.
        * **Phone number not found**: Hubungi customer untuk memperbarui nomor kontak aktif.
        """)

    # ==========================================
    # 6. MENU: PENGATURAN
    # ==========================================
    elif nav_menu == "⚙️ Pengaturan":
        st.subheader("⚙️ Pengaturan Sistem & Database")
        st.write("Kelola database lokal dan konfigurasi koneksi ACC Cabang Makassar.")
        if st.button("🗑️ Reset / Hapus Cache Data"):
            st.cache_data.clear()
            st.success("Data berhasil di-reset. Silakan upload file Excel baru.")