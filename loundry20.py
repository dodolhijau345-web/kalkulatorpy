import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import urllib.parse

st.set_page_config(page_title="JABUFI LAUNDRY", layout="centered")

st.markdown("""<style>#MainMenu,footer,header,button[kind="toolbar"]{display:none;} div.stButton>button{background-color:#2563EB;color:white;font-size:18px;font-weight:bold;border-radius:10px;height:3em;width:100%;border:none;}</style>""", unsafe_allow_html=True)

DB_FILE = "jabufi.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (id INTEGER PRIMARY KEY AUTOINCREMENT, waktu TEXT, nota TEXT, nama TEXT, wa TEXT, layanan TEXT, kg REAL, total INTEGER)''')
    conn.commit()
    conn.close()

def tambah_transaksi(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO transaksi (waktu, nota, nama, wa, layanan, kg, total) VALUES (?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()

def ambil_semua_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM transaksi ORDER BY id DESC", conn)
    conn.close()
    return df

def reset_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM transaksi")
    conn.commit()
    conn.close()

init_db()

# 1. JAM WIB DIBIKIN DULU DI ATAS BIAR GAK ERROR
wib = datetime.utcnow() + timedelta(hours=7)
jam_sekarang = wib.strftime('%d-%m-%Y %H:%M:%S')

st.title("🧺 JABUFI LAUNDRY")
st.caption(f"Kp. Pulo | 🕒 {jam_sekarang}")
st.divider()

col1, col2 = st.columns(2)
with col1: nama = st.text_input("Nama Pelanggan")
with col2: no_wa = st.text_input("No WA", placeholder="62812...")

layanan = st.selectbox("Layanan", ["Cuci Kering 7rb/kg", "Cuci+Setrika 9rb/kg", "Setrika 5rb/kg"])
harga_per_kg = 7000 if "7rb" in layanan else 9000 if "9rb" in layanan else 5000
kg = st.number_input("Berat Kg", min_value=0.1, step=0.1)
total = kg * harga_per_kg
st.write(f"**Total: Rp {total:,.0f}**")

if st.button("🧺 SIMPAN & BUAT STRUK"):
    if nama and no_wa:
        nota = f"JF{wib.strftime('%d%m%H%M%S')}"
        waktu = wib.strftime('%d-%m-%Y %H:%M:%S') # 2. PAKE wib YANG UDAH DIBIKIN
        data = (waktu, nota, nama, no_wa, layanan, kg, total)
        tambah_transaksi(data)
        st.success(f"Nota {nota} tersimpan di Brankas!")
        st.session_state['nota_terakhir'] = {"Nota":nota, "Nama":nama, "WA":no_wa, "Layanan":layanan, "Kg":kg, "Total":total}
        st.rerun()
    else: st.warning("Nama dan No WA wajib diisi!")

st.divider()
st.subheader("📊 Buku Kas & Riwayat")
df = ambil_semua_data()

if not df.empty:
    total_semua = df['total'].sum()
    hari_ini_str = wib.strftime('%Y-%m-%d') # 3. PAKE wib JUGA

    total_hari_ini = df[df['waktu'].str.contains(hari_ini_str)]['total'].sum()
    c1, c2 = st.columns(2)
    c1.metric("💰 Hari Ini", f"Rp {total_hari_ini:,.0f}")
    c2.metric("🏦 Total Semua", f"Rp {total_semua:,.0f}")
    st.dataframe(df.head(10), use_container_width=True, height=200)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Data Excel", csv, "data_jabufi.csv", "text/csv")
    if st.button("🗑️ RESET SEMUA RIWAYAT", type="secondary"):
        reset_data()
        st.rerun()
else:
    st.info("Belum ada riwayat")

if 'nota_terakhir' in st.session_state:
    st.divider()
    st.subheader("📤 Print Digital")
    data = st.session_state['nota_terakhir']
    pesan = f"""🧺 *JABUFI LAUNDRY* 🧺\nKp. Pulo\nYth. {data['Nama']}\nNota    : *{data['Nota']}*\nStatus  : SUDAH SELESAI ✅\nLayanan : {data['Layanan']}\nBerat   : {data['Kg']} Kg\nTotal   : *Rp {data['Total']:,.0f}*\n\nSilakan ambil ya 🙏"""
    st.code(pesan)
    link_wa = f"https://wa.me/{data['WA']}?text={urllib.parse.quote(pesan)}"
    st.link_button("KLIK UNTUK KIRIM KE WA", link_wa, use_container_width=True, type="primary") # 4. KOMA DIHAPUS