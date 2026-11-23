@echo off
echo ========================================
echo     🌾  AgriFarm Pro - Memulai App...
echo ========================================
echo.
cd /d "%~dp0"
echo Menjalankan aplikasi di http://localhost:8501
echo Tekan Ctrl+C untuk menghentikan.
echo.
python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
pause
