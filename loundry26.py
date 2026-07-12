import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import urllib.parse
from io import BytesIO # <-- TAMBAHAN BUAT EXCEL RAPI

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

wib = datetime.utcnow() + timedelta(hours=7)
jam_sekarang = wib.strftime('%d-%m-%Y %H:%M:%S')

st.title("🧺 JABUFI LAUNDRY")
st.caption(f"Kp. Pulo | 🕒 {jam_sekarang}")
st.divider()

# FORM OTOMATIS KOSONG SETELAH SIMPAN
with st.form("form_input", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Pelanggan", key="nama_input")
    with col2:
        no_wa = st.text_input("No WA", placeholder="62812...", key="wa_input")

    layanan = st.selectbox("Layanan", ["Cuci Kering 7rb/kg", "Cuci+Setrika 9rb/kg", "Setrika 5rb/kg"], key="layanan_input")
    harga_per_kg = 7000 if "7rb" in layanan else 9000 if "9rb" in layanan else 5000
    kg = st.number_input("Berat Kg", min_value=0.1, step=0.1, key="kg_input")

    total = kg * harga_per_kg
    st.write(f"**Total: Rp {total:,.0f}**")

    submitted = st.form_submit_button("🧺 SIMPAN & BUAT STRUK", use_container_width=True)

    if submitted:
        if nama and no_wa:
            nota = f"JF{wib.strftime('%d%m%H%M%S')}"
            waktu = wib.strftime('%d-%m-%Y %H:%M:%S')
            data = (waktu, nota, nama, no_wa, layanan, kg, total)
            tambah_transaksi(data)
            st.success(f"Nota {nota} tersimpan di Brankas!")
            st.session_state['nota_terakhir'] = {"Nota":nota, "Nama":nama, "WA":no_wa, "Layanan":layanan, "Kg":kg, "Total":total}
        else:
            st.warning("Nama dan No WA wajib diisi!")

st.divider()
st.subheader("📊 Buku Kas & Riwayat")
df = ambil_semua_data()

if not df.empty:
    # BIKIN KOLOM TANGGAL BUAT FILTER HARI INI
    df['tanggal'] = pd.to_datetime(df['waktu'], format='%d-%m-%Y %H:%M:%S').dt.date
    hari_ini = wib.date()

    total_semua = df['total'].sum()
    df_hari_ini = df[df['tanggal'] == hari_ini]
    total_hari_ini = df_hari_ini['total'].sum()
    jumlah_pelanggan_hari_ini = df_hari_ini.shape[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Hari Ini", f"Rp {total_hari_ini:,.0f}")
    c2.metric("👥 Pelanggan", f"{jumlah_pelanggan_hari_ini} Orang")
    c3.metric("🏦 Total Semua", f"Rp {total_semua:,.0f}")

    # TAMPILAN DI APP TETAP
    df_tampil = df.drop(columns=['tanggal']) # sembunyiin kolom tanggal
    st.dataframe(df_tampil.head(10), use_container_width=True, height=200)

    # INI BAGIAN DOWNLOAD YANG UDAH RAPI
    df_excel = df.drop(columns=['id', 'tanggal']) # hapus id & tanggal
    df_excel.columns = ['Waktu', 'No Nota', 'Nama Pelanggan', 'No WA', 'Layanan', 'Kg', 'Total Rp'] # ganti nama kolom
    df_excel['Total Rp'] = df_excel['Total Rp'].apply(lambda x: f"Rp {x:,.0f}") # format jadi Rp

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_excel.to_excel(writer, sheet_name='Riwayat Laundry', index=False)
    excel_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Data Excel",
        data=excel_data,
        file_name=f"data_jabufi_{wib.strftime('%d-%m-%Y')}.csv", # nama file ada tanggalnya
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    with st.popover("🗑️ RESET SEMUA RIWAYAT"):
        st.warning("⚠️ YAKIN MAU HAPUS SEMUA DATA?")
        st.write("Tindakan ini tidak bisa dibatalkan!")
        if st.button("YA, HAPUS SEMUA", type="primary", use_container_width=True):
            reset_data()
            st.success("Data berhasil dihapus!")
            st.rerun()

else:
    st.info("Belum ada riwayat")

if 'nota_terakhir' in st.session_state:
    st.divider()
    st.subheader("📤 Print Digital")
    data = st.session_state['nota_terakhir']
    pesan = f"""🧺 *JABUFI LAUNDRY* 🧺\nKp. Pulo\nYth. {data['Nama']}\nNota : *{data['Nota']}*\nStatus : SUDAH SELESAI ✅\nLayanan : {data['Layanan']}\nBerat : {data['Kg']} Kg\nTotal : *Rp {data['Total']:,.0f}*\n\nSilakan ambil ya 🙏"""
    st.code(pesan)
    link_wa = f"https://wa.me/{data['WA']}?text={urllib.parse.quote(pesan)}"
    st.link_button("KLIK UNTUK KIRIM KE WA", link_wa, use_container_width=True, type="primary")