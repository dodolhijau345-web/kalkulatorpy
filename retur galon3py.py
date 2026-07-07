import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("Input Data Retur Galon")

# 1. Menggunakan session_state agar form tidak reset otomatis
if 'terima' not in st.session_state:
    st.session_state.terima = 0
if 'retur' not in st.session_state:
    st.session_state.retur = 0

# 2. Input Data
nama_depo = st.text_input("Nama Depo", value="Bojong")
# Nilai default diambil dari session_state
jumlah_terima = st.number_input("Jumlah Terima", value=st.session_state.terima)
jumlah_retur = st.number_input("Jumlah Retur", value=st.session_state.retur)

# 3. Tombol Simpan
if st.button("Simpan Data"):
    # Logika simpan (misalnya ke list atau database)
    st.success(f"Data {nama_depo} berhasil ditambahkan!")
    
    # Reset atau Update session state jika perlu
    st.session_state.terima = jumlah_terima
    st.session_state.retur = jumlah_retur

# 4. Tabel Analisis Otomatis
st.subheader("Data Retur per Depo")
data = {
    'Depo': ['Bogor', 'Bojong'],
    'Terima': [300000, jumlah_terima],
    'Retur': [344, jumlah_retur]
}
df = pd.DataFrame(data)

# Menghitung Persen Retur Otomatis
df['Persen Retur (%)'] = (df['Retur'] / df['Terima'] * 100).round(2)
st.table(df)