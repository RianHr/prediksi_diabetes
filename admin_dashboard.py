import streamlit as st
from db_config import get_connection

def show_admin_dashboard():
    st.title("👑 Dashboard Admin")
    st.subheader("📋 Daftar Pengguna Terdaftar")

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nama_lengkap, username, role, tanggal_daftar FROM pengguna ORDER BY tanggal_daftar DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        if users:
            for user in users:
                st.markdown(f"""
                **👤 Nama:** {user['nama_lengkap']}  
                **🧾 Username:** `{user['username']}`  
                **🔑 Role:** `{user['role']}`  
                **🕒 Terdaftar:** {user['tanggal_daftar']}  
                ---
                """)
        else:
            st.info("Belum ada pengguna terdaftar.")
    except Exception as e:
        st.error(f"❌ Gagal memuat data pengguna: {e}")
