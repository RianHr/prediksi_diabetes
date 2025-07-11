import sqlite3

def get_connection():
    conn = sqlite3.connect('/tmp/diabetes_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Buat tabel pengguna
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pengguna (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_lengkap TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                tanggal_daftar DATETIME NOT NULL
            )
        """)
        # Buat tabel predictions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                jumlah_kehamilan INTEGER,
                glukosa INTEGER,
                tekanan_darah INTEGER,
                ketebalan_kulit INTEGER,
                insulin INTEGER,
                bmi REAL,
                riwayat_keluarga REAL,
                usia INTEGER,
                prediksi TEXT,
                probabilitas REAL,
                faktor_1 TEXT,
                faktor_2 TEXT,
                faktor_3 TEXT,
                tanggal DATETIME
            )
        """)
        conn.commit()
        print("Tabel pengguna dan predictions berhasil dibuat.")
    except sqlite3.Error as e:
        print(f"Error saat membuat tabel: {e}")
    finally:
        cursor.close()
        conn.close()