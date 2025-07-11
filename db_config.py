# db_config.py
import sqlite3
import os

def get_connection():
    # Pastikan folder "data/" ada, jika belum maka buat
    os.makedirs("data", exist_ok=True)

    # Buat atau buka database SQLite
    conn = sqlite3.connect("data/prediksi_diabetes.db", check_same_thread=False)
    return conn
