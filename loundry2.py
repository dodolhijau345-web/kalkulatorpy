import streamlit as st
import datetime
import urllib.parse
import pandas as pd

# 1. SETTING AWAL
st.set_page_config(page_title="Kasir Jabufi Laundry", page_icon="🧺", layout="wide")
hide_st_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. DATA TOKO
NAMA_TOKO = "JABUFI LAUNDRY"
ALAMAT = "Kp. Pulo"
NO_WA_TOKO = "6289887666666" 

# 3. DAFTAR HARGA
HARGA = {"Cuci Kering": 7000, "Cuci + Setrika": 9000, "Setrika Saja": 5000, "Selimut": 25000, "Bed Cover": 35000}

# 4. BIKIN BUKU KAS - INI KUNCINYA PAK
if 'riwayat' not in st.session_state:
    st.session_state.riwayat = [] # List buat nyimpen semua order

# 5. TAMPILAN KIRI: INPUT
col1, col2 = st.columns([1, 1.5])
with col1:
    st.title(f"🧺 {NAMA_TOKO}")
    st.caption(f"{ALAMAT} | WA: 0898876666")
    
    with st.form("form_kasir", clear_on_submit=True): # clear_on_submit biar form kosong lagi
        st.subheader("📝 Input Pesanan Baru")
        nama = st.text_input("Nama Pelanggan")
        no_hp = st.text_input("No WA Pelanggan", placeholder="08xxxxxxxxxx")
        jenis = st.selectbox("Jenis Layanan", list(HARGA.keys()))
        berat = st.number_input("Berat (Kg)", min_value=0.5, step=0.5)
        catatan = st.text_area("Catatan")
        submitted = st.form_submit_button("💰 SIMPAN ORDERAN")

    if submitted:
        total = HARGA[jenis] * berat
        order_baru = {
            "Waktu": datetime.datetime.now().strftime("%d-%m %H:%M"),
            "Kode": f"JBF{datetime.datetime.now().strftime('%H%M%S')}",
            "Nama": nama,
            "Layanan": jenis,
            "Berat": berat,
            "Total": total,
            "WA": no_hp
        }
        st.session_state.riwayat.append(order_baru) # MASUKIN KE BUKU KAS
        st.rerun() # Refresh halaman biar langsung muncul

# 6. TAMPILAN KAN: RIWAYAT + TOTAL
with col2:
    st.subheader("📊 Buku Kas Hari Ini")
    
    if st.session_state.riwayat:
        df = pd.DataFrame(st.session_state.riwayat)
        
        # TOTAL ORDER MASUK
        total_kg = df["Berat"].sum()
        total_rp = df["Total"].sum()
        st.metric("Total Omzet Hari Ini", f"Rp {total_rp:,}")
        st.metric("Total Kg Masuk", f"{total_kg} Kg")
        
        st.dataframe(df, use_container_width=True) # TABEL RIWAYAT
        
        # TOMBOL KIRIM WA ORDER TERAKHIR
        order_terakhir = st.session_state.riwayat[-1]
        struk = f"*{NAMA_TOKO}*\nKode: {order_terakhir['Kode']}\nNama: {order_terakhir['Nama']}\nLayanan: {order_terakhir['Layanan']}\nBerat: {order_terakhir['Berat']}Kg\nTOTAL: Rp {order_terakhir['Total']:,}\nTerima kasih 🙏"
        pesan_wa = urllib.parse.quote(struk)
        link_wa_pelanggan = f"https://wa.me/62{order_terakhir['WA'][1:]}?text={pesan_wa}"
        st.link_button("📲 Kirim Struk Order Terakhir via WA", link_wa_pelanggan)
        
    else:
        st.info("Belum ada orderan masuk hari ini")