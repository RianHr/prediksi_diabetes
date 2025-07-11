import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
from db_config import get_connection
from auth import login_user, register_user
from datetime import datetime
import time

# Load model dan scaler
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
    st.session_state.show_login_popup = False
    st.session_state.show_logout_popup = False
    st.session_state.show_register_success = False
    st.session_state.register_time = 0
    st.session_state.form_data = {"nama": "", "username": "", "password": "", "konfirmasi": ""}
    st.session_state.register_message = ""

# Fungsi login
def halaman_login():
    st.subheader("🔐 Login")
    username = st.text_input("Nama Pengguna")
    password = st.text_input("Kata Sandi", type="password")
    if st.button("Masuk"):
        berhasil, hasil = login_user(username, password)
        if berhasil:
            st.session_state.status_login = True
            st.session_state.nama = hasil["nama_lengkap"]
            st.session_state.role = hasil["role"]
            st.session_state.show_login_popup = True
            st.rerun()
        else:
            st.error(hasil)
    
    if st.session_state.show_login_popup:
        st.success(f"✅ Login berhasil! Selamat datang, {st.session_state.nama}!")
        st.session_state.show_login_popup = False

# Fungsi registrasi
def halaman_registrasi():
    st.subheader("📝 Registrasi")
    with st.form("form_registrasi"):
        nama = st.text_input("Nama Lengkap", value=st.session_state.form_data["nama"])
        username = st.text_input("Nama Pengguna", value=st.session_state.form_data["username"])
        password = st.text_input("Kata Sandi", type="password", value=st.session_state.form_data["password"])
        konfirmasi = st.text_input("Konfirmasi Kata Sandi", type="password", value=st.session_state.form_data["konfirmasi"])
        submit = st.form_submit_button("Daftar")

        if submit:
            if password != konfirmasi:
                st.warning("Kata Sandi tidak cocok")
            elif not nama or not username or not password:
                st.warning("Semua kolom wajib diisi")
            else:
                berhasil, pesan = register_user(nama, username, password)
                if berhasil:
                    st.session_state.show_register_success = True
                    st.session_state.register_time = time.time()
                    st.session_state.register_message = pesan
                    st.session_state.form_data = {"nama": "", "username": "", "password": "", "konfirmasi": ""}
                else:
                    st.error(pesan)

    if st.session_state.show_register_success:
        current_time = time.time()
        if current_time - st.session_state.register_time < 3:
            st.success(f"✅ {st.session_state.register_message}")
        else:
            st.session_state.show_register_success = False
            st.session_state.halaman = "login"
            st.rerun()

# Fungsi logout
def tombol_logout():
    if st.sidebar.button("Keluar", key="sidebar_logout_button"):
        st.session_state.status_login = False
        st.session_state.nama = ""
        st.session_state.role = ""
        st.session_state.halaman = "login"
        st.experimental_rerun()

# Fungsi dashboard user
def show_user_dashboard():
    st.title("🧠 Prediksi Diabetes dengan Regresi Logistik")
    st.markdown(f"Selamat datang di dashboard prediksi diabetes, {st.session_state.nama}!")

    menu = st.sidebar.radio("📂 Menu Navigasi", [
        "🧪 Prediksi Diabetes untuk Data Baru",
        "📊 Lihat Evaluasi Model",
        "📈 Informasi Dataset",
        "📁 Riwayat Prediksi"
    ])

    if menu == "🧪 Prediksi Diabetes untuk Data Baru":
        tampilkan_form_prediksi()
    elif menu == "📊 Lihat Evaluasi Model":
        tampilkan_evaluasi_model()
    elif menu == "📈 Informasi Dataset":
        tampilkan_informasi_dataset()
    elif menu == "📁 Riwayat Prediksi":
        tampilkan_riwayat_prediksi()

