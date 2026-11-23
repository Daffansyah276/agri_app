"""
Halaman Deteksi Hama & Gulma menggunakan YOLOv8 Computer Vision
Mendukung: upload gambar, webcam, dan kamera real-time
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import os
import datetime
import json
import random

# ── Mapping kelas hama & gulma ───────────────────────────────────────────────
# Ketika model custom belum tersedia, kita gunakan COCO atau simulasi
PEST_GULMA_CLASSES = {
    # Hama
    "aphid":            {"label": "Kutu Daun",       "type": "hama",  "severity": "sedang",  "color": (255, 100, 50)},
    "caterpillar":      {"label": "Ulat",             "type": "hama",  "severity": "tinggi",  "color": (255, 50, 50)},
    "whitefly":         {"label": "Kutu Putih",       "type": "hama",  "severity": "sedang",  "color": (255, 150, 50)},
    "leafhopper":       {"label": "Wereng",           "type": "hama",  "severity": "tinggi",  "color": (255, 0, 0)},
    "stem_borer":       {"label": "Penggerek Batang", "type": "hama",  "severity": "kritis",  "color": (200, 0, 0)},
    "spider_mite":      {"label": "Tungau Laba-laba", "type": "hama",  "severity": "sedang",  "color": (255, 100, 0)},
    # Gulma
    "crabgrass":        {"label": "Rumput Liar",      "type": "gulma", "severity": "rendah",  "color": (100, 200, 50)},
    "nutsedge":         {"label": "Teki",             "type": "gulma", "severity": "sedang",  "color": (150, 180, 50)},
    "broadleaf_weed":   {"label": "Gulma Daun Lebar", "type": "gulma", "severity": "sedang",  "color": (100, 180, 100)},
    "water_hyacinth":   {"label": "Eceng Gondok",     "type": "gulma", "severity": "tinggi",  "color": (80, 150, 80)},
    # Penyakit
    "leaf_blast":       {"label": "Blast Daun",       "type": "penyakit", "severity": "kritis","color": (200, 50, 200)},
    "brown_spot":       {"label": "Bercak Coklat",    "type": "penyakit", "severity": "sedang","color": (180, 100, 50)},
    "leaf_curl":        {"label": "Keriting Daun",    "type": "penyakit", "severity": "sedang","color": (220, 80, 150)},
}

REKOMENDASI = {
    "hama": {
        "rendah":  "Lakukan monitoring rutin setiap 3 hari. Gunakan perangkap lekat kuning.",
        "sedang":  "Semprot dengan insektisida nabati (neem oil/ekstrak daun sirih). Dosis 5ml/L.",
        "tinggi":  "Aplikasi insektisida kimia terdaftar. Hubungi penyuluh pertanian.",
        "kritis":  "🚨 TINDAKAN DARURAT! Lakukan eradikasi segera dan isolasi area terinfeksi.",
    },
    "gulma": {
        "rendah":  "Lakukan penyiangan manual. Mulching untuk mencegah pertumbuhan gulma.",
        "sedang":  "Penyiangan mekanis atau herbisida selektif. Rotasi tanaman direkomendasikan.",
        "tinggi":  "Aplikasi herbisida sistemik. Pastikan tidak terkena tanaman utama.",
        "kritis":  "🚨 Gulma dominan! Perlu penanganan intensif dan peninjauan sistem tanam.",
    },
    "penyakit": {
        "rendah":  "Tingkatkan sirkulasi udara. Kurangi kelembaban berlebih di sekitar tanaman.",
        "sedang":  "Semprot fungisida preventif. Buang daun/bagian tanaman yang terinfeksi.",
        "tinggi":  "Fungisida sistemik + sanitasi kebun. Hindari irigasi dari atas.",
        "kritis":  "🚨 Risiko kehilangan panen tinggi! Konsultasi segera dengan ahli patologi tanaman.",
    },
}

SEVERITY_COLOR = {"rendah": "#2d6a4f", "sedang": "#f4a261", "tinggi": "#e63946", "kritis": "#7b1113"}
SEVERITY_EMOJI = {"rendah": "🟢", "sedang": "🟡", "tinggi": "🔴", "kritis": "💀"}


def load_yolo_model(model_path: str):
    """Muat model YOLOv8."""
    try:
        from ultralytics import YOLO
        if os.path.exists(model_path):
            model = YOLO(model_path)
            return model, f"✅ Model dimuat dari: {model_path}"
        else:
            # Gunakan YOLOv8n pretrained sebagai fallback demo
            model = YOLO("yolov8n.pt")
            return model, "⚠️ Model custom tidak ditemukan. Menggunakan YOLOv8n (COCO) untuk demonstrasi."
    except Exception as e:
        return None, f"❌ Gagal memuat model: {str(e)}"


def run_yolo_detection(model, image_array: np.ndarray, conf_threshold: float, iou_threshold: float):
    """Jalankan inferensi YOLOv8 pada gambar."""
    try:
        from ultralytics import YOLO
        results = model(image_array, conf=conf_threshold, iou=iou_threshold, verbose=False)
        return results
    except Exception as e:
        st.error(f"Error deteksi: {e}")
        return None


def draw_detections(image_array: np.ndarray, results, class_mapping: dict, model_names: dict) -> np.ndarray:
    """Gambar bounding box hasil deteksi pada gambar."""
    img = image_array.copy()
    if results is None:
        return img
    for r in results:
        boxes = r.boxes
        if boxes is None:
            continue
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = model_names.get(cls_id, "unknown")

            # Cek apakah termasuk kelas hama/gulma
            info = class_mapping.get(cls_name, None)
            if info:
                color = info["color"]
                label = f"{info['label']} {conf:.0%}"
            else:
                color = (100, 100, 255)
                label = f"{cls_name} {conf:.0%}"

            # Gambar bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            # Label background
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(img, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)
            cv2.putText(img, label, (x1 + 3, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return img


def simulate_detection(image_array: np.ndarray, conf_threshold: float) -> tuple:
    """
    Simulasi deteksi untuk demo ketika model custom tidak tersedia.
    Mengembalikan (gambar_dengan_box, list_deteksi)
    """
    h, w = image_array.shape[:2]
    img  = image_array.copy()
    detections = []

    # Pilih 1-4 deteksi acak
    n_det = random.randint(1, 4)
    kelas_list = random.sample(list(PEST_GULMA_CLASSES.keys()), min(n_det, len(PEST_GULMA_CLASSES)))

    for cls_name in kelas_list:
        info  = PEST_GULMA_CLASSES[cls_name]
        conf  = random.uniform(conf_threshold, min(conf_threshold + 0.35, 0.99))
        # Buat bounding box acak (25–65% gambar)
        bw = random.randint(w // 6, w // 3)
        bh = random.randint(h // 6, h // 3)
        x1 = random.randint(0, w - bw)
        y1 = random.randint(0, h - bh)
        x2, y2 = x1 + bw, y1 + bh

        color = info["color"]
        label = f"{info['label']} {conf:.0%}"

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(img, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)
        cv2.putText(img, label, (x1 + 3, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        detections.append({
            "kelas": cls_name,
            "label": info["label"],
            "tipe":  info["type"],
            "severity": info["severity"],
            "confidence": conf,
            "bbox": [x1, y1, x2, y2],
        })

    return img, detections


def parse_real_detections(results, model_names: dict) -> list:
    """Parse hasil YOLO nyata menjadi list deteksi terstruktur."""
    detections = []
    if results is None:
        return detections
    for r in results:
        if r.boxes is None:
            continue
        for box in r.boxes:
            cls_id   = int(box.cls[0])
            cls_name = model_names.get(cls_id, "unknown")
            conf     = float(box.conf[0])
            bbox     = list(map(int, box.xyxy[0].tolist()))
            info     = PEST_GULMA_CLASSES.get(cls_name, {
                "label": cls_name, "type": "lainnya", "severity": "rendah", "color": (100, 100, 255)
            })
            detections.append({
                "kelas": cls_name, "label": info["label"],
                "tipe": info["type"], "severity": info["severity"],
                "confidence": conf, "bbox": bbox,
            })
    return detections


# ─────────────────────────────────────────────────────────────────────────────
def show():
    st.markdown("## 🔍 Deteksi Hama & Gulma — Computer Vision AI (YOLOv8)")
    st.markdown("Upload foto tanaman untuk mendeteksi hama, gulma, dan penyakit secara otomatis menggunakan YOLOv8.")
    st.markdown("---")

    # ── Pengaturan Model ──────────────────────────────────────────────────
    with st.expander("⚙️ Pengaturan Model YOLOv8", expanded=False):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            model_path = st.text_input(
                "📂 Path Model Custom (.pt)",
                value="models/hama_gulma_yolov8.pt",
                help="Masukkan path ke file model YOLOv8 yang sudah dilatih khusus untuk hama & gulma.",
                key="det_model_path"
            )
            use_demo = st.checkbox("🎭 Mode Demo (simulasi deteksi)", value=True, key="det_demo",
                                   help="Aktifkan untuk melihat demo tanpa model custom.")
        with col_m2:
            conf_threshold = st.slider("📊 Confidence Threshold", 0.1, 0.95, 0.40, 0.05, key="det_conf",
                                       help="Minimum kepercayaan prediksi. Nilai lebih tinggi = deteksi lebih ketat.")
            iou_threshold  = st.slider("🔀 IoU Threshold (NMS)", 0.1, 0.9, 0.45, 0.05, key="det_iou",
                                       help="Non-Maximum Suppression. Mengontrol overlap bounding box.")
            img_size       = st.select_slider("📐 Ukuran Input", [320, 416, 512, 640, 800], value=640, key="det_size")

    # ── Mode Input ────────────────────────────────────────────────────────
    input_mode = st.radio("📸 Sumber Gambar", [
        "📁 Upload Gambar", "📷 Kamera Langsung", "🌐 URL Gambar"
    ], horizontal=True, key="det_input_mode")

    image_to_detect = None
    img_array       = None

    if input_mode == "📁 Upload Gambar":
        uploaded = st.file_uploader(
            "Pilih gambar tanaman (JPG/PNG/JPEG)",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            key="det_upload"
        )
        if uploaded:
            image_to_detect = Image.open(uploaded).convert("RGB")
            st.image(image_to_detect, caption="Gambar yang Diunggah", use_column_width=True)
            img_array = np.array(image_to_detect)

    elif input_mode == "📷 Kamera Langsung":
        cam_img = st.camera_input("📷 Ambil Foto Tanaman", key="det_cam")
        if cam_img:
            image_to_detect = Image.open(cam_img).convert("RGB")
            img_array = np.array(image_to_detect)
            st.image(image_to_detect, caption="Foto dari Kamera", use_column_width=True)

    elif input_mode == "🌐 URL Gambar":
        url = st.text_input("Masukkan URL gambar tanaman:", key="det_url",
                            placeholder="https://example.com/tanaman.jpg")
        if url:
            try:
                import urllib.request
                with urllib.request.urlopen(url) as response:
                    img_data = response.read()
                image_to_detect = Image.open(io.BytesIO(img_data)).convert("RGB")
                img_array = np.array(image_to_detect)
                st.image(image_to_detect, caption="Gambar dari URL", use_column_width=True)
            except Exception as e:
                st.error(f"Gagal memuat gambar dari URL: {e}")

    # ── Tombol Deteksi ────────────────────────────────────────────────────
    if img_array is not None:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            run_detection = st.button("🔍 Jalankan Deteksi AI", type="primary", key="btn_deteksi")
        with col_btn2:
            st.caption(f"Gambar: {img_array.shape[1]}×{img_array.shape[0]} px | "
                       f"Conf: {conf_threshold} | Mode: {'Demo' if use_demo else 'Real Model'}")

        if run_detection:
            with st.spinner("🤖 YOLOv8 sedang menganalisis gambar..."):
                detections = []
                result_img = img_array.copy()

                if use_demo:
                    # ── Mode Demo ──────────────────────────────────────
                    result_img, detections = simulate_detection(img_array, conf_threshold)
                    st.info("🎭 **Mode Demo Aktif** — Deteksi adalah simulasi untuk tujuan demonstrasi. "
                            "Latih model custom dan nonaktifkan mode demo untuk hasil nyata.")
                else:
                    # ── Mode Model Nyata ───────────────────────────────
                    model, model_msg = load_yolo_model(model_path)
                    st.caption(model_msg)
                    if model:
                        results = run_yolo_detection(model, img_array, conf_threshold, iou_threshold)
                        result_img = draw_detections(img_array, results,
                                                     PEST_GULMA_CLASSES, model.names)
                        detections = parse_real_detections(results, model.names)

            # ── Tampilkan Hasil ───────────────────────────────────────
            st.markdown("### 📊 Hasil Deteksi")
            col_res1, col_res2 = st.columns([2, 1])

            with col_res1:
                st.image(result_img, caption="Hasil Deteksi YOLOv8", use_column_width=True,
                         channels="RGB")

                # Tombol unduh gambar hasil
                result_pil = Image.fromarray(result_img)
                buf = io.BytesIO()
                result_pil.save(buf, format="PNG")
                st.download_button(
                    "⬇️ Unduh Gambar Hasil",
                    data=buf.getvalue(),
                    file_name=f"deteksi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    key="btn_download_img"
                )

            with col_res2:
                st.markdown(f"**Total Objek Terdeteksi: `{len(detections)}`**")
                if detections:
                    # Hitung per tipe
                    n_hama     = sum(1 for d in detections if d["tipe"] == "hama")
                    n_gulma    = sum(1 for d in detections if d["tipe"] == "gulma")
                    n_penyakit = sum(1 for d in detections if d["tipe"] == "penyakit")
                    n_lain     = len(detections) - n_hama - n_gulma - n_penyakit

                    st.metric("🦗 Hama", n_hama)
                    st.metric("🌿 Gulma", n_gulma)
                    st.metric("🦠 Penyakit", n_penyakit)
                    if n_lain: st.metric("🔵 Lainnya", n_lain)
                else:
                    st.success("✅ Tidak ada hama/gulma yang terdeteksi pada gambar ini.")

            # ── Detail Setiap Deteksi ─────────────────────────────────
            if detections:
                st.markdown("---")
                st.markdown("### 🔬 Detail Deteksi & Rekomendasi Penanganan")

                for i, det in enumerate(detections):
                    sev   = det.get("severity", "rendah")
                    tipe  = det.get("tipe", "lainnya")
                    color = SEVERITY_COLOR.get(sev, "#666")
                    emoji = SEVERITY_EMOJI.get(sev, "⚪")
                    rek   = REKOMENDASI.get(tipe, {}).get(sev, "Konsultasikan dengan ahli pertanian setempat.")

                    with st.expander(f"{emoji} [{i+1}] {det['label']} — Tingkat: **{sev.upper()}** | Kepercayaan: {det['confidence']:.1%}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"""
