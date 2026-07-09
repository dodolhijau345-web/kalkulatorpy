import streamlit as st
import datetime
import pandas as pd
import os
import urllib.parse # buat bikin link WA

# 1. LAS LAYAR ANTI SCROLL
st.set_page_config(page_title="Kasir Jabufi Laundry", page_icon="🧺", layout="wide")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    html, body,.stApp { overflow: hidden!important; height: 100vh; }
    </style>
""", unsafe_allow_html=True)

NAMA_TOKO = "JABUFI LAUNDRY"
ALAMAT = "Kp. Pulo"
FILE_DATA = "data_jabufi.csv"
HARGA = {"Cuci Kering": 7000, "Cuci + Setrika": 9000, "Setrika Saja": 5000, "Selimut": 25000, "Bed Cover": 35000}

# 2. BACA DATA LAMA
if os.path.exists(FILE_DATA):
    df = pd.read_csv(FILE_DATA)
else:
    df = pd.DataFrame(columns=["Waktu", "Kode", "Nama", "Layanan", "Berat", "Total", "WA"])

# 3. LAYOUT
st.title(f"🧺 {NAMA_TOKO}")
col1, col2 = st.columns([1.2, 2])

with col1: # INPUT
    with st.form("form_kasir", clear_on_submit=True):
        nama = st.text_input("Nama Pelanggan")
        no_hp = st.text_input("No WA Pelanggan", placeholder="08xxxxxxxxxx")
        jenis = st.selectbox("Layanan", list(HARGA.keys()))
        berat = st.number_input("Berat Kg", min_value=0.5, step=0.5)
        submitted = st.form_submit_button("💰 SIMPAN & BUAT STRUK", use_container_width=True)

    if submitted:
        total = HARGA[jenis] * berat
        waktu = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        kode = f"JBF{datetime.datetime.now().strftime('%H%M%S')}"

        order_baru = pd.DataFrame([{
            "Waktu": waktu, "Kode": kode, "Nama": nama, "Layanan": jenis, "Berat": berat, "Total": total, "WA": no_hp
        }])
        df = pd.concat([df, order_baru], ignore_index=True)
        df.to_csv(FILE_DATA, index=False)

        # 4. BIKIN STRUK DIGITAL
        struk = f"""*{NAMA_TOKO}*\n{ALAMAT}\n----------------\nKode : {kode}\nTgl : {waktu}\nNama : {nama}\n----------------\nLayanan : {jenis}\nBerat : {berat} Kg\nHarga : Rp {HARGA[jenis]:,}/Kg\n----------------\n*TOTAL : Rp {total:,}*\n----------------\nTerima kasih 🙏"""

        st.session_state['struk_terakhir'] = struk # Simpen struk terakhir
        st.session_state['wa_terakhir'] = no_hp
        st.rerun()

with col2: # RIWAYAT + TOMBOL WA
    c1, c2 = st.columns(2)
    if not df.empty:
        c1.metric("Total Omzet", f"Rp {df['Total'].sum():,}")
        c2.metric("Total Kg", f"{df['Berat'].sum()} Kg")

    st.subheader("📋 Riwayat 10 Order Terakhir")
    if not df.empty:
        st.dataframe(df.tail(10), use_container_width=True, height=300)

    # 5. INI TOMBOL PRINT DIGITAL NYA PAK
    if 'struk_terakhir' in st.session_state:
        st.divider()
        st.subheader("📤 Print Digital")
        st.code(st.session_state['struk_terakhir']) # Nampilin struk

        no_pelanggan = st.session_state['wa_terakhir']
        if no_pelanggan:
            no_wa_bener = "62" + no_pelanggan[1:] # ganti 08 jadi 62
            pesan_wa = urllib.parse.quote(st.session_state['struk_terakhir'])
            link_wa = f"https://wa.me/{no_wa_bener}?text={pesan_wa}"
            st.link_button("📲 KIRIM STRUK VIA WA", link_wa, use_container_width=True, type="primary")