"""
Halaman Pemantauan Lingkungan — Suhu, Kelembaban, Kadar Oksigen
Simulasi data real-time + grafik historis dengan Plotly
"""

import streamlit as st
import random
import math
import time
import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Inisialisasi Riwayat Data ─────────────────────────────────────────────────
def init_history():
    if "sensor_history" not in st.session_state:
        now   = datetime.datetime.now()
        times = [now - datetime.timedelta(minutes=30 - i) for i in range(30)]
        st.session_state.sensor_history = pd.DataFrame({
            "waktu":      times,
            "suhu":       [26 + 4 * math.sin(i * 0.4) + random.uniform(-0.5, 0.5) for i in range(30)],
            "kelembaban": [65 + 10 * math.cos(i * 0.3) + random.uniform(-1, 1) for i in range(30)],
            "oksigen":    [20.9 + 0.5 * math.sin(i * 0.2) + random.uniform(-0.1, 0.1) for i in range(30)],
            "co2_ppm":    [400 + 50 * math.sin(i * 0.5) + random.uniform(-10, 10) for i in range(30)],
        })
    if "alert_log" not in st.session_state:
        st.session_state.alert_log = []

def generate_sensor_data(lokasi: str):
    """Simulasikan pembacaan sensor terbaru."""
    base = {
        "Lahan Padi Utara":   {"suhu": 29, "lembab": 80, "o2": 20.5, "co2": 450},
        "Lahan Jagung Selatan": {"suhu": 31, "lembab": 65, "o2": 20.8, "co2": 410},
        "Greenhouse Tomat":   {"suhu": 25, "lembab": 75, "o2": 21.0, "co2": 380},
        "Kebun Cabai Timur":  {"suhu": 32, "lembab": 60, "o2": 20.6, "co2": 420},
        "Semua Lokasi":       {"suhu": 29, "lembab": 70, "o2": 20.7, "co2": 415},
    }
    b = base.get(lokasi, base["Semua Lokasi"])
    t  = time.time()
    return {
        "suhu":       b["suhu"]  + 2 * math.sin(t * 0.1) + random.uniform(-0.8, 0.8),
        "kelembaban": b["lembab"]+ 5 * math.cos(t * 0.08)+ random.uniform(-2, 2),
        "oksigen":    b["o2"]    + 0.3 * math.sin(t * 0.05) + random.uniform(-0.1, 0.1),
        "co2_ppm":    b["co2"]   + 30 * math.cos(t * 0.07) + random.uniform(-10, 10),
        "waktu":      datetime.datetime.now(),
    }

def status_suhu(suhu):
    if 20 <= suhu <= 30:  return "🟢 Normal", "status-ok"
    if 30 < suhu <= 35:   return "🟡 Panas", "status-warning"
    return "🔴 Kritis", "status-danger"

def status_oksigen(o2):
    if o2 >= 20.5: return "🟢 Baik", "status-ok"
    if o2 >= 19.5: return "🟡 Rendah", "status-warning"
    return "🔴 Berbahaya", "status-danger"

def status_kelembaban(lembab):
    if 60 <= lembab <= 80: return "🟢 Ideal", "status-ok"
    if 50 <= lembab < 60 or 80 < lembab <= 90: return "🟡 Perhatian", "status-warning"
    return "🔴 Kritis", "status-danger"

