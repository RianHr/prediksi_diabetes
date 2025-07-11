import sqlite3

def get_connection():
    conn = sqlite3.connect("data/prediksi_diabetes.db")
    conn.row_factory = sqlite3.Row  # agar hasil fetch berupa dictionary
    return conn
