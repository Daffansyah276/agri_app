"""
🌾 AgriFarm Pro - Aplikasi Pertanian Cerdas
Fitur:
  1. Kalkulator Pertanian (Pupuk, Irigasi, Hasil Panen, Pestisida, ROI)
  2. Pemantauan Suhu & Kadar Oksigen secara Real-time
  3. Deteksi Hama & Gulma menggunakan YOLOv8 Computer Vision
"""

import streamlit as st

# ─── Konfigurasi Halaman ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌾 AgriFarm Pro",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Kustom ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Warna utama tema hijau pertanian */
:root {
    --primary: #2d6a4f;
    --secondary: #52b788;
    --accent: #95d5b2;
    --bg: #f0fdf4;
    --card: #ffffff;
    --danger: #e63946;
    --warning: #f4a261;
    --info: #457b9d;
}

/* Background */
.stApp { background: linear-gradient(135deg, #e8f5e9 0%, #f0fdf4 50%, #e3f2fd 100%); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 100%) !important;
}
[data-testid="stSidebar"] * { color: #d8f3dc !important; }

/* Header utama */
.main-header {
    background: linear-gradient(135deg, #1b4332, #2d6a4f, #40916c);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(29,70,51,0.3);
}
.main-header h1 { font-size: 2.5rem; margin: 0; letter-spacing: 2px; }
.main-header p  { font-size: 1rem; opacity: 0.9; margin: 0.5rem 0 0; }

/* Kartu fitur */
.feature-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border-left: 5px solid #40916c;
    transition: transform 0.2s;
}
.feature-card:hover { transform: translateY(-2px); }

/* Gauge / badge status */
.status-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.85rem;
}
.status-ok      { background:#d8f3dc; color:#1b4332; }
.status-warning { background:#fff3cd; color:#856404; }
.status-danger  { background:#fce4ec; color:#c62828; }

/* Metric override */
[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)

# ─── Navigasi Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 AgriFarm Pro")
    st.markdown("---")
    menu = st.radio(
        "📋 **Menu Utama**",
        [
            "🏠 Beranda",
            "🧮 Kalkulator Pertanian",
            "🌡️ Pemantauan Lingkungan",
            "🔍 Deteksi Hama & Gulma (AI)",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**ℹ️ Versi:** 1.0.0")
    st.markdown("**📅 Teknologi:** YOLOv8 + Streamlit")
    st.caption("© 2024 AgriFarm Pro")

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN: BERANDA
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Beranda":
    st.markdown("""
    <div class="main-header">
        <h1>🌾 AgriFarm Pro</h1>
        <p>Sistem Manajemen Pertanian Cerdas — Kalkulator · Monitoring · AI Vision</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="feature-card">
            <h3>🧮 Kalkulator Pertanian</h3>
            <p>Hitung kebutuhan pupuk, irigasi, hasil panen, pestisida, dan analisis ROI secara akurat.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card">
            <h3>🌡️ Pemantauan Lingkungan</h3>
            <p>Monitor suhu, kelembaban, dan kadar oksigen kebun secara real-time dengan grafik dinamis.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card">
            <h3>🔍 Deteksi AI (YOLOv8)</h3>
            <p>Deteksi otomatis hama & gulma pada tanaman menggunakan model YOLOv8 Computer Vision.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 Pilih menu di sidebar kiri untuk mulai menggunakan aplikasi.")

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN: KALKULATOR PERTANIAN
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🧮 Kalkulator Pertanian":
    from pages import kalkulator
    kalkulator.show()

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN: PEMANTAUAN LINGKUNGAN
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🌡️ Pemantauan Lingkungan":
    from pages import monitoring
    monitoring.show()

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN: DETEKSI HAMA & GULMA (AI)
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🔍 Deteksi Hama & Gulma (AI)":
    from pages import deteksi_ai
    deteksi_ai.show()