| Atribut | Nilai |
|---------|-------|
| **Jenis** | {det['label']} |
| **Tipe** | {tipe.capitalize()} |
| **Tingkat Keparahan** | {emoji} {sev.capitalize()} |
| **Confidence Score** | {det['confidence']:.4f} ({det['confidence']:.1%}) |
| **Lokasi (Bounding Box)** | {det['bbox']} |
                            """)
                        with c2:
                            st.markdown(f"""
**💊 Rekomendasi Tindakan:**

{rek}

---
**🗓️ Jadwal Pemantauan Lanjutan:**
- Periksa kembali dalam **{"24 jam" if sev == "kritis" else "3 hari" if sev == "tinggi" else "1 minggu"}**
- Dokumentasikan perkembangan serangan
- Catat curah hujan & suhu saat deteksi
                            """)

                # ── Ekspor Laporan ────────────────────────────────────
                st.markdown("---")
                st.markdown("### 📄 Ekspor Laporan Deteksi")

                report = {
                    "tanggal": datetime.datetime.now().isoformat(),
                    "total_deteksi": len(detections),
                    "detail": detections,
                    "conf_threshold": conf_threshold,
                    "mode": "demo" if use_demo else "real_model",
                }
                report_json = json.dumps(report, indent=2, ensure_ascii=False)

                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    st.download_button(
                        "📥 Unduh Laporan JSON",
                        data=report_json,
                        file_name=f"laporan_deteksi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        key="btn_download_json"
                    )
                with col_exp2:
                    # Buat laporan teks
                    lines = [f"=== LAPORAN DETEKSI HAMA & GULMA ==="]
                    lines.append(f"Tanggal: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                    lines.append(f"Total Deteksi: {len(detections)}")
                    lines.append("")
                    for i, det in enumerate(detections):
                        lines.append(f"[{i+1}] {det['label']} ({det['tipe']})")
                        lines.append(f"    Keparahan: {det['severity']}")
                        lines.append(f"    Confidence: {det['confidence']:.4f}")
                        lines.append(f"    Lokasi: {det['bbox']}")
                        sev  = det.get("severity", "rendah")
                        tipe = det.get("tipe", "lainnya")
                        rek  = REKOMENDASI.get(tipe, {}).get(sev, "Konsultasikan ahli.")
                        lines.append(f"    Rekomendasi: {rek}")
                        lines.append("")
                    report_txt = "\n".join(lines)
                    st.download_button(
                        "📥 Unduh Laporan TXT",
                        data=report_txt,
                        file_name=f"laporan_deteksi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="btn_download_txt"
                    )

    # ── Panduan Penggunaan ────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("📖 Panduan Penggunaan & Melatih Model Custom"):
        st.markdown("""
