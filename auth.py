# auth.py
from db_config import get_connection
from datetime import datetime
import bcrypt

def register_user(nama, username, password, role='user'):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Validasi input
        if not all([nama, username, password]):
            return False, "❌ Semua field wajib diisi."
        if len(username) < 3 or len(password) < 6:
            return False, "❌ Username minimal 3 karakter, password minimal 6 karakter."

        # Cek apakah username sudah ada
        cursor.execute("SELECT * FROM pengguna WHERE username = ?", (username,))
        if cursor.fetchone():
            return False, "❌ Username sudah digunakan."

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Simpan ke DB
        cursor.execute("""
            INSERT INTO pengguna (nama_lengkap, username, password, role, tanggal_daftar)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, username, hashed_password, role, datetime.now().isoformat()))
        conn.commit()
        return True, "✅ Registrasi berhasil!"
    except Exception as e:
        return False, f"❌ Error saat registrasi: {str(e)}"
    finally:
        conn.close()


def login_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pengguna WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            stored_hash = user[3]  # kolom password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return True, {
                    'id': user[0],
                    'nama_lengkap': user[1],
                    'username': user[2],
                    'role': user[4],
                    'tanggal_daftar': user[5]
                }
        return False, "❌ Username atau password salah."
    except Exception as e:
        return False, f"❌ Error saat login: {str(e)}"
    finally:
        conn.close()
