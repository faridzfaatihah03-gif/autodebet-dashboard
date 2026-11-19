import streamlit as st
import pandas as pd
import io
import urllib.parse

# Konfigurasi Halaman
st.set_page_config(
    page_title="AUTOTEAM - Autodebet Team Achievement & Monitoring",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Korporat Profesional & Perbaikan Kontras Teks
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    footer {display: none !important; visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    
    .tagline-pill {
        display: inline-block;
        background: linear-gradient(90deg, #1e3a8a, #2563eb);
        color: #eff6ff;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.6px;
        margin-top: 4px;
        margin-bottom: 10px;
        border: 1px solid #3b82f6;
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
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ef4444;
        border: 1px solid #374151;
        margin-bottom: 14px;
        color: #f3f4f6 !important;
    }
    .reject-box strong {
        color: #ffffff !important;
        font-size: 18px;
    }
    .reject-box small {
        color: #9ca3af !important;
        font-size: 13.5px;
    }
    .reject-reason {
        color: #f87171 !important;
        font-weight: bold;
        font-size: 15px;
        margin-top: 8px;
        display: block;
    }
    .solution-box {
        background-color: #064e3b;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin-top: 12px;
        color: #ecfdf5 !important;
    }
    .solution-box span {
        color: #34d399 !important;
        font-weight: bold;
    }
    .rekap-box {
        background-color: #111827;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #2563eb;
        border-left: 5px solid #25d366;
        margin-bottom: 18px;
        color: #e5e7eb !important;
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

# Kamus Arti Status Resmi
KAMUS_STATUS = {
    "O": "Open",
    "F": "Bukcet Finance",
    "D": "Pengajuan ke Bank",
    "A": "Approved",
    "R": "Rejected",
    "C": "Cancelled",
    "B": "Batal",
    "E": "Edit",
    "P": "Pending",
}

STATUS_TIDAK_AKTIF = {"C", "B"}
STATUS_AKTIF = {"O", "F", "D", "A", "R", "E", "P"}

def map_status_label(code):
    c = str(code).upper().strip()
    if c in KAMUS_STATUS:
        return KAMUS_STATUS[c]
    return "Belum Diproses" if c in ["", "NAN", "NONE"] else c

def map_keaktifan_label(code):
    c = str(code).upper().strip()
    if c in STATUS_TIDAK_AKTIF:
        return "Tidak Aktif"
    if c in STATUS_AKTIF:
        return "Aktif"
    return "Aktif" if c not in ["", "NAN", "NONE"] else "Tidak Aktif"

# Katalog Lengkap Panduan & Solusi Reject
REJECT_GUIDE_ITEMS = [
    {
        "No": 1,
        "Alasan Reject": "Phone number is not correct",
        "Keterangan": "Nomor telepon nasabah tidak sesuai atau berbeda antara data pengajuan/AOL dengan data yang terdaftar di bank / mobile banking (misalnya BRIMO).",
        "Tindakan Korektif / Solusi SO": "Input ulang melalui menu AOL Autodebet CSO dan pastikan nomor HP sesuai dengan yang terdaftar di Bank/BRIMO. Jika belum sinkron, arahkan nasabah walk-in ke bank untuk pembaruan nomor HP."
    },
    {
        "No": 2,
        "Alasan Reject": "Phone number not found",
        "Keterangan": "Nomor telepon nasabah belum terdaftar atau tidak ditemukan pada sistem bank terkait saat proses pendaftaran autodebet.",
        "Tindakan Korektif / Solusi SO": "Arahkan nasabah melakukan registrasi atau pembaruan data nomor HP aktif di bank terkait terlebih dahulu, lalu ajukan ulang."
    },
    {
        "No": 3,
        "Alasan Reject": "Scan Kartu ATM Meragukan / No. Kartu ATM Invalid",
        "Keterangan": "Foto atau scan kartu ATM kurang jelas/buram, atau nasabah sudah melakukan penggantian kartu ATM sehingga nomor kartu lama sudah tidak berlaku.",
        "Tindakan Korektif / Solusi SO": "Minta foto/scan kartu ATM terbaru yang jelas dan valid (pastikan tidak terpotong/buram), lalu lakukan pengajuan ulang."
    },
    {
        "No": 4,
        "Alasan Reject": "Tanda Tangan Tidak Menyentuh Materai / Tidak Sesuai",
        "Keterangan": "Tanda tangan pada form kuasa/SKPR tidak menyentuh materai atau tidak cocok dengan spesimen tanda tangan pada KTP/buku tabungan.",
        "Tindakan Korektif / Solusi SO": "Lengkapi ulang tanda tangan di atas materai sesuai spesimen KTP/rekening bank nasabah dan pastikan tidak menyimpang dari batas ketentuan."
    },
    {
        "No": 5,
        "Alasan Reject": "Invalid format account number",
        "Keterangan": "Format nomor rekening tidak sesuai ketentuan bank, salah digit, atau terdapat spasi/karakter yang tidak valid.",
        "Tindakan Korektif / Solusi SO": "Periksa kembali nomor rekening nasabah sesuai buku tabungan/rekening asli tanpa spasi atau karakter tambahan, lalu input ulang."
    },
    {
        "No": 6,
        "Alasan Reject": "Saldo tidak mencukupi",
        "Keterangan": "Saldo rekening nasabah tidak mencukupi untuk memenuhi syarat minimum atau proses pendebetan/validasi.",
        "Tindakan Korektif / Solusi SO": "Informasikan nasabah untuk memastikan saldo rekening mencukupi dan aktif sebelum proses penagihan/aktivasi berikutnya."
    },
    {
        "No": 7,
        "Alasan Reject": "Rekening tidak aktif / dormant",
        "Keterangan": "Rekening sumber autodebet dalam status dormant (tidak aktif) atau diblokir/terbatas transaksinya.",
        "Tindakan Korektif / Solusi SO": "Arahkan nasabah untuk mengaktifkan kembali rekening (reaktivasi dormant) di cabang bank terkait."
    },
    {
        "No": 8,
        "Alasan Reject": "Data customer tidak sesuai",
        "Keterangan": "Terdapat ketidaksesuaian identitas nasabah (nama, NIK/KTP, atau data pendukung) antara kontrak/pengajuan dan data rekening bank.",
        "Tindakan Korektif / Solusi SO": "Cocokkan kembali identitas nasabah di KTP, kontrak, dan rekening bank, lalu koordinasikan perbaikan data/dokumen pendukung."
    }
]

def get_solusi_reject(reason):
    r = str(reason).lower().strip()
    if "not correct" in r:
        return "Input ulang melalui menu AOL Autodebet CSO, pastikan nomor telepon yang diinput sesuai dengan nomor telepon yang terdaftar di Bank / BRIMO. Arahkan customer walk-in ke Bank untuk updation no Telp."
    elif "not found" in r:
        return "Arahkan Customer untuk melakukan registrasi / pembaruan data nomor HP di bank terkait."
    elif "tanda tangan" in r or "skpr" in r or "materai" in r:
        return "Lengkapi ulang tanda tangan di atas materai sesuai spesimen KTP/rekening bank, lalu lakukan pengajuan ulang."
    elif "kartu atm" in r or "3.1.3" in r or "7. " in r:
        return "Verifikasi ulang nomor kartu ATM aktif & kirim foto/scan kartu ATM yang jelas serta form SKPR sesuai ketentuan."
    elif "account number" in r or "rekening" in r:
        return "Cek dan input ulang nomor rekening sesuai buku tabungan asli tanpa spasi atau karakter tambahan."
    elif "saldo" in r:
        return "Informasikan customer untuk memastikan saldo rekening mencukupi sesuai ketentuan."
    elif "dormant" in r or "tidak aktif" in r:
        return "Arahkan customer untuk mengaktifkan kembali rekening dormant di bank terkait."
    elif "tidak sesuai" in r or "data customer" in r:
        return "Cocokkan kembali data identitas customer antara KTP, kontrak, dan data bank, lalu perbaiki sesuai dokumen sah."
    elif r in ["", "-", "nan", "none"]:
        return "Lakukan pengecekan detail kendala aktivasi autodebet bersama tim Admin / CSO."
    else:
        return "Koordinasikan perbaikan dokumen/data rekening nasabah sesuai catatan reject di AOL."

# Normalisasi Nama Bank
def normalize_bank(val):
    b = str(val).upper().strip()
    if "RAKYAT INDONESIA" in b or b == "BRI":
        return "BRI"
    elif "MANDIRI" in b:
        return "MANDIRI"
    elif "BCA" in b:
        return "BCA"
    elif "BNI" in b:
        return "BNI"
    elif "PERMATA" in b:
        return "PERMATA"
    elif b in ["", "NAN", "NONE"]:
        return "LAINNYA"
    return b

def clean_text(val, default="-"):
    s = str(val).strip()
    if s == "" or s.lower() in ["nan", "none", "nat", "-"]:
        return default
    return s

def extract_cabang_area(row):
    cabang = clean_text(row.get("CABANG", ""), "")
    area_new = clean_text(row.get("AREA NEW", ""), "")
    area = clean_text(row.get("AREA", ""), "")
    area_gabung = area_new if area_new else area
    if cabang and area_gabung and cabang.lower() != area_gabung.lower():
        return f"{cabang} / {area_gabung}"
    return cabang or area_gabung or "-"

def extract_aging_tanggal(row):
    aging = clean_text(row.get("Aging", ""), "")
    aging_raw = clean_text(row.get("AGING_", ""), "")
    tgl_ref = clean_text(row.get("2026-04-11", ""), "")
    dt_golive = clean_text(row.get("DT_GOLIVE", ""), "")

    bagian = []
    if aging:
        bagian.append(f"Aging {aging} hr")
    elif aging_raw:
        bagian.append(f"Aging {aging_raw}")

    if tgl_ref:
        bagian.append(f"Tgl {tgl_ref}")
    elif dt_golive:
        bagian.append(f"Golive {dt_golive}")

    return " | ".join(bagian) if bagian else "-"

def build_wa_item_message(row):
    sales = clean_text(row.get("Sales", ""), "Kak")
    cust = clean_text(row.get("Customer", ""), "-")
    nokon = clean_text(row.get("ID", ""), "-")
    bank = clean_text(row.get("Bank", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)
    alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum")
    solusi = clean_text(row.get("Solusi", ""), "-")

    lines = [
        f"Halo Kak {sales}, mohon bantuannya follow up reject autodebet customer berikut:",
        "",
        f"• *Customer:* {cust} ({nokon})",
        f"• *Cabang/Area:* {cabang_area}",
        f"• *Bank:* {bank}",
        f"• *Aging/Tanggal:* {aging_tgl}",
        f"• *Alasan Reject:* {alasan}",
        f"• *Solusi:* {solusi}",
    ]
    return "\n".join(lines)

def build_wa_rekap_message(df_rekap, nama_so="SO"):
    if df_rekap.empty:
        return ""
    sapaan = f"Halo Kak {nama_so}," if nama_so and nama_so != "SEMUA SALES" else "Halo Tim Sales Officer,"
    lines = [
        sapaan,
        "Berikut daftar customer reject yang perlu segera di follow up:",
        ""
    ]
    for idx, (_, row) in enumerate(df_rekap.iterrows(), start=1):
        cust = clean_text(row.get("Customer", ""), "-")
        nokon = clean_text(row.get("ID", ""), "-")
        bank = clean_text(row.get("Bank", ""), "-")
        cabang_area = extract_cabang_area(row)
        aging_tgl = extract_aging_tanggal(row)
        alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum")
        solusi = clean_text(row.get("Solusi", ""), "-")
        sales_item = clean_text(row.get("Sales", ""), "-")

        baris_so = f"\n   👤 SO: {sales_item}" if nama_so == "SEMUA SALES" else ""
        lines.append(
            f"{idx}. *{cust}* ({nokon}){baris_so}\n"
            f"   📍 Cabang/Area: {cabang_area}\n"
            f"   🏦 Bank: {bank}\n"
            f"   ⏳ Aging/Tanggal: {aging_tgl}\n"
            f"   ❌ Alasan: {alasan}\n"
            f"   ✅ Solusi: {solusi}"
        )
        lines.append("")
    return "\n".join(lines).strip()

# Fungsi Memuat Data dari Google Sheets Publik via CSV
@st.cache_data(ttl=10)
def load_data_sheets():
    sheet_id = "1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Tracking"
    try:
        df = pd.read_csv(url, dtype=str).fillna("")
        df.columns = [c.strip() for c in df.columns]

        if "NAMA_CUST" in df.columns:
            df = df[df["NAMA_CUST"].str.strip() != ""].copy()
        elif "Customer" in df.columns:
            df = df[df["Customer"].str.strip() != ""].copy()

        df["ID"] = df["NOKON"] if "NOKON" in df.columns else df.get("ID", "-")
        df["Customer"] = df["NAMA_CUST"] if "NAMA_CUST" in df.columns else df.get("Customer", "-")
        df["Bank_Raw"] = df["BANK_AUTODEBET"] if "BANK_AUTODEBET" in df.columns else df.get("Bank", "")
        df["Bank"] = df["Bank_Raw"].apply(normalize_bank)
        df["Sales"] = df["NAME_SO"].str.strip() if "NAME_SO" in df.columns else df.get("Sales", "-")
        df["Status_Code"] = df["STATUS PENDAFTARAN"].str.upper().str.strip() if "STATUS PENDAFTARAN" in df.columns else ""
        df["Status"] = df["Status_Code"].apply(map_status_label)
        df["Keaktifan"] = df["Status_Code"].apply(map_keaktifan_label)
        df["Alasan Reject"] = df["REASON REJECT"].str.strip() if "REASON REJECT" in df.columns else df.get("Alasan Reject", "")
        df["Solusi"] = df["Alasan Reject"].apply(get_solusi_reject)
        return df, True
    except Exception:
        fallback = pd.DataFrame([
            {"ID": "REG-001", "Customer": "HENRI", "Bank": "BRI", "Sales": "RESKYANTO PUNDA", "Status_Code": "R", "Status": "Rejected", "Keaktifan": "Aktif", "Alasan Reject": "Phone number is not correct", "Solusi": get_solusi_reject("Phone number is not correct"), "CABANG": "MAKASSAR", "AREA NEW": "Area 5", "Aging": "7"}
        ])
        return fallback, False

df_tracking, is_live = load_data_sheets()

# Sidebar Navigasi Korporat
st.sidebar.title("AUTOTEAM")
st.sidebar.caption("Autodebet Team Achievement & Monitoring")
st.sidebar.markdown('<div class="tagline-pill">Monitor. Improve. Activate.</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("**Menu Utama:**")

menu_pilihan = st.sidebar.radio(
    "Navigasi",
    [
        "📊 Monitoring Dashboard",
        "📈 Cust Status Tracking",
        "📋 Sales Tracking Reject",
        "📖 Reject Guide",
        "⚙️ Pengaturan & Database"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ACC Cabang Makassar** — Kolaborasi & monitoring performa autodebet tim lapangan.")

def main():
    total_data = len(df_tracking)
    df_aktif = df_tracking[df_tracking["Keaktifan"] == "Aktif"] if not df_tracking.empty else pd.DataFrame()
    total_aktif = len(df_aktif)
    total_approved = len(df_tracking[df_tracking["Status_Code"] == "A"]) if not df_tracking.empty else 0
    total_rejected = len(df_tracking[df_tracking["Status_Code"] == "R"]) if not df_tracking.empty else 0
    success_rate_cabang = (total_approved / total_data * 100) if total_data > 0 else 0.0

    if menu_pilihan == "📊 Monitoring Dashboard":
        st.title("🚗 AUTOTEAM — ACC Cabang Makassar")
        st.markdown("**Autodebet Team Achievement & Monitoring**")
        st.markdown('<div class="tagline-pill">Monitor. Improve. Activate.</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Data Tracking</span>
                    <h2 style="color: #3b82f6; margin: 5px 0;">{total_data}</h2>
                    <small style="color: #10b981;">● Aktif: {total_aktif} | Non-Aktif (C/B): {total_data - total_aktif}</small>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Total Rejected (R)</span>
                    <h2 style="color: #ef4444; margin: 5px 0;">{total_rejected}</h2>
                    <small style="color: #f59e0b;">● Status Aktif Perlu Tindak Lanjut</small>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Success Rate (Approved / A)</span>
                    <h2 style="color: #10b981; margin: 5px 0;">{success_rate_cabang:.1f}%</h2>
                    <small style="color: #10b981;">● {total_approved} Approved dari {total_data} Data</small>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <span style="color: #9ca3af; font-size: 14px;">Server Status</span>
                    <h2 style="color: #a855f7; margin: 5px 0;">Online 🚀</h2>
                    <small style="color: #10b981;">● AUTOTEAM Active</small>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("📊 Statistik Volume & Performa per Bank (Data Cabang Makassar)")
        
        bank_configs = [
            ("BRI", "#3b82f6"),
            ("MANDIRI", "#f59e0b"),
            ("BCA", "#3b82f6"),
            ("BNI", "#f97316"),
            ("PERMATA", "#10b981"),
        ]
        bank_cols = st.columns(5)
        for idx, (bank_name, title_color) in enumerate(bank_configs):
            sub_b = df_tracking[df_tracking["Bank"] == bank_name]
            vol_b = len(sub_b)
            app_b = len(sub_b[sub_b["Status_Code"] == "A"])
            rate_b = (app_b / vol_b * 100) if vol_b > 0 else 0.0
            badge_label = "Top Rate" if rate_b >= 70 else ("Dominan" if vol_b >= 100 else ("Proses" if vol_b > 0 else "N/A"))
            with bank_cols[idx]:
                st.markdown(
                    f'<div class="bank-card">'
                    f'<b style="color: {title_color}; font-size: 16px;">{bank_name}</b>'
                    f'<h3 style="margin: 5px 0; color: #f3f4f6;">{rate_b:.1f}%</h3>'
                    f'<span style="color: #9ca3af; font-size: 12px;">Total: <b>{vol_b}</b> Nasabah ({app_b} Approved)</span><br>'
                    f'<small style="color: #10b981;">{badge_label}</small>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.subheader("📋 Master Data Nasabah & Status Tracking (Live from Google Sheets)")
        kolom_tampil = [c for c in ["NOKON", "NAMA_CUST", "CABANG", "NAME_SO", "BANK_AUTODEBET", "STATUS PENDAFTARAN", "Status", "Keaktifan", "REASON REJECT"] if c in df_tracking.columns]
        st.dataframe(df_tracking[kolom_tampil] if kolom_tampil else df_tracking, use_container_width=True, hide_index=True)

    elif menu_pilihan == "📈 Cust Status Tracking":
        st.title("📈 Cust Status Tracking")
        st.markdown("Pemantauan menyeluruh progress pengajuan seluruh nasabah dan kontribusi performa setiap Sales Officer.")

        c_f1, c_f2, c_f3, c_f4, c_f5 = st.columns([1.8, 1.3, 1.1, 1.1, 1.5])
        with c_f1:
            so_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
            opsi_so = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SO_MAKASSAR + so_di_data))
            pilih_so_all = st.selectbox("👤 Filter Sales Officer:", opsi_so, key="so_all_select")
        with c_f2:
            opsi_status = [
                "SEMUA STATUS",
                "Open (O)",
                "Bukcet Finance (F)",
                "Pengajuan ke Bank (D)",
                "Approved (A)",
                "Rejected (R)",
                "Cancelled (C)",
                "Batal (B)",
                "Edit (E)",
                "Pending (P)",
            ]
            pilih_status = st.selectbox("📌 Filter Status:", opsi_status, key="status_all_select")
        with c_f3:
            pilih_keaktifan = st.selectbox("⚡ Keaktifan:", ["SEMUA", "Aktif", "Tidak Aktif"], key="aktif_all_select")
        with c_f4:
            opsi_bank = ["SEMUA BANK", "BRI", "MANDIRI", "BCA", "BNI", "PERMATA", "LAINNYA"]
            pilih_bank = st.selectbox("🏦 Filter Bank:", opsi_bank, key="bank_all_select")
        with c_f5:
            cari_cust_all = st.text_input("🔍 Cari Customer / NOKON:", placeholder="Ketik nama atau no. kontrak...", key="search_all_input")

        df_all_view = df_tracking.copy()
        if pilih_so_all != "SEMUA SALES":
            df_all_view = df_all_view[df_all_view["Sales"].str.upper() == pilih_so_all.upper()]
        if pilih_keaktifan != "SEMUA":
            df_all_view = df_all_view[df_all_view["Keaktifan"] == pilih_keaktifan]
        if pilih_bank != "SEMUA BANK":
            df_all_view = df_all_view[df_all_view["Bank"].str.upper() == pilih_bank.upper()]

        status_code_map = {
            "Open (O)": "O",
            "Bukcet Finance (F)": "F",
            "Pengajuan ke Bank (D)": "D",
            "Approved (A)": "A",
            "Rejected (R)": "R",
            "Cancelled (C)": "C",
            "Batal (B)": "B",
            "Edit (E)": "E",
            "Pending (P)": "P",
        }
        if pilih_status in status_code_map:
            df_all_view = df_all_view[df_all_view["Status_Code"] == status_code_map[pilih_status]]

        if cari_cust_all:
            m_n = df_all_view["Customer"].astype(str).str.contains(cari_cust_all, case=False, na=False)
            m_i = df_all_view["ID"].astype(str).str.contains(cari_cust_all, case=False, na=False)
            df_all_view = df_all_view[m_n | m_i]

        cnt_app = len(df_all_view[df_all_view["Status_Code"] == "A"])
        cnt_aktif = len(df_all_view[df_all_view["Keaktifan"] == "Aktif"])
        cnt_nonaktif = len(df_all_view[df_all_view["Keaktifan"] == "Tidak Aktif"])
        cnt_rej = len(df_all_view[df_all_view["Status_Code"] == "R"])

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Data", len(df_all_view))
        k2.metric("Approved (A)", cnt_app)
        k3.metric("Status Aktif", cnt_aktif)
        k4.metric("Tidak Aktif (C/B)", cnt_nonaktif)
        k5.metric("Rejected (R)", cnt_rej)

        st.markdown("---")
        st.subheader("👥 Rekap Progress per Sales Officer")
        if not df_all_view.empty:
            rekap_rows = []
            for so_name, grp in df_all_view.groupby("Sales"):
                so_label = so_name if so_name.strip() != "" else "(Tanpa Nama SO)"
                tot_s = len(grp)
                app_s = len(grp[grp["Status_Code"] == "A"])
                akt_s = len(grp[grp["Keaktifan"] == "Aktif"])
                nonakt_s = len(grp[grp["Keaktifan"] == "Tidak Aktif"])
                rej_s = len(grp[grp["Status_Code"] == "R"])
                pct_app = (app_s / tot_s * 100) if tot_s > 0 else 0.0
                rekap_rows.append({
                    "Sales Officer": so_label,
                    "Total Data": tot_s,
                    "Approved (A)": app_s,
                    "Aktif": akt_s,
                    "Tidak Aktif (C/B)": nonakt_s,
                    "Rejected (R)": rej_s,
                    "% Approved": f"{pct_app:.1f}%"
                })
            df_rekap_so = pd.DataFrame(rekap_rows).sort_values(by=["Total Data", "Approved (A)"], ascending=False)
            st.dataframe(df_rekap_so, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data rekap SO untuk filter saat ini.")

        st.markdown("---")
        st.subheader(f"📄 Detail Progress Seluruh Nasabah ({len(df_all_view)} Data)")
        if not df_all_view.empty:
            df_detail = df_all_view.copy()
            df_detail["Cabang / Area"] = df_detail.apply(extract_cabang_area, axis=1)
            df_detail["Aging / Tanggal"] = df_detail.apply(extract_aging_tanggal, axis=1)
            kol_detail = [
                c for c in [
                    "ID", "Customer", "Sales", "Bank", "Cabang / Area",
                    "Aging / Tanggal", "Status_Code", "Status", "Keaktifan", "Alasan Reject"
                ] if c in df_detail.columns
            ]
            st.dataframe(df_detail[kol_detail], use_container_width=True, hide_index=True)
        else:
            st.warning("Tidak ada data nasabah yang cocok dengan filter yang dipilih.")

    elif menu_pilihan == "📋 Sales Tracking Reject":
        st.title("📋 Sales Tracking Reject")
        st.markdown("Pusat pemantauan dan pengelolaan penolakan (*reject / R*) penagihan autodebet nasabah.")
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            so_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
            daftar_filter_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SO_MAKASSAR + so_di_data))
            pilih_sales = st.selectbox("👤 Pilih Nama Sales Officer:", daftar_filter_sales)
        with col_f2:
            search_box = st.text_input("🔍 Cari Nama / No. Kontrak:", placeholder="Ketik nama customer atau NOKON...")

        st.markdown("---")

        df_view = df_tracking[df_tracking["Status_Code"] == "R"].copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"].str.upper() == pilih_sales.upper()]
        if search_box:
            mask_nama = df_view["Customer"].astype(str).str.contains(search_box, case=False, na=False)
            mask_id = df_view["ID"].astype(str).str.contains(search_box, case=False, na=False)
            df_view = df_view[mask_nama | mask_id]

        st.info("💡 **Akses Database Pusat:** Untuk mengelola, menambah, atau menghapus data secara langsung, silakan buka Google Sheets utama.")
        st.markdown('<a href="https://docs.google.com/spreadsheets/d/1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M/edit" target="_blank"><button style="background-color:#10b981; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer;">📂 Buka Google Sheets Database Utama</button></a>', unsafe_allow_html=True)

        st.markdown(f"### Daftar Tanggungan Rejected ({len(df_view)} Data)")
        
        if len(df_view) == 0:
            st.warning("Tidak ada data rejected yang ditemukan untuk filter tersebut.")
        else:
            if pilih_sales != "SEMUA SALES" and len(df_view) > 1:
                pesan_rekap_so = build_wa_rekap_message(df_view, pilih_sales)
                url_rekap_so = f"https://wa.me/?text={urllib.parse.quote(pesan_rekap_so)}"
                with st.container():
                    st.markdown(f"""
                        <div class="rekap-box">
                            <strong style="color:#ffffff; font-size:16px;">📲 Opsi Rekap Sekaligus untuk {pilih_sales} ({len(df_view)} Nasabah)</strong><br>
                            <small style="color:#9ca3af;">Menggabungkan seluruh {len(df_view)} nasabah reject milik {pilih_sales} ke dalam 1 pesan WA bernomor (lengkap Cabang/Area, Aging/Tanggal, Alasan & Solusi).</small>
                        </div>
                    """, unsafe_allow_html=True)
                    col_r1, col_r2 = st.columns([1.4, 2.6])
                    with col_r1:
                        st.markdown(
                            f'<a href="{url_rekap_so}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:6px; font-weight:bold; cursor:pointer;">📨 Kirim Rekap Sekaligus ({len(df_view)} Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    with col_r2:
                        with st.expander("👁️ Lihat / Salin Teks Rekap WA SO"):
                            st.text_area("Teks Rekap WA SO", value=pesan_rekap_so, height=220, label_visibility="collapsed")
                st.markdown("---")

            for _, row in df_view.iterrows():
                sales_nama = clean_text(row.get("Sales", ""), "-")
                alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum di sheet")
                cabang_area = extract_cabang_area(row)
                aging_tgl = extract_aging_tanggal(row)

                wa_item_msg = build_wa_item_message(row)
                wa_item_url = f"https://wa.me/?text={urllib.parse.quote(wa_item_msg)}"

                df_so_ini = df_view[df_view["Sales"] == row.get("Sales", "")]
                jml_so_ini = len(df_so_ini)
                wa_so_group_msg = build_wa_rekap_message(df_so_ini, sales_nama)
                wa_so_group_url = f"https://wa.me/?text={urllib.parse.quote(wa_so_group_msg)}"

                with st.container():
                    st.markdown(f"""
                        <div class="reject-box">
                            <strong>{clean_text(row.get('Customer', ''))}</strong> ({clean_text(row.get('Bank', ''))} - No. Kontrak: {clean_text(row.get('ID', ''))})<br>
                            <small>Sales Officer: <b>{sales_nama}</b> &nbsp;|&nbsp; Status: <b>{clean_text(row.get('Status', 'Rejected'))} ({clean_text(row.get('Status_Code', 'R'))})</b> &nbsp;|&nbsp; Total Reject SO ini: <b>{jml_so_ini} Nasabah</b></small><br>
                            <small>📍 Cabang/Area: <b>{cabang_area}</b> &nbsp;|&nbsp; ⏳ Aging/Tanggal: <b>{aging_tgl}</b></small><br>
                            <span class="reject-reason">❌ Alasan Reject: {alasan}</span>
                            <div class="solution-box">
                                <span>💡 Solusi Perbaikan:</span><br>
                                {clean_text(row.get('Solusi', ''))}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    if jml_so_ini > 1:
                        b_col1, b_col2 = st.columns([1.2, 2.8])
                        with b_col1:
                            st.markdown(
                                f'<a href="{wa_item_url}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; cursor:pointer;">💬 Kirim 1 Nasabah Saja</button></a>',
                                unsafe_allow_html=True
                            )
                        with b_col2:
                            st.markdown(
                                f'<a href="{wa_so_group_url}" target="_blank"><button style="background-color:#1d4ed8; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; cursor:pointer;">📋 Rekap Semua ({jml_so_ini} Nasabah {sales_nama})</button></a>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            f'<a href="{wa_item_url}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer;">💬 Kirim WA ke SO (1 Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    st.markdown("---")

    elif menu_pilihan == "📖 Reject Guide":
        st.header("📖 Panduan Penanganan Reject & Solusi SO")
        st.markdown("Acuan standar operasional lengkap untuk penanganan penolakan autodebet dan tindakan korektif Sales Officer di ACC Cabang Makassar.")
        
        search_guide = st.text_input("🔍 Cari Kata Kunci Panduan / Solusi:", placeholder="Contoh: tanda tangan, rekening, telepon, brimo, saldo, dormant...")
        
        df_g = pd.DataFrame(REJECT_GUIDE_ITEMS)
        if search_guide:
            mask_g = (
                df_g["Alasan Reject"].str.contains(search_guide, case=False, na=False) |
                df_g["Keterangan"].str.contains(search_guide, case=False, na=False) |
                df_g["Tindakan Korektif / Solusi SO"].str.contains(search_guide, case=False, na=False)
            )
            df_g = df_g[mask_g]
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    elif menu_pilihan == "⚙️ Pengaturan & Database":
        st.subheader("⚙️ Pengaturan Sistem & Database Google Sheets")
        st.write("Versi Web: **AUTOTEAM** (Autodebet Team Achievement & Monitoring) v7.3")
        if is_live:
            st.success(f"Status: Terhubung Sempurna ke Google Sheets Database Utama (`DB_AutoMonitor_Makassar` — {total_data} Data)")
        else:
            st.warning("Status: Menggunakan mode cadangan sementara. Pastikan akses berbagi Google Sheets diset 'Siapa saja yang memiliki link dapat melihat'.")
        
        st.markdown("---")
        st.subheader("🔗 Akses Langsung Google Sheets")
        st.markdown("Anda dapat langsung mengelola, menambah, atau menghapus data Sales Officer melalui tautan berikut:")
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
            file_name="Backup_AUTOTEAM_Makassar.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == '__main__':
    main()