def gauge_chart(value, title, min_val, max_val, unit, threshold_low, threshold_high):
    """Buat gauge chart Plotly."""
    if value < threshold_low:   color = "#e63946"
    elif value > threshold_high: color = "#f4a261"
    else:                        color = "#2d6a4f"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={"text": f"<b>{title}</b>", "font": {"size": 14}},
        number={"suffix": f" {unit}", "font": {"size": 24}},
        delta={"reference": (threshold_low + threshold_high) / 2, "valueformat": ".1f"},
        gauge={
            "axis": {"range": [min_val, max_val], "tickwidth": 1},
            "bar":  {"color": color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#cccccc",
            "steps": [
                {"range": [min_val, threshold_low],  "color": "#fce4ec"},
                {"range": [threshold_low, threshold_high], "color": "#e8f5e9"},
                {"range": [threshold_high, max_val], "color": "#fff3e0"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": threshold_high,
            },
        },
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# ─────────────────────────────────────────────────────────────────────────────
def show():
    init_history()
    st.markdown("## 🌡️ Pemantauan Lingkungan Real-Time")
    st.markdown("Monitor suhu, kelembaban, dan kadar oksigen kebun Anda secara langsung.")
    st.markdown("---")

    # ── Kontrol Sidebar Monitoring ────────────────────────────────────────
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 1])
    with col_ctrl1:
        lokasi = st.selectbox("📍 Pilih Lokasi Sensor", [
            "Lahan Padi Utara", "Lahan Jagung Selatan",
            "Greenhouse Tomat", "Kebun Cabai Timur", "Semua Lokasi"
        ], key="mon_lokasi")
    with col_ctrl2:
        interval = st.select_slider("⏱️ Interval Refresh", ["5 det", "10 det", "30 det", "1 menit"], value="10 det")
    with col_ctrl3:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=False, key="mon_auto")

    # ── Baca Sensor ───────────────────────────────────────────────────────
    if st.button("📡 Baca Sensor Sekarang", type="primary", key="btn_baca_sensor") or auto_refresh:
        data = generate_sensor_data(lokasi)
        # Tambah ke history
        new_row = pd.DataFrame([data])
        st.session_state.sensor_history = pd.concat(
            [st.session_state.sensor_history, new_row], ignore_index=True
        ).tail(60)

        # Simpan data terkini di session
        st.session_state.last_sensor = data

        # Periksa alert
        alerts = []
        if data["suhu"] > 35:    alerts.append(f"⚠️ SUHU TINGGI: {data['suhu']:.1f}°C di {lokasi}")
        if data["suhu"] < 15:    alerts.append(f"⚠️ SUHU RENDAH: {data['suhu']:.1f}°C di {lokasi}")
        if data["oksigen"] < 19.5: alerts.append(f"🚨 O₂ RENDAH: {data['oksigen']:.2f}% di {lokasi}")
        if data["kelembaban"] > 90: alerts.append(f"⚠️ KELEMBABAN TINGGI: {data['kelembaban']:.1f}% di {lokasi}")
        for a in alerts:
            st.session_state.alert_log.append({"waktu": data["waktu"].strftime("%H:%M:%S"), "pesan": a})

    # Gunakan data terbaru atau default
    if "last_sensor" in st.session_state:
        d = st.session_state.last_sensor
    else:
        d = generate_sensor_data(lokasi)

    # ── Metric Cards ──────────────────────────────────────────────────────
    st.markdown("#### 📊 Pembacaan Sensor Terkini")
    m1, m2, m3, m4 = st.columns(4)

    s_suhu, _ = status_suhu(d["suhu"])
    s_o2, _   = status_oksigen(d["oksigen"])
    s_lembab, _ = status_kelembaban(d["kelembaban"])

    m1.metric("🌡️ Suhu Udara", f"{d['suhu']:.1f} °C", f"{s_suhu}")
    m2.metric("💧 Kelembaban", f"{d['kelembaban']:.1f} %", f"{s_lembab}")
    m3.metric("🫧 Kadar O₂", f"{d['oksigen']:.2f} %", f"{s_o2}")
    m4.metric("💨 CO₂", f"{d['co2_ppm']:.0f} ppm")

    # ── Gauge Charts ──────────────────────────────────────────────────────
    st.markdown("#### 🎛️ Gauge Sensor")
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.plotly_chart(gauge_chart(d["suhu"], "Suhu", 10, 45, "°C", 20, 32), use_container_width=True)
    with g2:
        st.plotly_chart(gauge_chart(d["kelembaban"], "Kelembaban", 20, 100, "%", 60, 80), use_container_width=True)
    with g3:
        st.plotly_chart(gauge_chart(d["oksigen"], "Kadar O₂", 15, 22, "%", 19.5, 21.5), use_container_width=True)
    with g4:
        st.plotly_chart(gauge_chart(d["co2_ppm"], "CO₂", 350, 600, "ppm", 350, 450), use_container_width=True)

    # ── Grafik Historis ───────────────────────────────────────────────────
    st.markdown("#### 📈 Grafik Historis (60 Pembacaan Terakhir)")
    hist = st.session_state.sensor_history.tail(60).copy()
    hist["waktu_str"] = hist["waktu"].apply(lambda x: x.strftime("%H:%M"))

    tab_g1, tab_g2, tab_g3, tab_g4 = st.tabs(["🌡️ Suhu", "💧 Kelembaban", "🫧 Oksigen", "💨 CO₂"])

    def line_chart(df, y_col, title, color, y_label, low=None, high=None):
        fig = px.line(df, x="waktu_str", y=y_col, title=title,
                      labels={"waktu_str": "Waktu", y_col: y_label},
                      color_discrete_sequence=[color])
        if low:  fig.add_hline(y=low, line_dash="dash", line_color="red", annotation_text=f"Min: {low}")
        if high: fig.add_hline(y=high, line_dash="dash", line_color="orange", annotation_text=f"Max: {high}")
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(240,253,244,1)",
                          xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(0,0,0,0.05)"))
        return fig

    with tab_g1:
        st.plotly_chart(line_chart(hist, "suhu", "Riwayat Suhu", "#e63946", "Suhu (°C)", low=20, high=32), use_container_width=True)
    with tab_g2:
        st.plotly_chart(line_chart(hist, "kelembaban", "Riwayat Kelembaban", "#457b9d", "Kelembaban (%)", low=60, high=80), use_container_width=True)
    with tab_g3:
        st.plotly_chart(line_chart(hist, "oksigen", "Riwayat Kadar O₂", "#2d6a4f", "O₂ (%)", low=19.5, high=21.5), use_container_width=True)
    with tab_g4:
        st.plotly_chart(line_chart(hist, "co2_ppm", "Riwayat CO₂", "#f4a261", "CO₂ (ppm)", low=None, high=450), use_container_width=True)

    # ── Rentang Optimal Referensi ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 Referensi Rentang Optimal Sensor")
    ref_data = {
        "Parameter": ["🌡️ Suhu", "💧 Kelembaban", "🫧 Kadar O₂", "💨 CO₂"],
        "Optimal Min": ["20°C", "60%", "19.5%", "350 ppm"],
        "Optimal Max": ["32°C", "80%", "21.5%", "450 ppm"],
        "Kritis Min":  ["<15°C", "<50%", "<19%", "—"],
        "Kritis Max":  [">38°C", ">90%", "—", ">600 ppm"],
        "Dampak Tanaman": [
            "Pertumbuhan lambat / kematian",
            "Busuk akar / cendawan",
            "Fotosintesis terganggu",
            "Stunting / gangguan akar",
        ],
    }
    st.dataframe(pd.DataFrame(ref_data), use_container_width=True, hide_index=True)

    # ── Log Peringatan ─────────────────────────────────────────────────────
    if st.session_state.alert_log:
        st.markdown("---")
        st.markdown("#### 🚨 Log Peringatan")
        df_alert = pd.DataFrame(st.session_state.alert_log[-10:])
        st.dataframe(df_alert, use_container_width=True, hide_index=True)
        if st.button("🗑️ Hapus Log", key="clear_alert"):
            st.session_state.alert_log = []
            st.rerun()

    # ── Auto refresh menggunakan st.rerun ─────────────────────────────────
    if auto_refresh:
        interval_map = {"5 det": 5, "10 det": 10, "30 det": 30, "1 menit": 60}
        sec = interval_map.get(interval, 10)
        time.sleep(sec)
        st.rerun()