# Fungsi prediksi
def tampilkan_form_prediksi():
    st.header("🧪 Prediksi Diabetes")
    fitur = [
        "Jumlah Kehamilan", "Glukosa", "Tekanan Darah",
        "Ketebalan Kulit", "Insulin", "BMI", "Riwayat Keluarga", "Usia"
    ]

    with st.form("form_prediksi"):
        col1, col2 = st.columns(2)
        with col1:
            kehamilan = st.number_input("Jumlah Kehamilan", 0, 20, 1)
            glukosa = st.number_input("Kadar Glukosa", 0, 300, 120)
            tekanan = st.number_input("Tekanan Darah", 0, 200, 70)
            kulit = st.number_input("Ketebalan Kulit", 0, 100, 20)
        with col2:
            insulin = st.number_input("Insulin", 0, 900, 79)
            bmi = st.number_input("BMI", 0.0, 70.0, 28.5)
            riwayat = st.number_input("Riwayat Keluarga", 0.0, 2.5, 0.5)
            usia = st.number_input("Usia", 1, 120, 30)
        submit = st.form_submit_button("🔍 Prediksi")

    if submit:
        data = np.array([[kehamilan, glukosa, tekanan, kulit, insulin, bmi, riwayat, usia]])
        data_scaled = scaler.transform(data)
        pred = model.predict(data_scaled)[0]
        prob = model.predict_proba(data_scaled)[0][1]
        hasil = "🟥 Positif Diabetes" if pred == 1 else "🟩 Negatif Diabetes"

        st.subheader("📋 Hasil Prediksi:")
        st.write(f"**Status:** {hasil}")
        st.write(f"**Probabilitas:** {prob:.2%}")

        if pred == 1:
            if prob > 0.75:
                st.error("⚠️ Risiko sangat tinggi! Segera konsultasikan dengan dokter.")
            else:
                st.warning("⚠️ Terdeteksi risiko diabetes. Disarankan cek medis.")
        else:
            if prob > 0.4:
                st.warning("⚠️ Meskipun negatif, risiko cukup mendekati ambang batas.")
            else:
                st.success("✅ Risiko rendah. Pertahankan gaya hidup sehat!")

        st.markdown("### 🧠 Faktor Terkuat yang Mempengaruhi Prediksi")
        koef = model.coef_[0]
        dampak = [(fitur[i], data_scaled[0][i] * koef[i]) for i in range(len(fitur))]
        dampak = sorted(dampak, key=lambda x: abs(x[1]), reverse=True)
        top_features = []
        for i, (ftr, skor) in enumerate(dampak[:3]):
            arah = "meningkatkan" if skor > 0 else "menurunkan"
            st.write(f"{i+1}. **{ftr}**: {arah} risiko diabetes (kontribusi: `{skor:.4f}`)")
            top_features.append(ftr)

        hasil_df = pd.DataFrame([{
            "Jumlah Kehamilan": kehamilan,
            "Glukosa": glukosa,
            "Tekanan Darah": tekanan,
            "Ketebalan Kulit": kulit,
            "Insulin": insulin,
            "BMI": bmi,
            "Riwayat Keluarga": riwayat,
            "Usia": usia,
            "Prediksi": hasil,
            "Probabilitas": prob,
            "Faktor Terkuat 1": top_features[0],
            "Faktor Terkuat 2": top_features[1],
            "Faktor Terkuat 3": top_features[2]
        }])

        os.makedirs("hasil", exist_ok=True)
        file_path = "hasil/hasil_prediksi.csv"
        if os.path.exists(file_path):
            hasil_df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            hasil_df.to_csv(file_path, index=False)
        st.success("✅ Hasil disimpan ke file CSV.")

def tampilkan_riwayat_prediksi():
    st.header("📁 Riwayat Prediksi")
    path = "hasil/hasil_prediksi.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        st.dataframe(df.tail(10).reset_index(drop=True))
    else:
        st.info("Belum ada data prediksi yang tersimpan.")

def tampilkan_evaluasi_model():
    st.header("📊 Lihat Evaluasi Model")
    if os.path.exists("hasil/laporan_evaluasi.txt"):
        with open("hasil/laporan_evaluasi.txt", "r") as file:
            st.text(file.read())
    else:
        st.warning("Belum ada laporan evaluasi yang tersimpan.")

def tampilkan_informasi_dataset():
    st.header("📈 Informasi Dataset")
    st.subheader("Kumulasi Data Statistik:")
    if os.path.exists("data/diabetes.csv"):
        df = pd.read_csv("data/diabetes.csv")
        st.dataframe(df.describe())
        st.subheader("Distribusi Kelas:")
        st.write(df["Outcome"].value_counts())
    else:
        st.error("File dataset 'diabetes.csv' tidak ditemukan.")

# Fungsi dashboard admin
def show_admin_dashboard():
    st.title("👑 Dashboard Admin")
    st.subheader("📋 Daftar Pengguna Terdaftar")

    search_query = st.text_input("🔍 Cari Pengguna (Nama atau Nama Pengguna)")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if search_query:
            cursor.execute("""
                SELECT nama_lengkap, username, role, tanggal_daftar
                FROM pengguna
                WHERE nama_lengkap LIKE ? OR username LIKE ?
                ORDER BY tanggal_daftar DESC
            """, (f"%{search_query}%", f"%{search_query}%"))
        else:
            cursor.execute("""
                SELECT nama_lengkap, username, role, tanggal_daftar
                FROM pengguna
                ORDER BY tanggal_daftar DESC
            """)
        users = cursor.fetchall()
    except Exception as e:
        st.error(f"❌ Gagal memuat data pengguna: {e}")
        users = []

    if users:
        st.subheader("📋 Daftar Pengguna")
        for user in users:
            with st.expander(f"👤 {user['nama_lengkap']}"):
                st.write(f"**🧾 Nama Pengguna:** `{user['username']}`")
                st.write(f"**🔑 Peran:** `{user['role']}`")
                st.write(f"**🕒 Terdaftar:** {user['tanggal_daftar']}")
    else:
        st.info("Belum ada pengguna terdaftar atau tidak ditemukan.")

# TAMPILAN UTAMA
if __name__ == "__main__":
    if st.session_state.status_login:
        st.sidebar.markdown(f"👤 Login sebagai: **{st.session_state.nama}**")
        tombol_logout()
        if st.session_state.role == "admin":
            show_admin_dashboard()
        else:
            show_user_dashboard()
    else:
        st.sidebar.title("🔐 Autentikasi")
        menu = st.sidebar.radio("Menu", ["Login", "Registrasi"])
        if menu == "Login":
            halaman_login()
        else:
            halaman_registrasi()
