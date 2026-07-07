import streamlit as st

st.set_page_config(page_title="Kasir Uwi", page_icon="🍧", layout="wide")

st.title("🍧 KASIR ES CREAM AWING LEGEND")
st.caption("Jajan es terenak sedunia akhirat")

harga_es = 5000

# BAGI 2 KOLOM: KIRI INPUT, KANAN STRUK
kolom_kiri, kolom_kanan = st.columns([2, 1]) # kolom kiri 2x lebih lebar

with kolom_kiri:
    st.subheader("📝 Pesan Di Sini")
    nama = st.text_input("Nama Pemesan", placeholder="Contoh: Uwi")
    jumlah = st.number_input("Jumlah Es Cup", min_value=1, value=1, step=1)
    
    pake_topping = st.checkbox("Tambah Topping Keju +Rp 2.000")
    
    tombol_hitung = st.button("🧮 HITUNG SEKARANG", use_container_width=True)

with kolom_kanan:
    st.subheader("🧾 Struk Kamu")
    st.image("https://i.imgur.com/8z8QY3a.png", caption="Es Uwi Segar") # gambar es random
    
    if tombol_hitung:
        if nama == "":
            st.error("Nama kosong!")
        else:
            total_es = harga_es * jumlah
            total_topping = 2000 if pake_topping else 0
            total_awal = total_es + total_topping
            
            # DISKON
            if jumlah >= 10:
                diskon = 0.5
                st.balloons()
            elif jumlah >= 5:
                diskon = 0.3
            elif jumlah >= 2:
                diskon = 0.2
            else:
                diskon = 0
            
            potongan = total_awal * diskon
            total_bayar = total_awal - potongan
            
            # TAMPILIN STRUK
            st.write(f"**Nama:** {nama}")
            st.write(f"**Es {jumlah}x:** Rp {total_es:,}")
            if pake_topping:
                st.write(f"**Topping:** Rp {total_topping:,}")
            if diskon > 0:
                st.write(f"**Diskon {int(diskon*100)}%:** -Rp {potongan:,.0f}")
            
            st.success(f"**TOTAL: Rp {total_bayar:,.0f}**")
    else:
        st.info("Isi pesanan dulu di kiri ya")

st.divider()
st.write("Dibuat pake ❤️ sama Uwi & Meta AI")