### 🎯 Cara Menggunakan Mode Demo
1. Aktifkan **Mode Demo** di pengaturan
2. Upload/ambil foto tanaman
3. Klik **Jalankan Deteksi AI**
4. Lihat hasil simulasi deteksi dengan bounding box

### 🤖 Cara Melatih Model Custom YOLOv8
```bash
# 1. Siapkan dataset dengan labelme atau Roboflow
# 2. Ekspor dalam format YOLO

# 3. Latih model
pip install ultralytics
yolo train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640

# 4. Validasi model
yolo val model=runs/detect/train/weights/best.pt data=dataset.yaml

# 5. Prediksi
yolo predict model=best.pt source=gambar_tanaman.jpg
```

### 📂 Format Dataset yang Didukung
- **YOLO v8 format**: `images/` + `labels/` + `data.yaml`
- **Roboflow export**: YOLO v8
- **LabelImg**: YOLO format

### 🏷️ Kelas yang Disarankan untuk Dataset
| ID | Kelas | Deskripsi |
|----|-------|-----------|
| 0 | aphid | Kutu daun |
| 1 | caterpillar | Ulat grayak |
| 2 | whitefly | Kutu putih |
| 3 | leafhopper | Wereng |
| 4 | stem_borer | Penggerek batang |
| 5 | crabgrass | Rumput liar |
| 6 | nutsedge | Teki |
| 7 | broadleaf_weed | Gulma daun lebar |
| 8 | leaf_blast | Blast daun |
| 9 | brown_spot | Bercak coklat |

### 🌐 Sumber Dataset Publik
- [Roboflow Universe - Plant Disease](https://roboflow.com/datasets/plant-disease)
- [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset)
- [iNaturalist - Insects](https://www.inaturalist.org/)
        """)
