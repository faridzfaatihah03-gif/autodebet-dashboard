import streamlit as st
import pandas as pd
import io
import html
import urllib.parse

# Konfigurasi Halaman
st.set_page_config(
    page_title="AUTOTEAM - Autodebet Team Achievement & Monitoring",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Korporat Profesional, Nuansa Biru ACC, Navigasi Berwarna & Animasi Halus
st.markdown("""
    <style>
    @keyframes floatTrophy {
        0%, 100% { transform: translateY(0px) scale(1); filter: drop-shadow(0 0 6px rgba(250, 204, 21, 0.55)); }
        50% { transform: translateY(-4px) scale(1.08); filter: drop-shadow(0 0 14px rgba(250, 204, 21, 0.9)); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 12px rgba(37, 99, 235, 0.35); }
        50% { box-shadow: 0 0 22px rgba(56, 189, 248, 0.65); }
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main {
        background-color: #0b1120;
    }
    footer {display: none !important; visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}

    /* Sidebar Lebih Berwarna, Elegan & Beranimasi */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071330 0%, #0b1f4d 52%, #091738 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.25);
    }
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
    }
    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(15, 35, 82, 0.72);
        border: 1px solid rgba(96, 165, 250, 0.28);
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 4px;
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        transform: translateX(5px);
        background: linear-gradient(90deg, rgba(0, 85, 204, 0.85), rgba(14, 116, 144, 0.78));
        border-color: #7dd3fc;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.32);
    }
    section[data-testid="stSidebar"] .stRadio label:nth-child(1) { border-left-color: #38bdf8; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(2) { border-left-color: #34d399; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(3) { border-left-color: #fbbf24; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(4) { border-left-color: #f87171; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(5) { border-left-color: #a78bfa; }
    section[data-testid="stSidebar"] .stRadio label:nth-child(6) { border-left-color: #2dd4bf; }

    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: linear-gradient(90deg, #0044b3 0%, #0284c7 100%) !important;
        border: 1px solid #bae6fd !important;
        border-left: 5px solid #facc15 !important;
        transform: translateX(6px);
        animation: pulseGlow 2.8s infinite ease-in-out;
    }
    section[data-testid="stSidebar"] .stRadio label p {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Hero Banner Atas Agar Ramai & Hidup */
    .hero-banner {
        background: linear-gradient(120deg, #002366, #0044b3, #0369a1, #002b7f);
        background-size: 250% 250%;
        animation: gradientShift 9s ease infinite, fadeSlideUp 0.5s ease-out;
        padding: 20px 24px;
        border-radius: 14px;
        border: 1px solid rgba(125, 211, 252, 0.45);
        box-shadow: 0 8px 24px rgba(0, 35, 102, 0.45);
        margin-bottom: 18px;
    }
    .hero-title {
        color: #ffffff !important;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.4px;
    }
    .hero-sub {
        color: #e0f2fe !important;
        font-size: 14.5px;
        margin-top: 4px;
        margin-bottom: 10px;
    }

    .tagline-pill {
        display: inline-block;
        background: linear-gradient(90deg, #003399, #0284c7, #0055cc);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 700;
        letter-spacing: 0.6px;
        margin-top: 2px;
        margin-bottom: 6px;
        border: 1px solid #7dd3fc;
    }

    /* Kartu KPI & Bank Biru ACC */
    .metric-card {
        background: linear-gradient(145deg, #002b7f 0%, #0044b3 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 35, 102, 0.45);
        border: 1px solid #3b82f6;
        text-align: center;
        margin-bottom: 10px;
        color: #ffffff !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeSlideUp 0.45s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.55);
    }
    .metric-label {
        color: #dbeafe !important;
        font-size: 14px;
        font-weight: 600;
    }
    .metric-value {
        color: #ffffff !important;
        margin: 6px 0;
        font-weight: 800;
    }
    .metric-sub {
        color: #bae6fd !important;
        font-size: 12.5px;
    }
    .bank-card {
        background: linear-gradient(160deg, #00266e 0%, #003d9e 100%);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0, 25, 80, 0.35);
        border: 1px solid #2563eb;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 8px;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .bank-card:hover {
        transform: translateY(-3px);
        border-color: #7dd3fc;
    }
    .bank-title {
        color: #93c5fd !important;
        font-size: 16px;
        font-weight: 700;
    }
    .bank-rate {
        margin: 6px 0;
        color: #ffffff !important;
        font-weight: 800;
    }
    .bank-sub {
        color: #e0f2fe !important;
        font-size: 12px;
    }
    .bank-badge {
        color: #fef08a !important;
        font-weight: 600;
    }

    /* Sales Leaderboard Styling (Top 5 Trophy Cards + Bottom 5 Seragam) */
    .lb-panel {
        background: linear-gradient(165deg, #0b1d45 0%, #102a63 100%);
        border: 1px solid #2563eb;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 6px 18px rgba(0, 28, 85, 0.4);
        animation: fadeSlideUp 0.55s ease-out;
    }
    .lb-panel-title {
        color: #ffffff !important;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(147, 197, 253, 0.25);
    }
    .top-rank-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, rgba(0, 51, 153, 0.85), rgba(3, 105, 161, 0.65));
        border: 1px solid rgba(125, 211, 252, 0.38);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }
    .top-rank-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.35);
    }
    .top-rank-1 {
        background: linear-gradient(90deg, rgba(161, 98, 7, 0.55), rgba(0, 68, 179, 0.9));
        border: 1px solid #facc15;
    }
    .top-rank-2 {
        background: linear-gradient(90deg, rgba(71, 85, 105, 0.6), rgba(0, 68, 179, 0.88));
        border: 1px solid #e2e8f0;
    }
    .top-rank-3 {
        background: linear-gradient(90deg, rgba(146, 64, 14, 0.55), rgba(0, 68, 179, 0.88));
        border: 1px solid #f59e0b;
    }
    .trophy-anim {
        display: inline-block;
        font-size: 22px;
        margin-right: 10px;
        animation: floatTrophy 2.2s infinite ease-in-out;
    }
    .rank-name {
        color: #ffffff !important;
        font-weight: 700;
        font-size: 14.5px;
    }
    .rank-meta {
        color: #bae6fd !important;
        font-size: 12px;
    }
    .rank-score-pill {
        background-color: #002366;
        color: #fef08a !important;
        border: 1px solid #facc15;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 13px;
        white-space: nowrap;
    }

    /* Tabel Bottom 5 Seragam dengan Tema Top 5 */
    .lb-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13.5px;
        color: #f8fafc;
        border-radius: 8px;
        overflow: hidden;
    }
    .lb-table thead tr {
        background: linear-gradient(90deg, #003399, #0369a1);
        color: #ffffff;
        text-align: left;
    }
    .lb-table th, .lb-table td {
        padding: 10px 12px;
        border-bottom: 1px solid rgba(147, 197, 253, 0.2);
    }
    .lb-table tbody tr {
        background-color: rgba(15, 35, 82, 0.68);
        transition: background-color 0.2s ease;
    }
    .lb-table tbody tr:hover {
        background-color: rgba(29, 78, 216, 0.55);
    }
    .rej-pill {
        background-color: rgba(185, 28, 28, 0.85);
        color: #fecaca;
        border: 1px solid #f87171;
        padding: 2px 9px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
    }

    /* Kartu Reject & BNI */
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
    .bni-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #0055cc;
        border: 1px solid #374151;
        margin-bottom: 14px;
        color: #f3f4f6 !important;
    }
    .bni-box strong {
        color: #ffffff !important;
        font-size: 18px;
    }
    .bni-box small {
        color: #cbd5e1 !important;
        font-size: 13.5px;
    }
    .ceklis-badge {
        display: inline-block;
        background-color: #065f46;
        color: #6ee7b7;
        border: 1px solid #10b981;
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 13px;
        margin-top: 6px;
    }
    .belum-ceklis-badge {
        display: inline-block;
        background-color: #1e293b;
        color: #93c5fd;
        border: 1px solid #3b82f6;
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 13px;
        margin-top: 6px;
    }
    .rekap-box {
        background-color: #0f172a;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #2563eb;
        border-left: 5px solid #25d366;
        margin-bottom: 18px;
        color: #e5e7eb !important;
    }
    </style>
""", unsafe_allow_html=True)

# Daftar Resmi Sales ACC Cabang Makassar
DAFTAR_SALES_MAKASSAR = [
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
        "Tindakan Korektif / Solusi Sales": "Input ulang melalui menu AOL Autodebet CSO dan pastikan nomor HP sesuai dengan yang terdaftar di Bank/BRIMO. Jika belum sinkron, arahkan nasabah walk-in ke bank untuk pembaruan nomor HP."
    },
    {
        "No": 2,
        "Alasan Reject": "Phone number not found",
        "Keterangan": "Nomor telepon nasabah belum terdaftar atau tidak ditemukan pada sistem bank terkait saat proses pendaftaran autodebet.",
        "Tindakan Korektif / Solusi Sales": "Arahkan nasabah melakukan registrasi atau pembaruan data nomor HP aktif di bank terkait terlebih dahulu, lalu ajukan ulang."
    },
    {
        "No": 3,
        "Alasan Reject": "Scan Kartu ATM Meragukan / No. Kartu ATM Invalid",
        "Keterangan": "Foto atau scan kartu ATM kurang jelas/buram, atau nasabah sudah melakukan penggantian kartu ATM sehingga nomor kartu lama sudah tidak berlaku.",
        "Tindakan Korektif / Solusi Sales": "Minta foto/scan kartu ATM terbaru yang jelas dan valid (pastikan tidak terpotong/buram), lalu lakukan pengajuan ulang."
    },
    {
        "No": 4,
        "Alasan Reject": "Tanda Tangan Tidak Menyentuh Materai / Tidak Sesuai",
        "Keterangan": "Tanda tangan pada form kuasa/SKPR tidak menyentuh materai atau tidak cocok dengan spesimen tanda tangan pada KTP/buku tabungan.",
        "Tindakan Korektif / Solusi Sales": "Lengkapi ulang tanda tangan di atas materai sesuai spesimen KTP/rekening bank nasabah dan pastikan tidak menyimpang dari batas ketentuan."
    },
    {
        "No": 5,
        "Alasan Reject": "Invalid format account number",
        "Keterangan": "Format nomor rekening tidak sesuai ketentuan bank, salah digit, atau terdapat spasi/karakter yang tidak valid.",
        "Tindakan Korektif / Solusi Sales": "Periksa kembali nomor rekening nasabah sesuai buku tabungan/rekening asli tanpa spasi atau karakter tambahan, lalu input ulang."
    },
    {
        "No": 6,
        "Alasan Reject": "Saldo tidak mencukupi",
        "Keterangan": "Saldo rekening nasabah tidak mencukupi untuk memenuhi syarat minimum atau proses pendebetan/validasi.",
        "Tindakan Korektif / Solusi Sales": "Informasikan nasabah untuk memastikan saldo rekening mencukupi dan aktif sebelum proses penagihan/aktivasi berikutnya."
    },
    {
        "No": 7,
        "Alasan Reject": "Rekening tidak aktif / dormant",
        "Keterangan": "Rekening sumber autodebet dalam status dormant (tidak aktif) atau diblokir/terbatas transaksinya.",
        "Tindakan Korektif / Solusi Sales": "Arahkan nasabah untuk mengaktifkan kembali rekening (reaktivasi dormant) di cabang bank terkait."
    },
    {
        "No": 8,
        "Alasan Reject": "Data customer tidak sesuai",
        "Keterangan": "Terdapat ketidaksesuaian identitas nasabah (nama, NIK/KTP, atau data pendukung) antara kontrak/pengajuan dan data rekening bank.",
        "Tindakan Korektif / Solusi Sales": "Cocokkan kembali identitas nasabah di KTP, kontrak, dan rekening bank, lalu koordinasikan perbaikan data/dokumen pendukung."
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

# Pesan WA Polos (Tanpa Emotikon) - Reject Satuan
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
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        f"- Bank: {bank}",
        f"- Aging/Tanggal: {aging_tgl}",
        f"- Alasan Reject: {alasan}",
        f"- Solusi: {solusi}",
    ]
    return "\n".join(lines)

# Pesan WA Polos (Tanpa Emotikon) - Reject Rekap per Sales
def build_wa_rekap_message(df_rekap, nama_sales="Sales"):
    if df_rekap.empty:
        return ""
    sapaan = f"Halo Kak {nama_sales}," if nama_sales and nama_sales != "SEMUA SALES" else "Halo Tim Sales,"
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

        baris_sales = f"\n   Sales: {sales_item}" if nama_sales == "SEMUA SALES" else ""
        lines.append(
            f"{idx}. *{cust}* ({nokon}){baris_sales}\n"
            f"   Cabang/Area: {cabang_area}\n"
            f"   Bank: {bank}\n"
            f"   Aging/Tanggal: {aging_tgl}\n"
            f"   Alasan: {alasan}\n"
            f"   Solusi: {solusi}"
        )
        lines.append("")
    return "\n".join(lines).strip()

# Pesan WA Polos (Tanpa Emotikon) - BNI Status D (Pengajuan ke Bank -> Arahan ACC ONE)
def build_wa_bni_item_message(row):
    sales = clean_text(row.get("Sales", ""), "Kak")
    cust = clean_text(row.get("Customer", ""), "-")
    nokon = clean_text(row.get("ID", ""), "-")
    cabang_area = extract_cabang_area(row)
    aging_tgl = extract_aging_tanggal(row)

    lines = [
        f"Halo Kak {sales}, mohon arahkan nasabah BNI berikut untuk pengaktifan ACC ONE:",
        "",
        f"- Customer: {cust} ({nokon})",
        f"- Cabang/Area: {cabang_area}",
        "- Bank: BNI",
        "- Status: D (Pengajuan ke Bank)",
        f"- Aging/Tanggal: {aging_tgl}",
        "- Arahan: Wajib mengajukan dan mengaktifkan ACC ONE sesuai arahan Sales.",
    ]
    return "\n".join(lines)

def build_wa_bni_rekap_message(df_bni, nama_sales="Sales"):
    if df_bni.empty:
        return ""
    sapaan = f"Halo Kak {nama_sales}," if nama_sales and nama_sales != "SEMUA SALES" else "Halo Tim Sales,"
    lines = [
        sapaan,
        "Berikut daftar nasabah BNI status D (Pengajuan ke Bank) yang wajib diarahkan untuk pengaktifan ACC ONE:",
        ""
    ]
    for idx, (_, row) in enumerate(df_bni.iterrows(), start=1):
        cust = clean_text(row.get("Customer", ""), "-")
        nokon = clean_text(row.get("ID", ""), "-")
        cabang_area = extract_cabang_area(row)
        aging_tgl = extract_aging_tanggal(row)
        sales_item = clean_text(row.get("Sales", ""), "-")

        baris_sales = f"\n   Sales: {sales_item}" if nama_sales == "SEMUA SALES" else ""
        lines.append(
            f"{idx}. *{cust}* ({nokon}){baris_sales}\n"
            f"   Cabang/Area: {cabang_area}\n"
            f"   Bank: BNI | Status: D (Pengajuan ke Bank)\n"
            f"   Aging/Tanggal: {aging_tgl}\n"
            f"   Arahan: Pengaktifan ACC ONE oleh nasabah dengan arahan Sales."
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

if "bni_contacted_keys" not in st.session_state:
    st.session_state.bni_contacted_keys = set()

# Sidebar Navigasi Korporat Berwarna & Beranimasi
st.sidebar.markdown("""
    <div style="padding: 6px 2px 2px 2px;">
        <h2 style="color: #ffffff; margin: 0; font-weight: 800; letter-spacing: 0.5px;">⚡ AUTOTEAM</h2>
        <p style="color: #93c5fd; font-size: 12.5px; margin: 2px 0 8px 0;">Autodebet Team Achievement & Monitoring</p>
        <div class="tagline-pill">Monitor. Improve. Activate.</div>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<span style='color:#bae6fd; font-weight:700; font-size:13px;'>MENU UTAMA</span>", unsafe_allow_html=True)

menu_pilihan = st.sidebar.radio(
    "Navigasi",
    [
        "🎯 Home Dashboard",
        "📊 Status Customer",
        "🏛️ BNI Autodebet Tracking",
        "⚠️ Reject Tracking",
        "📘 Reject Guide",
        "🔧 Settings"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("ACC Cabang Makassar — Kolaborasi & monitoring performa autodebet tim lapangan.")

def build_sales_leaderboard(df):
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    rows = []
    for sales_name, grp in df.groupby("Sales"):
        s_label = sales_name.strip() if str(sales_name).strip() != "" else "(Tanpa Nama Sales)"
        tot = len(grp)
        app = len(grp[grp["Status_Code"] == "A"])
        rej = len(grp[grp["Status_Code"] == "R"])
        pct = (app / tot * 100.0) if tot > 0 else 0.0
        rows.append({
            "Sales": s_label,
            "Total Data": tot,
            "Approved (A)": app,
            "Rejected (R)": rej,
            "% Autodebet": round(pct, 1),
        })

    lb_df = pd.DataFrame(rows)
    if lb_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Top 5: seluruh Sales yang punya data, % Autodebet tertinggi & Rejected (R) paling sedikit
    top5 = lb_df.sort_values(
        by=["% Autodebet", "Rejected (R)", "Approved (A)", "Total Data"],
        ascending=[False, True, False, False]
    ).head(5).copy()
    top5.insert(0, "Rank", range(1, len(top5) + 1))

    # Bottom 5: Sales dengan Rejected (R) terbanyak
    bottom5 = lb_df.sort_values(
        by=["Rejected (R)", "% Autodebet", "Total Data"],
        ascending=[False, True, False]
    ).head(5).copy()
    bottom5.insert(0, "Rank", range(1, len(bottom5) + 1))

    return top5, bottom5

def render_top5_trophy_cards(top5_df):
    trophy_icons = {1: "🏆", 2: "🥈", 3: "🥉", 4: "🏅", 5: "🎖️"}
    rank_classes = {1: "top-rank-1", 2: "top-rank-2", 3: "top-rank-3"}
    html_parts = [
        '<div class="lb-panel">',
        '<div class="lb-panel-title">🏆 Top 5 Sales — Persentase Autodebet Tertinggi & Reject Paling Sedikit</div>'
    ]
    for _, r in top5_df.iterrows():
        rk = int(r["Rank"])
        t_icon = trophy_icons.get(rk, "🏆")
        extra_cls = rank_classes.get(rk, "")
        s_name = html.escape(str(r["Sales"]))
        tot_d = int(r["Total Data"])
        app_d = int(r["Approved (A)"])
        rej_d = int(r["Rejected (R)"])
        pct_v = float(r["% Autodebet"])
        html_parts.append(
            f'<div class="top-rank-card {extra_cls}">'
            f'  <div style="display:flex; align-items:center;">'
            f'    <span class="trophy-anim">{t_icon}</span>'
            f'    <div>'
            f'      <div class="rank-name">#{rk} &nbsp;{s_name}</div>'
            f'      <div class="rank-meta">Approved: <b>{app_d}</b> / {tot_d} Data &nbsp;|&nbsp; Rejected: <b>{rej_d}</b></div>'
            f'    </div>'
            f'  </div>'
            f'  <div class="rank-score-pill">{pct_v:.1f}%</div>'
            f'</div>'
        )
    html_parts.append('</div>')
    return "".join(html_parts)

def render_bottom5_styled_table(bottom5_df):
    html_parts = [
        '<div class="lb-panel">',
        '<div class="lb-panel-title">⚠️ Bottom 5 Sales — Rejected (R) Terbanyak</div>',
        '<table class="lb-table">',
        '<thead><tr><th>Rank</th><th>Nama Sales</th><th>Total</th><th>Approved</th><th>Rejected (R)</th><th>% Autodebet</th></tr></thead>',
        '<tbody>'
    ]
    for _, r in bottom5_df.iterrows():
        rk = int(r["Rank"])
        s_name = html.escape(str(r["Sales"]))
        tot_d = int(r["Total Data"])
        app_d = int(r["Approved (A)"])
        rej_d = int(r["Rejected (R)"])
        pct_v = float(r["% Autodebet"])
        html_parts.append(
            f'<tr>'
            f'  <td><b>#{rk}</b></td>'
            f'  <td><b>{s_name}</b></td>'
            f'  <td>{tot_d}</td>'
            f'  <td>{app_d}</td>'
            f'  <td><span class="rej-pill">{rej_d} Reject</span></td>'
            f'  <td><b>{pct_v:.1f}%</b></td>'
            f'</tr>'
        )
    html_parts.append('</tbody></table></div>')
    return "".join(html_parts)

def main():
    total_data = len(df_tracking)
    df_aktif = df_tracking[df_tracking["Keaktifan"] == "Aktif"] if not df_tracking.empty else pd.DataFrame()
    total_aktif = len(df_aktif)
    total_approved = len(df_tracking[df_tracking["Status_Code"] == "A"]) if not df_tracking.empty else 0
    total_rejected = len(df_tracking[df_tracking["Status_Code"] == "R"]) if not df_tracking.empty else 0
    success_rate_cabang = (total_approved / total_data * 100) if total_data > 0 else 0.0

    if menu_pilihan == "🎯 Home Dashboard":
        st.markdown("""
            <div class="hero-banner">
                <div class="hero-title">⚡ AUTOTEAM — Home Dashboard</div>
                <div class="hero-sub">Autodebet Team Achievement & Monitoring — ACC Cabang Makassar</div>
                <div class="tagline-pill">Monitor. Improve. Activate.</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Data Tracking</div>
                    <h2 class="metric-value">{total_data}</h2>
                    <div class="metric-sub">Aktif: {total_aktif} | Non-Aktif (C/B): {total_data - total_aktif}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Rejected (R)</div>
                    <h2 class="metric-value">{total_rejected}</h2>
                    <div class="metric-sub">Status Aktif Perlu Tindak Lanjut</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Success Rate (Approved / A)</div>
                    <h2 class="metric-value">{success_rate_cabang:.1f}%</h2>
                    <div class="metric-sub">{total_approved} Approved dari {total_data} Data</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Server Status</div>
                    <h2 class="metric-value">Online</h2>
                    <div class="metric-sub">AUTOTEAM Active</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("Statistik Volume & Performa per Bank (Data Cabang Makassar)")
        
        bank_configs = ["BRI", "MANDIRI", "BCA", "BNI", "PERMATA"]
        bank_cols = st.columns(5)
        for idx, bank_name in enumerate(bank_configs):
            sub_b = df_tracking[df_tracking["Bank"] == bank_name]
            vol_b = len(sub_b)
            app_b = len(sub_b[sub_b["Status_Code"] == "A"])
            rate_b = (app_b / vol_b * 100) if vol_b > 0 else 0.0
            badge_label = "Top Rate" if rate_b >= 70 else ("Dominan" if vol_b >= 100 else ("Proses" if vol_b > 0 else "N/A"))
            with bank_cols[idx]:
                st.markdown(
                    f'<div class="bank-card">'
                    f'<div class="bank-title">{bank_name}</div>'
                    f'<h3 class="bank-rate">{rate_b:.1f}%</h3>'
                    f'<div class="bank-sub">Total: <b>{vol_b}</b> Nasabah ({app_b} Approved)</div>'
                    f'<small class="bank-badge">{badge_label}</small>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.subheader("Sales Leaderboard")
        top5_df, bottom5_df = build_sales_leaderboard(df_tracking)
        lb_col1, lb_col2 = st.columns(2)
        with lb_col1:
            if not top5_df.empty:
                st.markdown(render_top5_trophy_cards(top5_df), unsafe_allow_html=True)
            else:
                st.info("Belum ada data Sales.")
        with lb_col2:
            if not bottom5_df.empty:
                st.markdown(render_bottom5_styled_table(bottom5_df), unsafe_allow_html=True)
            else:
                st.info("Belum ada data Sales.")

        st.markdown("---")
        st.subheader("Master Data Nasabah & Status Tracking (Live from Google Sheets)")
        kolom_tampil = [c for c in ["NOKON", "NAMA_CUST", "CABANG", "NAME_SO", "BANK_AUTODEBET", "STATUS PENDAFTARAN", "Status", "Keaktifan", "REASON REJECT"] if c in df_tracking.columns]
        st.dataframe(df_tracking[kolom_tampil] if kolom_tampil else df_tracking, use_container_width=True, hide_index=True)

    elif menu_pilihan == "📊 Status Customer":
        st.title("⚡ AUTOTEAM — Status Customer")
        st.markdown("Pemantauan menyeluruh progress pengajuan seluruh nasabah dan kontribusi performa setiap Sales.")

        c_f1, c_f2, c_f3, c_f4, c_f5 = st.columns([1.8, 1.3, 1.1, 1.1, 1.5])
        with c_f1:
            sales_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
            opsi_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SALES_MAKASSAR + sales_di_data))
            pilih_sales_all = st.selectbox("Filter Sales:", opsi_sales, key="sales_all_select")
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
            pilih_status = st.selectbox("Filter Status:", opsi_status, key="status_all_select")
        with c_f3:
            pilih_keaktifan = st.selectbox("Keaktifan:", ["SEMUA", "Aktif", "Tidak Aktif"], key="aktif_all_select")
        with c_f4:
            opsi_bank = ["SEMUA BANK", "BRI", "MANDIRI", "BCA", "BNI", "PERMATA", "LAINNYA"]
            pilih_bank = st.selectbox("Filter Bank:", opsi_bank, key="bank_all_select")
        with c_f5:
            cari_cust_all = st.text_input("Cari Customer / NOKON:", placeholder="Ketik nama atau no. kontrak...", key="search_all_input")

        df_all_view = df_tracking.copy()
        if pilih_sales_all != "SEMUA SALES":
            df_all_view = df_all_view[df_all_view["Sales"].str.upper() == pilih_sales_all.upper()]
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
        st.subheader("Rekap Progress per Sales")
        if not df_all_view.empty:
            rekap_rows = []
            for sales_name, grp in df_all_view.groupby("Sales"):
                s_label = sales_name if sales_name.strip() != "" else "(Tanpa Nama Sales)"
                tot_s = len(grp)
                app_s = len(grp[grp["Status_Code"] == "A"])
                akt_s = len(grp[grp["Keaktifan"] == "Aktif"])
                nonakt_s = len(grp[grp["Keaktifan"] == "Tidak Aktif"])
                rej_s = len(grp[grp["Status_Code"] == "R"])
                pct_app = (app_s / tot_s * 100) if tot_s > 0 else 0.0
                rekap_rows.append({
                    "Sales": s_label,
                    "Total Data": tot_s,
                    "Approved (A)": app_s,
                    "Aktif": akt_s,
                    "Tidak Aktif (C/B)": nonakt_s,
                    "Rejected (R)": rej_s,
                    "% Approved": f"{pct_app:.1f}%"
                })
            df_rekap_sales = pd.DataFrame(rekap_rows).sort_values(by=["Total Data", "Approved (A)"], ascending=False)
            st.dataframe(df_rekap_sales, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data rekap Sales untuk filter saat ini.")

        st.markdown("---")
        st.subheader(f"Detail Progress Seluruh Nasabah ({len(df_all_view)} Data)")
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

    elif menu_pilihan == "🏛️ BNI Autodebet Tracking":
        st.title("⚡ AUTOTEAM — BNI Autodebet Tracking")
        st.markdown("Pemantauan nasabah **BNI** berstatus **D (Pengajuan ke Bank)** yang diarahkan untuk pengaktifan **ACC ONE**.")

        df_bni_d = df_tracking[
            (df_tracking["Bank"] == "BNI") & (df_tracking["Status_Code"] == "D")
        ].copy()

        f_b1, f_b2 = st.columns([2, 1.5])
        with f_b1:
            sales_bni_list = sorted([s for s in df_bni_d["Sales"].unique() if s not in ["", "-"]])
            opsi_sales_bni = ["SEMUA SALES"] + list(dict.fromkeys([s for s in DAFTAR_SALES_MAKASSAR if s in sales_bni_list] + sales_bni_list))
            pilih_sales_bni = st.selectbox("Pilih Nama Sales (BNI Status D):", opsi_sales_bni, key="bni_sales_select")
        with f_b2:
            cari_bni = st.text_input("Cari Customer / NOKON:", placeholder="Ketik nama atau no. kontrak...", key="bni_search_input")

        if pilih_sales_bni != "SEMUA SALES":
            df_bni_d = df_bni_d[df_bni_d["Sales"].str.upper() == pilih_sales_bni.upper()]
        if cari_bni:
            m_n = df_bni_d["Customer"].astype(str).str.contains(cari_bni, case=False, na=False)
            m_i = df_bni_d["ID"].astype(str).str.contains(cari_bni, case=False, na=False)
            df_bni_d = df_bni_d[m_n | m_i]

        b_k1, b_k2, b_k3 = st.columns(3)
        b_k1.metric("Nasabah BNI Status D", len(df_bni_d))
        b_k2.metric("Jumlah Sales Terkait", df_bni_d["Sales"].nunique() if not df_bni_d.empty else 0)
        b_k3.metric("Sudah Dihubungi (ACC ONE)", sum(
            1 for idx, r in df_bni_d.iterrows()
            if f"{clean_text(r.get('ID', ''))}_{clean_text(r.get('Customer', ''))}_{idx}" in st.session_state.bni_contacted_keys
        ))

        st.markdown("---")
        if df_bni_d.empty:
            st.info("Tidak ada nasabah BNI berstatus D (Pengajuan ke Bank) untuk filter saat ini.")
        else:
            if pilih_sales_bni != "SEMUA SALES" and len(df_bni_d) > 1:
                pesan_bni_rekap = build_wa_bni_rekap_message(df_bni_d, pilih_sales_bni)
                url_bni_rekap = f"https://wa.me/?text={urllib.parse.quote(pesan_bni_rekap)}"
                with st.container():
                    st.markdown(f"""
                        <div class="rekap-box">
                            <strong style="color:#ffffff; font-size:16px;">Rekap Sekaligus Arahan ACC ONE untuk {pilih_sales_bni} ({len(df_bni_d)} Nasabah)</strong><br>
                            <small style="color:#9ca3af;">Menggabungkan seluruh nasabah BNI status D milik {pilih_sales_bni} ke dalam satu pesan WA polos untuk arahan pengaktifan ACC ONE.</small>
                        </div>
                    """, unsafe_allow_html=True)
                    col_br1, col_br2 = st.columns([1.4, 2.6])
                    with col_br1:
                        st.markdown(
                            f'<a href="{url_bni_rekap}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:6px; font-weight:bold; cursor:pointer;">Kirim Rekap WA ({len(df_bni_d)} Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    with col_br2:
                        with st.expander("Lihat / Salin Teks Pesan Rekap ACC ONE"):
                            st.text_area("Teks Rekap BNI ACC ONE", value=pesan_bni_rekap, height=200, label_visibility="collapsed")
                st.markdown("---")

            for idx, row in df_bni_d.iterrows():
                sales_nama = clean_text(row.get("Sales", ""), "-")
                cabang_area = extract_cabang_area(row)
                aging_tgl = extract_aging_tanggal(row)
                item_key = f"{clean_text(row.get('ID', ''))}_{clean_text(row.get('Customer', ''))}_{idx}"
                is_checked = item_key in st.session_state.bni_contacted_keys

                df_sales_bni = df_bni_d[df_bni_d["Sales"] == row.get("Sales", "")]
                jml_sales_bni = len(df_sales_bni)

                wa_bni_one = build_wa_bni_item_message(row)
                url_bni_one = f"https://wa.me/?text={urllib.parse.quote(wa_bni_one)}"

                wa_bni_grp = build_wa_bni_rekap_message(df_sales_bni, sales_nama)
                url_bni_grp = f"https://wa.me/?text={urllib.parse.quote(wa_bni_grp)}"

                with st.container():
                    card_c, status_c = st.columns([5.2, 1.3])
                    with card_c:
                        st.markdown(f"""
                            <div class="bni-box">
                                <strong>{clean_text(row.get('Customer', ''))}</strong> (No. Kontrak: {clean_text(row.get('ID', ''))})<br>
                                <small>Sales: <b>{sales_nama}</b> &nbsp;|&nbsp; Bank: <b>BNI</b> &nbsp;|&nbsp; Status: <b>D — Pengajuan ke Bank</b> &nbsp;|&nbsp; Total BNI (D) Sales ini: <b>{jml_sales_bni} Nasabah</b></small><br>
                                <small>Cabang/Area: <b>{cabang_area}</b> &nbsp;|&nbsp; Aging/Tanggal: <b>{aging_tgl}</b></small>
                            </div>
                        """, unsafe_allow_html=True)
                    with status_c:
                        checked_val = st.checkbox(
                            "Sudah dihubungi (ACC ONE)",
                            value=is_checked,
                            key=f"chk_bni_{item_key}"
                        )
                        if checked_val:
                            st.session_state.bni_contacted_keys.add(item_key)
                            st.markdown('<div class="ceklis-badge">✓ Sudah Dihubungi</div>', unsafe_allow_html=True)
                        else:
                            st.session_state.bni_contacted_keys.discard(item_key)
                            st.markdown('<div class="belum-ceklis-badge">Belum Dihubungi</div>', unsafe_allow_html=True)

                    if jml_sales_bni > 1:
                        bc1, bc2 = st.columns([1.2, 2.8])
                        with bc1:
                            st.markdown(
                                f'<a href="{url_bni_one}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; cursor:pointer;">Kirim 1 Nasabah Saja</button></a>',
                                unsafe_allow_html=True
                            )
                        with bc2:
                            st.markdown(
                                f'<a href="{url_bni_grp}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; cursor:pointer;">Rekap Semua ({jml_sales_bni} Nasabah {sales_nama})</button></a>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            f'<a href="{url_bni_one}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer;">Kirim WA Arahan ACC ONE</button></a>',
                            unsafe_allow_html=True
                        )
                    st.markdown("---")

    elif menu_pilihan == "⚠️ Reject Tracking":
        st.title("⚡ AUTOTEAM — Reject Tracking")
        st.markdown("Pusat pemantauan dan pengelolaan penolakan (Rejected / R) penagihan autodebet nasabah.")
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            sales_di_data = sorted([s for s in df_tracking["Sales"].unique() if s not in ["", "-"]])
            daftar_filter_sales = ["SEMUA SALES"] + list(dict.fromkeys(DAFTAR_SALES_MAKASSAR + sales_di_data))
            pilih_sales = st.selectbox("Pilih Nama Sales:", daftar_filter_sales)
        with col_f2:
            search_box = st.text_input("Cari Nama / No. Kontrak:", placeholder="Ketik nama customer atau NOKON...")

        st.markdown("---")

        df_view = df_tracking[df_tracking["Status_Code"] == "R"].copy()
        if pilih_sales != "SEMUA SALES":
            df_view = df_view[df_view["Sales"].str.upper() == pilih_sales.upper()]
        if search_box:
            mask_nama = df_view["Customer"].astype(str).str.contains(search_box, case=False, na=False)
            mask_id = df_view["ID"].astype(str).str.contains(search_box, case=False, na=False)
            df_view = df_view[mask_nama | mask_id]

        st.info("Akses Database Pusat: Untuk mengelola, menambah, atau menghapus data secara langsung, silakan buka Google Sheets utama.")
        st.markdown('<a href="https://docs.google.com/spreadsheets/d/1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M/edit" target="_blank"><button style="background-color:#10b981; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer;">Buka Google Sheets Database Utama</button></a>', unsafe_allow_html=True)

        st.markdown(f"### Daftar Tanggungan Rejected ({len(df_view)} Data)")
        
        if len(df_view) == 0:
            st.warning("Tidak ada data rejected yang ditemukan untuk filter tersebut.")
        else:
            if pilih_sales != "SEMUA SALES" and len(df_view) > 1:
                pesan_rekap_sales = build_wa_rekap_message(df_view, pilih_sales)
                url_rekap_sales = f"https://wa.me/?text={urllib.parse.quote(pesan_rekap_sales)}"
                with st.container():
                    st.markdown(f"""
                        <div class="rekap-box">
                            <strong style="color:#ffffff; font-size:16px;">Opsi Rekap Sekaligus untuk {pilih_sales} ({len(df_view)} Nasabah)</strong><br>
                            <small style="color:#9ca3af;">Menggabungkan seluruh {len(df_view)} nasabah reject milik {pilih_sales} ke dalam 1 pesan WA polos bernomor (lengkap Cabang/Area, Aging/Tanggal, Alasan & Solusi).</small>
                        </div>
                    """, unsafe_allow_html=True)
                    col_r1, col_r2 = st.columns([1.4, 2.6])
                    with col_r1:
                        st.markdown(
                            f'<a href="{url_rekap_sales}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:10px 18px; border-radius:6px; font-weight:bold; cursor:pointer;">Kirim Rekap Sekaligus ({len(df_view)} Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    with col_r2:
                        with st.expander("Lihat / Salin Teks Rekap WA Sales"):
                            st.text_area("Teks Rekap WA Sales", value=pesan_rekap_sales, height=220, label_visibility="collapsed")
                st.markdown("---")

            for _, row in df_view.iterrows():
                sales_nama = clean_text(row.get("Sales", ""), "-")
                alasan = clean_text(row.get("Alasan Reject", ""), "Alasan belum tercantum di sheet")
                cabang_area = extract_cabang_area(row)
                aging_tgl = extract_aging_tanggal(row)

                wa_item_msg = build_wa_item_message(row)
                wa_item_url = f"https://wa.me/?text={urllib.parse.quote(wa_item_msg)}"

                df_sales_ini = df_view[df_view["Sales"] == row.get("Sales", "")]
                jml_sales_ini = len(df_sales_ini)
                wa_sales_group_msg = build_wa_rekap_message(df_sales_ini, sales_nama)
                wa_sales_group_url = f"https://wa.me/?text={urllib.parse.quote(wa_sales_group_msg)}"

                with st.container():
                    st.markdown(f"""
                        <div class="reject-box">
                            <strong>{clean_text(row.get('Customer', ''))}</strong> ({clean_text(row.get('Bank', ''))} - No. Kontrak: {clean_text(row.get('ID', ''))})<br>
                            <small>Sales: <b>{sales_nama}</b> &nbsp;|&nbsp; Status: <b>{clean_text(row.get('Status', 'Rejected'))} ({clean_text(row.get('Status_Code', 'R'))})</b> &nbsp;|&nbsp; Total Reject Sales ini: <b>{jml_sales_ini} Nasabah</b></small><br>
                            <small>Cabang/Area: <b>{cabang_area}</b> &nbsp;|&nbsp; Aging/Tanggal: <b>{aging_tgl}</b></small><br>
                            <span class="reject-reason">Alasan Reject: {alasan}</span>
                            <div class="solution-box">
                                <span>Solusi Perbaikan:</span><br>
                                {clean_text(row.get('Solusi', ''))}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    if jml_sales_ini > 1:
                        b_col1, b_col2 = st.columns([1.2, 2.8])
                        with b_col1:
                            st.markdown(
                                f'<a href="{wa_item_url}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; cursor:pointer;">Kirim 1 Nasabah Saja</button></a>',
                                unsafe_allow_html=True
                            )
                        with b_col2:
                            st.markdown(
                                f'<a href="{wa_sales_group_url}" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; cursor:pointer;">Rekap Semua ({jml_sales_ini} Nasabah {sales_nama})</button></a>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            f'<a href="{wa_item_url}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer;">Kirim WA ke Sales (1 Nasabah)</button></a>',
                            unsafe_allow_html=True
                        )
                    st.markdown("---")

    elif menu_pilihan == "📘 Reject Guide":
        st.header("⚡ AUTOTEAM — Panduan Penanganan Reject & Solusi Sales")
        st.markdown("Acuan standar operasional lengkap untuk penanganan penolakan autodebet dan tindakan korektif Sales di ACC Cabang Makassar.")
        
        search_guide = st.text_input("Cari Kata Kunci Panduan / Solusi:", placeholder="Contoh: tanda tangan, rekening, telepon, brimo, saldo, dormant...")
        
        df_g = pd.DataFrame(REJECT_GUIDE_ITEMS)
        if search_guide:
            mask_g = (
                df_g["Alasan Reject"].str.contains(search_guide, case=False, na=False) |
                df_g["Keterangan"].str.contains(search_guide, case=False, na=False) |
                df_g["Tindakan Korektif / Solusi Sales"].str.contains(search_guide, case=False, na=False)
            )
            df_g = df_g[mask_g]
        st.dataframe(df_g, use_container_width=True, hide_index=True)

    elif menu_pilihan == "🔧 Settings":
        st.subheader("🔧 Pengaturan Sistem & Database Google Sheets")
        st.write("Versi Web: **AUTOTEAM** (Autodebet Team Achievement & Monitoring) v7.6")
        if is_live:
            st.success(f"Status: Terhubung Sempurna ke Google Sheets Database Utama (DB_AutoMonitor_Makassar — {total_data} Data)")
        else:
            st.warning("Status: Menggunakan mode cadangan sementara. Pastikan akses berbagi Google Sheets diset 'Siapa saja yang memiliki link dapat melihat'.")
        
        st.markdown("---")
        st.subheader("Akses Langsung Google Sheets")
        st.markdown("Anda dapat langsung mengelola, menambah, atau menghapus data Sales melalui tautan berikut:")
        st.markdown('<a href="https://docs.google.com/spreadsheets/d/1eGeosnjBbMnAK0I0pbIcGtTBxlOYTN4eUgtz9X5CM2M/edit" target="_blank"><button style="background-color:#0044b3; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer;">Buka Google Sheets Utama</button></a>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Download Backup Data (Excel)")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_tracking.to_excel(writer, sheet_name='Tracking_Backup', index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            label="Download Rekap Data Tracking (.xlsx)",
            data=excel_data,
            file_name="Backup_AUTOTEAM_Makassar.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == '__main__':
    main()
