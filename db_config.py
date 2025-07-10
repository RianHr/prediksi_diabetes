import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="prediksi_diabetes"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Gagal terkoneksi ke database: {e}")
        return None
