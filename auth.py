from db_config import get_connection
from datetime import datetime

def register_user(nama, username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Cek apakah username sudah ada
        cursor.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "❌ Username sudah digunakan."

        # Simpan user baru ke database
        cursor.execute("""
            INSERT INTO pengguna (nama_lengkap, username, password, role, tanggal_daftar)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama, username, password, 'user', datetime.now()))
        conn.commit()
        return True, "✅ Registrasi berhasil!"
    except Exception as e:
        return False, f"❌ Terjadi kesalahan saat registrasi: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def login_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM pengguna WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return True, user
        else:
            return False, "Username atau password salah."
    except Exception as e:
        return False, f"Terjadi kesalahan saat login: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
