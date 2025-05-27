import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib

def show_user_dashboard(model, scaler):
    st.title("🧠 Prediksi Diabetes Tipe 2")
    st.markdown("Selamat datang di dashboard prediksi diabetes.")

    menu = st.sidebar.radio("📂 Menu Navigasi", [
        "🧪 Prediksi Data Baru",
        "📁 Riwayat Prediksi",
        "📈 Ringkasan Statistik",
        "📊 Visualisasi Model",
        "🚪 Logout"
    ])

    if menu == "🧪 Prediksi Data Baru":
        tampilkan_form_prediksi(model, scaler)
    elif menu == "📁 Riwayat Prediksi":
        tampilkan_riwayat_prediksi()
    elif menu == "📈 Ringkasan Statistik":
        tampilkan_ringkasan_statistik()
    elif menu == "📊 Visualisasi Model":
        tampilkan_visualisasi()
    elif menu == "🚪 Logout":
        st.session_state.status_login = False
        st.session_state.nama = ""
        st.session_state.role = ""
        st.success("Berhasil logout.")
        st.rerun()

def tampilkan_form_prediksi(model, scaler):
    st.header("🧪 Prediksi Diabetes")
    fitur = [
        "Jumlah_Kehamilan", "Glukosa", "Tekanan_Darah", "Ketebalan_Kulit",
        "Insulin", "BMI", "Riwayat_Keluarga", "Usia"
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

        # Simpan hasil ke CSV
        hasil_df = pd.DataFrame([{
            "Jumlah_Kehamilan": kehamilan,
            "Glukosa": glukosa,
            "Tekanan_Darah": tekanan,
            "Ketebalan_Kulit": kulit,
            "Insulin": insulin,
            "BMI": bmi,
            "Riwayat_Keluarga": riwayat,
            "Usia": usia,
            "Prediksi": hasil,
            "Probabilitas": prob
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

def tampilkan_ringkasan_statistik():
    st.header("📈 Ringkasan Statistik")
    path = "hasil/hasil_prediksi.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        total = len(df)
        positif = df["Prediksi"].str.contains("Positif").sum()
        negatif = total - positif
        st.write(f"Total Prediksi: **{total}**")
        st.write(f"Positif Diabetes: **{positif}**")
        st.write(f"Negatif Diabetes: **{negatif}**")
    else:
        st.warning("Belum ada data untuk dianalisis.")

def tampilkan_visualisasi():
    st.header("📊 Visualisasi Model")
    folder = "visualisasi"
    gambar = {
        "Matriks Konfusi": "confusion_matrix.png",
        "ROC Curve": "roc_curve.png",
        "Pentingnya Fitur": "feature_importance.png",
        "Distribusi Kelas": "distribusi_kelas.png",
        "Korelasi Fitur": "korelasi.png"
    }
    for judul, file in gambar.items():
        path = os.path.join(folder, file)
        if os.path.exists(path):
            st.subheader(judul)
            st.image(path, use_container_width=True)
        else:
            st.warning(f"Gambar `{file}` tidak ditemukan.")
