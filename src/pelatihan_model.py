import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def bagi_data(X, y, test_size=0.2, random_state=42):
    """
    Membagi data menjadi data latih dan uji.
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"Jumlah data latih: {X_train.shape[0]}")
        print(f"Jumlah data uji: {X_test.shape[0]}")
        print(f"Distribusi kelas data latih:\n{y_train.value_counts()}")
        print(f"Distribusi kelas data uji:\n{y_test.value_counts()}")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Error saat membagi data: {e}")
        raise

def latih_model(X_train, y_train, scaler, simpan_model=True,
                model_path='model/model_diabetes.pkl',
                scaler_path='model/scaler_diabetes.pkl'):
    """
    Melatih model dengan hyperparameter tuning menggunakan GridSearchCV.
    Jika model sudah ada, akan dimuat ulang.
    """
    try:
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            print("✅ Model dimuat dari file yang sudah ada.")
        else:
            print("Melatih model baru dengan GridSearchCV...")
            param_grid = {
                'C': [0.01, 0.1, 1, 10, 100],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear'],
                'max_iter': [1000]
            }
            grid = GridSearchCV(
                LogisticRegression(random_state=42),
                param_grid,
                cv=5,
                scoring='accuracy'
            )
            grid.fit(X_train, y_train)
            model = grid.best_estimator_
            print(f"✅ Model selesai dilatih. Parameter terbaik: {grid.best_params_}")

            if simpan_model:
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                joblib.dump(model, model_path)
                joblib.dump(scaler, scaler_path)
                print("✅ Model dan scaler disimpan ke file.")
        
        return model
    except Exception as e:
        print(f"Error saat melatih model: {e}")
        raise

# Eksekusi utama
if __name__ == "__main__":
    try:
        # Muat data
        data = pd.read_csv('data/diabetes.csv')
        print("Kolom di dataset:", data.columns.tolist())
        X = data.drop('Outcome', axis=1)
        y = data['Outcome']
        print("Distribusi kelas data asli:\n", y.value_counts())

        # Bagi data
        X_train, X_test, y_train, y_test = bagi_data(X, y)

        # Skalakan data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Latih model
        model = latih_model(X_train_scaled, y_train, scaler, simpan_model=True)

        # Evaluasi model
        y_pred = model.predict(X_test_scaled)
        print(f"Akurasi model: {accuracy_score(y_test, y_pred):.2f}")

        print("✅ Proses pelatihan selesai!")
    except Exception as e:
        print(f"Error utama: {e}")