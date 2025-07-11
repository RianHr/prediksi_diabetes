# 📊 Prediksi Diabetes Menggunakan Regresi Logistik

## 🎯 Tujuan Proyek

1. Membangun model prediksi diabetes berdasarkan data medis menggunakan algoritma Regresi Logistik.
2. Menguji akurasi model dan menyediakan visualisasi untuk analisis.
3. Menyediakan antarmuka web interaktif dengan autentikasi pengguna melalui Streamlit.

---

## 🧠 Teknologi yang Digunakan

- **Python 3**: Bahasa pemrograman utama.
- **Scikit-learn**: Untuk model machine learning dan evaluasi.
- **Pandas & NumPy**: Untuk manipulasi dan perhitungan data.
- **Matplotlib & Seaborn**: Untuk visualisasi data dan model.
- **Streamlit**: Untuk membangun antarmuka web interaktif.
- **Joblib**: Untuk menyimpan dan memuat model.
- **MySQL Connector & bcrypt**: Untuk autentikasi pengguna dan manajemen database.

---

## 🗂️ Struktur Folder

```
PREDIKSI_DIABETES/
├── data/                    # Dataset dan hasil prediksi
│   ├── diabetes.csv         # Dataset utama
│   └── hasil/               # Hasil evaluasi dan prediksi
│       ├── hasil_prediksi.csv
│       └── laporan_evaluasi.txt
├── model/                   # File model dan scaler
│   ├── model_diabetes.pkl
│   └── scaler_diabetes.pkl
├── visualisasi/             # Grafik hasil analisis
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   ├── feature_importance.png
│   ├── distribusi_kelas.png
│   └── korelasi.png
├── src/                     # Modul Python utama
│   ├── auth.py             # Autentikasi pengguna
│   ├── db_config.py        # Konfigurasi database
│   ├── evaluasi_model.py   # Evaluasi model
│   ├── pelatihan_model.py  # Pelatihan model
│   └── preprocessing.py    # Pembersihan dan normalisasi data
├── main.py                  # Titik masuk program berbasis Streamlit
├── README.md
└── requirements.txt         # Daftar pustaka Python
```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Clone repositori dan masuk ke folder:

```bash
git clone <repo-url>
cd PREDIKSI_DIABETES
```

### 2. Siapkan Database:
- Instal MySQL dan buat database bernama `prediksi_diabetes`.
- Buat tabel `pengguna` dengan skema berikut:
  ```sql
  CREATE TABLE pengguna (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nama_lengkap VARCHAR(100) NOT NULL,
      username VARCHAR(50) NOT NULL UNIQUE,
      password VARCHAR(255) NOT NULL,
      role ENUM('user', 'admin') DEFAULT 'user',
      tanggal_daftar DATETIME NOT NULL
  );
  ```
- Sesuaikan konfigurasi di `src/db_config.py` (host, user, password) jika berbeda.

### 3. Install semua pustaka:

```bash
pip install -r requirements.txt
```

### 4. Pastikan Data Tersedia:
- Tempatkan file `data/diabetes.csv` di folder `data/`.
- Jalankan pelatihan model jika file di `model/` belum ada:
  ```bash
  python src/pelatihan_model.py
  ```

### 5. Jalankan program:

```bash
streamlit run main.py
```

### 6. Akses Aplikasi:
- Buka browser dan kunjungi `http://localhost:8501`.
- Registrasi atau login untuk memulai.

---

## 📋 Menu Utama Aplikasi

| No | Menu                              | Deskripsi                                  |
|----|-----------------------------------|--------------------------------------------|
| 1  | Prediksi Diabetes untuk Data Baru | Input data pasien, prediksi, dan simpan hasil |
| 2  | Lihat Evaluasi Model              | Tampilkan akurasi, ROC AUC, dan matriks konfusi |
| 3  | Informasi Dataset                 | Statistik dan distribusi kelas pasien       |
| 4  | Lihat Hasil Prediksi Sebelumnya   | Riwayat prediksi dari file CSV             |
| 5  | Keluar                            | Keluar dari aplikasi (khusus CLI jika ada) |

**Catatan**: Menu ini diakses melalui dashboard Streamlit setelah login. Admin memiliki akses tambahan untuk mengelola pengguna.

---

## 📈 Hasil yang Dihasilkan

- `hasil/laporan_evaluasi.txt`: Laporan evaluasi model (akurasi, ROC AUC, dll.).
- `hasil/hasil_prediksi.csv`: Data prediksi termasuk fitur dominan.
- `visualisasi/*.png`: Grafik evaluasi (confusion matrix, ROC curve, dll.).

---

## 📚 Dataset

Dataset yang digunakan: [Pima Indians Diabetes Dataset (Kaggle)](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)
- Berisi fitur seperti jumlah kehamilan, glukosa, tekanan darah, BMI, dll.
- Target: `Outcome` (0 = tidak diabetes, 1 = diabetes).

---

## ✍️ Penulis

Nama: Rian Hadi Rhamdani  
Tahun: 2025  

---

## 📌 Lisensi

Proyek ini dapat digunakan untuk pembelajaran dan penelitian. Harap beri atribusi jika digunakan untuk keperluan akademik atau publikasi.
