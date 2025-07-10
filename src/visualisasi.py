import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import os

# Set gaya visualisasi
plt.style.use('seaborn-v0_8-darkgrid')
sns.set(style="darkgrid")
plt.rcParams.update({'font.size': 12})

def simpan_gambar(path):
    """
    Simpan plot ke file, pastikan folder tujuan ada.
    """
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    plt.savefig(path)

def plot_confusion_matrix(cm, save_path="visualisasi/confusion_matrix.png"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax)
    ax.set_title("Confusion Matrix")
    ax.set_ylabel('Actual')
    ax.set_xlabel('Predicted')
    ax.set_xticklabels(['Tidak Diabetes', 'Diabetes'])
    ax.set_yticklabels(['Tidak Diabetes', 'Diabetes'])
    fig.tight_layout()
    simpan_gambar(save_path)
    return fig

def plot_roc_curve(y_test, y_score, save_path="visualisasi/roc_curve.png"):
    fpr, tpr, _ = roc_curve(y_test, y_score)
    auc = roc_auc_score(y_test, y_score)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, label=f'AUC = {auc:.4f}')
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title("ROC Curve")
    ax.legend(loc='lower right')
    ax.grid(True)
    fig.tight_layout()
    simpan_gambar(save_path)
    return fig

def plot_feature_importance(model, feature_names, save_path="visualisasi/feature_importance.png"):
    coef = model.coef_[0]
    importance = pd.DataFrame({
        'Fitur': feature_names,
        'Koefisien': coef,
        'Penting': np.abs(coef)
    }).sort_values('Penting', ascending=False)

    warna = ['red' if c < 0 else 'green' for c in importance['Koefisien']]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(importance['Fitur'], importance['Koefisien'], color=warna)
    ax.set_xticks(np.arange(len(importance['Fitur'])))
    ax.set_xticklabels(importance['Fitur'], rotation=45, ha='right')
    ax.set_title("Koefisien Fitur dalam Model Regresi Logistik")
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    fig.tight_layout()
    simpan_gambar(save_path)
    return fig

def plot_distribusi_kelas(df, save_path="visualisasi/distribusi_kelas.png"):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=df, x='Outcome', palette='Set2', ax=ax)
    ax.set_title('Distribusi Pasien Diabetes vs Tidak Diabetes')
    ax.set_xticklabels(['Tidak Diabetes', 'Diabetes'])
    ax.set_xlabel('Status Diabetes')
    ax.set_ylabel('Jumlah Pasien')
    fig.tight_layout()
    simpan_gambar(save_path)
    return fig

def plot_korelasi(df, save_path="visualisasi/korelasi.png"):
    korelasi = df.corr()
    mask = np.triu(np.ones_like(korelasi, dtype=bool))

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(korelasi, annot=True, fmt=".2f", cmap='coolwarm', mask=mask, ax=ax)
    ax.set_title('Matriks Korelasi antar Fitur')
    fig.tight_layout()
    simpan_gambar(save_path)
    return fig
