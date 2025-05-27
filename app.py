import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from auth import login_user
from user_dashboard import show_user_dashboard
from admin_dashboard import show_admin_dashboard

model = joblib.load("model/model_diabetes.pkl")
scaler = joblib.load("model/scaler_diabetes.pkl")

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi Diabetes", layout="wide")

# Inisialisasi session state
if "status_login" not in st.session_state:
    st.session_state.status_login = False
    st.session_state.nama = ""
    st.session_state.role = ""
    st.session_state.halaman = "login"

# Fungsi login
def halaman_login():
    st.subheader("🔐 Login")

    username = st.text_input("Nama pengguna")
    password = st.text_input("Kata sandi", type="password")

    if st.button("Login"):
        berhasil, hasil = login_user(username, password)
        if berhasil:
            st.session_state.status_login = True
            st.session_state.nama = hasil["nama_lengkap"]
            st.session_state.role = hasil["role"]
            st.session_state.halaman = "dashboard"
            st.rerun()
        else:
            st.error(hasil)

# Fungsi logout
def tombol_logout():
    if st.sidebar.button("Logout"):
        st.session_state.status_login = False
        st.session_state.nama = ""
        st.session_state.role = ""
        st.session_state.halaman = "login"
        st.rerun()

# Tampilan untuk user login
if st.session_state.status_login:
    st.sidebar.markdown(f"👤 Anda login sebagai: **{st.session_state.nama}**")
    tombol_logout()
    
    if st.session_state.role == "admin":
        show_admin_dashboard()
    else:
        show_user_dashboard(model, scaler)

# Tampilan awal sebelum login
else:
    menu = st.sidebar.selectbox("Menu", ["Login", "Registrasi"])
    if menu == "Login":
        halaman_login()
    else:
        from auth import register_user

        def halaman_registrasi():
            st.subheader("📝 Registrasi Pengguna Baru")
            with st.form("register_form"):
                nama = st.text_input("Nama Lengkap")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                konfirmasi = st.text_input("Konfirmasi Password", type="password")
                daftar = st.form_submit_button("Daftar")

            if daftar:
                if password != konfirmasi:
                    st.warning("Password tidak cocok")
                elif not nama or not username or not password:
                    st.warning("Semua field wajib diisi")
                else:
                    berhasil, pesan = register_user(nama, username, password)
                    if berhasil:
                        st.success(pesan)
                        st.session_state.halaman = "login"
                        st.rerun()
                    else:
                        st.error(pesan)

        halaman_registrasi()
