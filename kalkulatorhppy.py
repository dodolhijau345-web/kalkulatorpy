def kalkulator():
    print("Kalkulator Sederhana")
    print("Ketik 'keluar' buat berhenti")
    
    while True:
        rumus = input("\nMasukkan perhitungan: ")  # contoh: 12+3*4
        
        if rumus.lower() == 'keluar':
            print("Bye!")
            break
        
        try:
            # Ganti × dan ÷ biar bisa jalan
            rumus = rumus.replace("×", "*").replace("÷", "/")
            hasil = eval(rumus)
            print(f"Hasil: {hasil}")
        except:
            print("Error! Cek lagi rumusnya")

kalkulator()