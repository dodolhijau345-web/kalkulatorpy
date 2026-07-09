import streamlit as st
import datetime
import pandas as pd
import os
import urllib.parse

# 1. SETTING LAYAR ANTI SCROLL
st.set_page_config(page_title="Kasir Jabufi Laundry", page_icon="🧺", layout="wide")
st.markdown("""<style>#MainMenu,footer,header{visibility:hidden;} html,body,.stApp{overflow:hidden!important;height:100vh;}</style>""", unsafe_allow_html=True)

NAMA_TOKO = "JABUFI LAUNDRY"
ALAMAT = "Kp. Pulo"
FILE_DATA = "data_jabufi.csv"
HARGA = {"Cuci Kering": 7000, "Cuci + Setrika": 9000, "Setrika Saja": 5000, "Selimut": 25000, "Bed Cover": 35000}

# 2. BACA DATA LAMA
if os.path.exists(FILE_DATA):
    df = pd.read_csv(FILE_DATA)
    df['Waktu'] = pd.to_datetime(df['Waktu'], errors='coerce')
    df = df.dropna(subset=['Waktu'])
else:
    df = pd.DataFrame(columns=["Waktu", "Kode", "Nama", "Layanan", "Berat", "Total", "WA"])

# 3. BAGI LAYAR
st.title(f"🧺 {NAMA_TOKO} | {ALAMAT}")
col1, col2 = st.columns([1.2, 2])

with col1: # INPUT
    with st.form("form_kasir", clear_on_submit=True):
        nama = st.text_input("Nama Pelanggan")
        no_hp = st.text_input("No WA Pelanggan", placeholder="08xxxxxxxxxx")
        jenis = st.selectbox("Jenis Layanan", list(HARGA.keys()))
        berat = st.number_input("Berat (Kg)", min_value=0.5, step=0.5)
        submitted = st.form_submit_button("💰 SIMPAN & BUAT STRUK", use_container_width=True, type="primary")

    if submitted and nama and no_hp:
        total = HARGA[jenis] * berat
        waktu = datetime.datetime.now()
        kode = f"JBF{waktu.strftime('%H%M%S')}"
        order_baru = pd.DataFrame([{"Waktu": waktu, "Kode": kode, "Nama": nama, "Layanan": jenis, "Berat": berat, "Total": total, "WA": no_hp}])
        df = pd.concat([df, order_baru], ignore_index=True)
        df.to_csv(FILE_DATA, index=False)
        struk = f"*{NAMA_TOKO}*\n{ALAMAT}\n----------------\nKode : {kode}\nTgl : {waktu.strftime('%d-%m-%Y %H:%M')}\nNama : {nama}\n----------------\nLayanan : {jenis}\nBerat : {berat} Kg\n----------------\n*TOTAL : Rp {total:,}*\n----------------\nTerima kasih 🙏"
        st.session_state['struk_terakhir'] = struk
        st.session_state['wa_terakhir'] = no_hp
        st.toast("✅ Orderan Tersimpan!", icon="🧺")
        st.rerun()
    elif submitted:
        st.warning("Nama dan No WA wajib diisi!")

with col2: # RIWAYAT + TOTAL
    if not df.empty:
        hari_ini = df[df['Waktu'].dt.date == datetime.date.today()]
        minggu_ini = df[df['Waktu'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Hari Ini", f"Rp {hari_ini['Total'].sum():,}")
        c2.metric("📅 7 Hari", f"Rp {minggu_ini['Total'].sum():,}")
        c3.metric("🏦 Total Semua", f"Rp {df['Total'].sum():,}")

    st.subheader("📋 Riwayat 10 Order Terakhir")
    if not df.empty:
        df_tampil = df.sort_values('Waktu', ascending=False).head(10)
        st.dataframe(df_tampil, use_container_width=True, height=250)
    else:
        st.info("Belum ada orderan")

    # 4. INI TOMBOL RESET NYA PAK
    st.divider()
    with st.expander("⚠️ Zona Bahaya: Reset Data"):
        st.write("Hati-hati! Ini akan menghapus SEMUA riwayat orderan selamanya.")
        if st.button("🗑️ HAPUS SEMUA RIWAYAT", type="secondary", use_container_width=True):
            if os.path.exists(FILE_DATA):
                os.remove(FILE_DATA) # HAPUS FILE
            st.success("Data berhasil direset!")
            st.rerun()

    # TOMBOL PRINT DIGITAL WA
    if 'struk_terakhir' in st.session_state:
        st.divider()
        st.subheader("📤 Print Digital")
        st.code(st.session_state['struk_terakhir'])
        no_pelanggan = st.session_state['wa_terakhir']
        if no_pelanggan.startswith('0'):
            no_wa_bener = "62" + no_pelanggan[1:]
        else:
            no_wa_bener = no_pelanggan
        pesan_wa = urllib.parse.quote(st.session_state['struk_terakhir'])
        link_wa = f"https://wa.me/{no_wa_bener}?text={pesan_wa}"
        st.link_button("📲 KIRIM STRUK VIA WA", link_wa, use_container_width=True, type="primary")