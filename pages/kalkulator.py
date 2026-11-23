"""
Halaman Kalkulator Pertanian
Fitur: Pupuk, Irigasi, Hasil Panen, Pestisida, ROI
"""

import streamlit as st
import math

def show():
    st.markdown("## 🧮 Kalkulator Pertanian")
    st.markdown("Hitung kebutuhan pertanian Anda secara akurat dan efisien.")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌱 Pupuk",
        "💧 Irigasi",
        "🌾 Hasil Panen",
        "🐛 Pestisida",
        "💰 Analisis ROI",
    ])

    # ── TAB 1: KALKULATOR PUPUK ────────────────────────────────────────────
    with tab1:
        st.markdown("### 🌱 Kalkulator Kebutuhan Pupuk")
        st.markdown("Hitung dosis pupuk berdasarkan luas lahan dan jenis tanaman.")

        col1, col2 = st.columns(2)
        with col1:
            luas_lahan = st.number_input("📐 Luas Lahan (hektar)", min_value=0.1, value=1.0, step=0.1, key="pupuk_luas")
            jenis_tanaman = st.selectbox("🌿 Jenis Tanaman", [
                "Padi", "Jagung", "Kedelai", "Cabai", "Tomat",
                "Singkong", "Ubi Jalar", "Tebu", "Kelapa Sawit"
            ], key="pupuk_tanaman")

        with col2:
            jenis_pupuk = st.selectbox("🧪 Jenis Pupuk", [
                "NPK (16-16-16)", "Urea (46% N)", "SP-36 (36% P₂O₅)",
                "KCl (60% K₂O)", "ZA (21% N)", "Pupuk Organik"
            ], key="pupuk_jenis")
            fase_pertumbuhan = st.selectbox("🌱 Fase Pertumbuhan", [
                "Pembibitan", "Vegetatif Awal", "Vegetatif Aktif",
                "Generatif / Berbunga", "Pembuahan / Panen"
            ], key="pupuk_fase")

        # Referensi dosis pupuk per hektar (kg/ha) berdasarkan tanaman & pupuk
        dosis_ref = {
            ("Padi", "NPK (16-16-16)"): 300,
            ("Padi", "Urea (46% N)"): 200,
            ("Padi", "SP-36 (36% P₂O₅)"): 100,
            ("Padi", "KCl (60% K₂O)"): 100,
            ("Jagung", "NPK (16-16-16)"): 400,
            ("Jagung", "Urea (46% N)"): 300,
            ("Tomat", "NPK (16-16-16)"): 500,
            ("Cabai", "NPK (16-16-16)"): 450,
            ("Kedelai", "SP-36 (36% P₂O₅)"): 150,
        }
        # Faktor fase pertumbuhan
        faktor_fase = {
            "Pembibitan": 0.1,
            "Vegetatif Awal": 0.3,
            "Vegetatif Aktif": 0.4,
            "Generatif / Berbunga": 0.15,
            "Pembuahan / Panen": 0.05,
        }

        key = (jenis_tanaman, jenis_pupuk)
        dosis_base = dosis_ref.get(key, 350)  # default 350 kg/ha
        faktor = faktor_fase[fase_pertumbuhan]

        total_kebutuhan = luas_lahan * dosis_base * faktor
        per_aplikasi    = total_kebutuhan
        harga_pupuk     = {"NPK (16-16-16)": 10000, "Urea (46% N)": 7000,
                           "SP-36 (36% P₂O₅)": 8000, "KCl (60% K₂O)": 9000,
                           "ZA (21% N)": 5500, "Pupuk Organik": 3000}
        harga           = harga_pupuk.get(jenis_pupuk, 8000)
        biaya_total     = total_kebutuhan * harga / 1000  # per kg → Rp/kg

        if st.button("🔢 Hitung Kebutuhan Pupuk", key="btn_pupuk"):
            st.markdown("---")
            st.markdown("#### 📊 Hasil Perhitungan")
            c1, c2, c3 = st.columns(3)
            c1.metric("Dosis per Fase", f"{per_aplikasi:.1f} kg")
            c2.metric("Dosis per Hektar", f"{dosis_base * faktor:.1f} kg/ha")
            c3.metric("Estimasi Biaya", f"Rp {biaya_total:,.0f}")

            st.info(f"""
**Rekomendasi Aplikasi Pupuk:**
- **Tanaman:** {jenis_tanaman} | **Pupuk:** {jenis_pupuk}
- **Luas Lahan:** {luas_lahan} ha | **Fase:** {fase_pertumbuhan}
- **Total Pupuk Dibutuhkan:** {per_aplikasi:.2f} kg
- **Harga Satuan:** Rp {harga:,}/kg
- **Total Biaya Pupuk:** Rp {biaya_total:,.0f}

> ⚠️ Dosis berdasarkan standar Kementan RI. Sesuaikan dengan hasil uji tanah.
            """)

    # ── TAB 2: KALKULATOR IRIGASI ──────────────────────────────────────────
    with tab2:
        st.markdown("### 💧 Kalkulator Kebutuhan Irigasi")
        st.markdown("Hitung volume air yang dibutuhkan tanaman berdasarkan kondisi lahan.")

        col1, col2 = st.columns(2)
        with col1:
            luas_irigasi   = st.number_input("📐 Luas Lahan (hektar)", 0.1, 1000.0, 1.0, 0.1, key="irig_luas")
            jenis_tanaman2 = st.selectbox("🌿 Jenis Tanaman", ["Padi", "Jagung", "Cabai", "Tomat", "Kedelai"], key="irig_tan")
            metode_irigasi = st.selectbox("🚿 Metode Irigasi", [
                "Genangan / Flood", "Furrow / Alur", "Drip / Tetes", "Sprinkler"
            ], key="irig_met")

        with col2:
            suhu_udara   = st.slider("🌡️ Suhu Udara (°C)", 20, 40, 30, key="irig_suhu")
            kelembaban   = st.slider("💨 Kelembaban Relatif (%)", 30, 100, 70, key="irig_lembab")
            curah_hujan  = st.number_input("🌧️ Curah Hujan (mm/hari)", 0.0, 50.0, 2.0, 0.5, key="irig_hujan")
            durasi_irg   = st.number_input("📅 Durasi Irigasi (hari)", 1, 30, 7, 1, key="irig_dur")

        # Evapotranspirasi referensi (Penman-Monteith sederhana)
        ET0_base = {
            "Padi": 6.5, "Jagung": 5.5, "Cabai": 4.5,
            "Tomat": 5.0, "Kedelai": 5.0
        }
        Kc = {"Genangan / Flood": 1.2, "Furrow / Alur": 1.0, "Drip / Tetes": 0.75, "Sprinkler": 0.9}
        ET0   = ET0_base.get(jenis_tanaman2, 5.0) * (suhu_udara / 30) * ((110 - kelembaban) / 60)
        ETc   = ET0 * Kc[metode_irigasi]
        defisit_air = max(0, ETc - curah_hujan)
        volume_harian = defisit_air * luas_irigasi * 10000 / 1000  # m³/hari
        volume_total  = volume_harian * durasi_irg

        if st.button("💧 Hitung Kebutuhan Irigasi", key="btn_irigasi"):
            st.markdown("---")
            st.markdown("#### 📊 Hasil Perhitungan")
            c1, c2, c3 = st.columns(3)
            c1.metric("ET₀ (Referensi)", f"{ET0:.2f} mm/hari")
            c2.metric("ETc (Aktual)", f"{ETc:.2f} mm/hari")
            c3.metric("Defisit Air", f"{defisit_air:.2f} mm/hari")

            c4, c5 = st.columns(2)
            c4.metric("Volume Air/Hari", f"{volume_harian:,.1f} m³")
            c5.metric("Volume Total", f"{volume_total:,.1f} m³")

            st.success(f"""
**Jadwal Irigasi yang Direkomendasikan:**
- Frekuensi: Setiap **{max(1, int(ETc/defisit_air)) if defisit_air > 0 else 'N/A'} hari** sekali
- Durasi siram: **{durasi_irg} hari**
- Volume per sesi: **{volume_harian:,.0f} m³/hari**
            """)

    # ── TAB 3: ESTIMASI HASIL PANEN ───────────────────────────────────────
    with tab3:
        st.markdown("### 🌾 Estimasi Hasil Panen")

        col1, col2 = st.columns(2)
        with col1:
            luas_panen    = st.number_input("📐 Luas Lahan (hektar)", 0.1, 1000.0, 1.0, key="pan_luas")
            tanaman_panen = st.selectbox("🌿 Jenis Tanaman", [
                "Padi", "Jagung", "Kedelai", "Cabai Merah", "Tomat",
                "Singkong", "Ubi Jalar", "Tebu"
            ], key="pan_tan")
            varietas = st.selectbox("🌱 Kualitas Varietas", [
                "Lokal (standar)", "Hibrida (baik)", "Super Hibrida (terbaik)"
            ], key="pan_var")

        with col2:
            kondisi_tanah = st.select_slider("🌍 Kondisi Tanah", ["Buruk", "Cukup", "Baik", "Sangat Baik"], value="Baik", key="pan_tanah")
            pemupukan_ok  = st.checkbox("✅ Pemupukan Optimal", value=True, key="pan_pupuk")
            irigasi_ok    = st.checkbox("✅ Irigasi Optimal", value=True, key="pan_irig")
            hama_penyakit = st.select_slider("🐛 Tekanan Hama/Penyakit", ["Parah", "Sedang", "Ringan", "Tidak Ada"], value="Ringan", key="pan_hama")

        # Produktivitas dasar (ton/ha)
        prod_base = {
            "Padi": 6.0, "Jagung": 7.0, "Kedelai": 2.0,
            "Cabai Merah": 10.0, "Tomat": 25.0,
            "Singkong": 25.0, "Ubi Jalar": 20.0, "Tebu": 80.0
        }
        f_varietas = {"Lokal (standar)": 0.8, "Hibrida (baik)": 1.0, "Super Hibrida (terbaik)": 1.2}
        f_tanah    = {"Buruk": 0.6, "Cukup": 0.8, "Baik": 1.0, "Sangat Baik": 1.15}
        f_pupuk    = 1.1 if pemupukan_ok else 0.85
        f_irigasi  = 1.1 if irigasi_ok else 0.80
        f_hama     = {"Parah": 0.5, "Sedang": 0.75, "Ringan": 0.9, "Tidak Ada": 1.0}

        prod = (prod_base.get(tanaman_panen, 5.0)
                * f_varietas[varietas] * f_tanah[kondisi_tanah]
                * f_pupuk * f_irigasi * f_hama[hama_penyakit])
        total_panen = prod * luas_panen

        # Harga komoditas (Rp/kg)
        harga_komoditas = {
            "Padi": 5500, "Jagung": 4500, "Kedelai": 9000,
            "Cabai Merah": 25000, "Tomat": 8000,
            "Singkong": 2500, "Ubi Jalar": 4000, "Tebu": 600
        }
        harga_jual = harga_komoditas.get(tanaman_panen, 5000)
        pendapatan  = total_panen * 1000 * harga_jual  # ton → kg

        if st.button("🌾 Estimasi Hasil Panen", key="btn_panen"):
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("Produktivitas", f"{prod:.2f} ton/ha")
            c2.metric("Total Hasil Panen", f"{total_panen:.2f} ton")
            c3.metric("Estimasi Pendapatan", f"Rp {pendapatan:,.0f}")

            # Progress bar produktivitas
            max_prod = prod_base.get(tanaman_panen, 5.0) * 1.2
            st.markdown("**Produktivitas vs Potensi Maksimum:**")
            st.progress(min(1.0, prod / max_prod))
            st.caption(f"{prod:.2f} / {max_prod:.2f} ton/ha ({100*prod/max_prod:.1f}%)")

    # ── TAB 4: KALKULATOR PESTISIDA ───────────────────────────────────────
    with tab4:
        st.markdown("### 🐛 Kalkulator Dosis Pestisida")

        col1, col2 = st.columns(2)
        with col1:
            luas_pest     = st.number_input("📐 Luas Lahan (hektar)", 0.1, 1000.0, 1.0, key="pest_luas")
            jenis_hama    = st.selectbox("🦗 Jenis Hama / Penyakit", [
                "Wereng Coklat", "Penggerek Batang", "Ulat Grayak",
                "Blast (Padi)", "Antraknosa (Cabai)", "Kutu Daun",
                "Blas Daun", "Gulma Umum"
            ], key="pest_hama")
            jenis_pestisida = st.selectbox("🧪 Jenis Pestisida", [
                "Insektisida (cair)", "Fungisida (bubuk)", "Herbisida",
                "Akarisida", "Rodentisida"
            ], key="pest_jenis")

        with col2:
            volume_semprot = st.number_input("🪣 Volume Semprot (L/ha)", 100, 600, 400, 50, key="pest_vol")
            konsentrasi    = st.number_input("💊 Konsentrasi (ml atau g per L air)", 0.5, 10.0, 2.0, 0.5, key="pest_konsen")
            frekuensi      = st.number_input("🔁 Frekuensi Aplikasi (kali/musim)", 1, 10, 3, 1, key="pest_frek")

        total_volume  = luas_pest * volume_semprot
        bahan_aktif   = total_volume * konsentrasi
        total_musim   = bahan_aktif * frekuensi

        harga_pest = {"Insektisida (cair)": 150000, "Fungisida (bubuk)": 120000,
                      "Herbisida": 80000, "Akarisida": 200000, "Rodentisida": 60000}
        harga_p = harga_pest.get(jenis_pestisida, 100000)
        biaya_pest = (total_musim / 1000) * harga_p  # per liter

        if st.button("🐛 Hitung Dosis Pestisida", key="btn_pest"):
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            c1.metric("Volume Air/Aplikasi", f"{total_volume:,.0f} L")
            c2.metric("Bahan Aktif/Aplikasi", f"{bahan_aktif:,.0f} ml/g")
            c3.metric("Total Bahan Aktif/Musim", f"{total_musim:,.0f} ml/g")

            st.warning(f"""
⚠️ **Catatan Keselamatan Penggunaan Pestisida:**
- Gunakan APD lengkap (masker, sarung tangan, kacamata)
- Semprot pada pagi hari (06.00–09.00) atau sore hari (16.00–18.00)
- Hindari semprot saat angin kencang atau hujan
- Rotasi jenis pestisida setiap musim untuk mencegah resistensi
- Estimasi biaya pestisida: **Rp {biaya_pest:,.0f}** per musim
            """)

    # ── TAB 5: ANALISIS ROI ───────────────────────────────────────────────
    with tab5:
        st.markdown("### 💰 Analisis Return on Investment (ROI) Pertanian")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📤 Biaya Produksi**")
            biaya_benih    = st.number_input("🌱 Biaya Benih (Rp)", 0, 100_000_000, 500_000, 50_000, key="roi_benih")
            biaya_pupuk    = st.number_input("🧪 Biaya Pupuk (Rp)", 0, 100_000_000, 1_500_000, 100_000, key="roi_pupuk")
            biaya_pestisid = st.number_input("🐛 Biaya Pestisida (Rp)", 0, 50_000_000, 800_000, 50_000, key="roi_pest")
            biaya_tenaker  = st.number_input("👷 Biaya Tenaga Kerja (Rp)", 0, 100_000_000, 3_000_000, 100_000, key="roi_tk")
            biaya_lain     = st.number_input("📦 Biaya Lain-lain (Rp)", 0, 50_000_000, 500_000, 50_000, key="roi_lain")

        with col2:
            st.markdown("**📥 Pendapatan**")
            hasil_ton      = st.number_input("🌾 Hasil Panen (ton)", 0.1, 1000.0, 5.0, 0.1, key="roi_ton")
            harga_per_kg   = st.number_input("💵 Harga Jual (Rp/kg)", 100, 100_000, 5_500, 100, key="roi_harga")
            subsidi        = st.number_input("🏛️ Subsidi / Bantuan (Rp)", 0, 50_000_000, 0, 100_000, key="roi_subsidi")

        total_biaya    = biaya_benih + biaya_pupuk + biaya_pestisid + biaya_tenaker + biaya_lain
        total_penjualan = hasil_ton * 1000 * harga_per_kg
        total_pendapatan = total_penjualan + subsidi
        keuntungan     = total_pendapatan - total_biaya
        roi_pct        = (keuntungan / total_biaya * 100) if total_biaya > 0 else 0
        bep_kg         = total_biaya / harga_per_kg if harga_per_kg > 0 else 0

        if st.button("💰 Hitung ROI", key="btn_roi"):
            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Biaya", f"Rp {total_biaya:,.0f}")
            c2.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
            c3.metric("Keuntungan Bersih", f"Rp {keuntungan:,.0f}",
                      delta=f"{roi_pct:.1f}% ROI")
            c4.metric("BEP (Break Even)", f"{bep_kg:,.0f} kg")

            if keuntungan > 0:
                st.success(f"✅ **MENGUNTUNGKAN!** ROI = {roi_pct:.1f}% — Setiap Rp 1.000 yang diinvestasikan menghasilkan Rp {1000+roi_pct*10:,.0f}")
            elif keuntungan == 0:
                st.warning("⚖️ **IMPAS** — Pendapatan sama dengan biaya produksi.")
            else:
                st.error(f"❌ **RUGI** — Kerugian sebesar Rp {abs(keuntungan):,.0f}. Pertimbangkan efisiensi biaya.")
