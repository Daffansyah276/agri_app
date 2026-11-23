# 🌾 AgriFarm Pro

**Aplikasi Manajemen Pertanian Cerdas** berbasis AI — Kalkulator, Monitoring, dan Deteksi Hama menggunakan YOLOv8.

---

## 🚀 Cara Menjalankan

### Opsi 1 — Double-click (Windows)
Klik ganda file `jalankan_app.bat`

### Opsi 2 — Command Prompt / PowerShell
```bash
cd "c:\Semester 5\New folder\agri_app"
streamlit run app.py
```

Lalu buka browser ke: **http://localhost:8501**

---

## 📦 Instalasi Dependensi
```bash
pip install -r requirements.txt
```

---

## 🗂️ Struktur Proyek
```
agri_app/
├── app.py                  ← Halaman utama & navigasi
├── jalankan_app.bat        ← Launcher Windows
├── requirements.txt        ← Daftar dependensi
├── pages/
│   ├── kalkulator.py       ← 🧮 Kalkulator Pertanian
│   ├── monitoring.py       ← 🌡️ Pemantauan Suhu & O₂
│   └── deteksi_ai.py       ← 🔍 Deteksi Hama (YOLOv8)
└── models/
    └── README.md           ← Panduan model custom
```

---

## ✨ Fitur Lengkap

### 🧮 Kalkulator Pertanian
| Kalkulator | Fungsi |
|-----------|--------|
| Pupuk | Dosis NPK/Urea/SP-36/KCl per fase & luas lahan |
| Irigasi | Kebutuhan air via Penman-Monteith sederhana |
| Hasil Panen | Estimasi produktivitas & pendapatan |
| Pestisida | Dosis & biaya pestisida per musim |
| ROI | Analisis laba-rugi & Break Even Point |

### 🌡️ Pemantauan Lingkungan
- Gauge chart real-time: Suhu, Kelembaban, O₂, CO₂
- Grafik historis 60 titik terakhir (Plotly)
- Alert otomatis jika nilai keluar batas optimal
- Referensi rentang optimal 4 parameter sensor

### 🔍 Deteksi Hama & Gulma (YOLOv8)
- Upload gambar / kamera langsung / URL
- Bounding box + label confidence tiap deteksi
- Rekomendasi penanganan per tipe & tingkat keparahan
- Ekspor laporan JSON & TXT
- Mode Demo tanpa model custom
- Panduan pelatihan model custom

---

## 🤖 Melatih Model Custom YOLOv8

```bash
# 1. Siapkan dataset dengan Roboflow / LabelImg
# 2. Latih model
yolo train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640

# 3. Salin model ke folder models/
copy runs\detect\train\weights\best.pt models\hama_gulma_yolov8.pt
```

Kelas yang direkomendasikan: `aphid`, `caterpillar`, `whitefly`, `leafhopper`, `stem_borer`, `crabgrass`, `nutsedge`, `broadleaf_weed`, `leaf_blast`, `brown_spot`

---

## 🛠️ Teknologi
- **Frontend**: Streamlit 1.67
- **CV/AI**: YOLOv8 (Ultralytics)
- **Grafik**: Plotly
- **Pemrosesan Gambar**: OpenCV + Pillow
- **Data**: Pandas + NumPy
