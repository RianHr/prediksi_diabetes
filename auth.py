from db_config import get_connection
from datetime import datetime
import bcrypt

def register_user(nama, username, password, role='user'):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Validasi input dasar
        if not all([nama, username, password]):
            return False, "❌ Semua field (nama, username, password) wajib diisi."
        if len(username) < 3 or len(password) < 6:
            return False, "❌ Username minimal 3 karakter, password minimal 6 karakter."

        # Cek apakah username sudah ada
        cursor.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "❌ Username sudah digunakan."

        # Hash password sebelum menyimpan
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Simpan user baru ke database
        cursor.execute("""
            INSERT INTO pengguna (nama_lengkap, username, password, role, tanggal_daftar)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama, username, hashed_password, role, datetime.now()))
        conn.commit()
        return True, "✅ Registrasi berhasil!"
    except Exception as e:
        return False, f"❌ Terjadi kesalahan saat registrasi: {str(e)}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def login_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if not username or not password:
            return False, "❌ Username dan password wajib diisi."

        cursor.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return True, user
        else:
            return False, "❌ Username atau password salah."
    except Exception as e:
        return False, f"❌ Terjadi kesalahan saat login: {str(e)}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Contoh penggunaan untuk registrasi admin (opsional di main.py)
# register_user("Admin Utama", "admin", "admin123", role='admin')