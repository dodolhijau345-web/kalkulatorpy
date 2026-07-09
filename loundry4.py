import streamlit as st
import datetime
import urllib.parse
import pandas as pd
import os # buat cek file

# 1. SETTING AWAL
st.set_page_config(page_title="Kasir Jabufi Laundry", page_icon="🧺", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

NAMA_TOKO = "JABUFI LAUNDRY"
FILE_DATA = "data_jabufi.csv" # NAMA BUKU BESAR KITA
HARGA = {"Cuci Kering": 7000, "Cuci + Setrika": 9000, "Setrika Saja": 5000, "Selimut": 25000, "Bed Cover": 35000}

# 2. BACA DATA LAMA DULU KALO ADA
if os.path.exists(FILE_DATA):
    df = pd.read_csv(FILE_DATA)
else:
    df = pd.DataFrame(columns=["Waktu", "Kode", "Nama", "Layanan", "Berat", "Total", "WA"])

# 3. FORM INPUT KIRI
col1, col2 = st.columns([1, 1.5])
with col1:
    st.title(f"🧺 {NAMA_TOKO}")
    with st.form("form_kasir", clear_on_submit=True):
        nama = st.text_input("Nama Pelanggan")
        no_hp = st.text_input("No WA Pelanggan", placeholder="08xxxxxxxxxx")
        jenis = st.selectbox("Jenis Layanan", list(HARGA.keys()))
        berat = st.number_input("Berat (Kg)", min_value=0.5, step=0.5)
        submitted = st.form_submit_button("💰 SIMPAN ORDERAN")

    if submitted:
        total = HARGA[jenis] * berat
        order_baru = pd.DataFrame([{
            "Waktu": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Kode": f"JBF{datetime.datetime.now().strftime('%H%M%S')}",
            "Nama": nama, "Layanan": jenis, "Berat": berat, "Total": total, "WA": no_hp
        }])
        df = pd.concat([df, order_baru], ignore_index=True)
        df.to_csv(FILE_DATA, index=False) # INI KUNCINYA: SIMPEN KE FILE
        st.success("Orderan Tersimpan!")
        st.rerun()

# 4. TABEL + TOTAL KAN
with col2:
    st.subheader("📊 Buku Kas Jabufi")
    if not df.empty:
        st.metric("Total Omzet", f"Rp {df['Total'].sum():,}")
        st.metric("Total Kg", f"{df['Berat'].sum()} Kg")
        st.dataframe(df, use_container_width=True)
        
        # TOMBOL DOWNLOAD BACKUP
        st.download_button("💾 Download Data Excel", df.to_csv(index=False).encode('utf-8'), "laporan_jabufi.csv", "text/csv")
    else:
        st.info("Belum ada orderan")