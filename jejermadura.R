<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#dc3545">
<title>Kasir Warung Madura</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<style>
  body { font-family: Arial; background: #f2f2f2; padding: 10px; }
  .box { background: white; padding: 15px; border-radius: 10px; max-width: 500px; margin: auto; }
  h2 { text-align: center; color: #dc3545; margin-bottom: 5px; }
  .install-btn { background:#007bff; color:white; border:none; padding:12px; border-radius:5px; width:100%; margin-bottom:15px; display:none; font-weight:bold; }
  
  /* INPUT JEJER KEBAWAH */
  .form-input label { display:block; font-weight:bold; margin-top:10px; margin-bottom:5px; }
  .form-input input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; box-sizing:border-box; }
  .btn-tambah { background: #28a745; color: white; border: none; padding: 12px; border-radius: 5px; font-weight: bold; cursor: pointer; width:100%; margin-top:15px; font-size:16px; }
  
  table { width: 100%; margin-top: 15px; border-collapse: collapse; font-size:14px; }
  th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
  th { background: #007bff; color: white; }
  .btn-hapus { background: #dc3545; color: white; border: none; padding: 4px 8px; border-radius: 3px; cursor: pointer; }
  .total-box { background: #e7f3ff; padding: 15px; border-radius: 8px; margin-top: 15px; }
  .total { font-size: 26px; color: #dc3545; font-weight: bold; text-align:right; }
  .bayar-box input { width:100%; padding:10px; margin-top:5px; box-sizing:border-box; }
  .kembalian { font-size: 20px; color: #28a745; font-weight: bold; text-align:right; margin-top:5px; }
</style>
</head>
<body>

<div class="box">
  <button id="installBtn" class="install-btn">📲 INSTALL APLIKASI</button>
  <h2>🛒 KASIR WARUNG MADURA</h2>

  <!-- INPUT JEJER KEBAWAH -->
  <div class="form-input">
    <label>Nama Barang</label>
    <input type="text" id="namaBarang" placeholder="Contoh: Rokok, Kopi, Gula">
    
    <label>Harga Rp</label>
    <input type="number" id="hargaBarang" placeholder="Contoh: 25000">
    
    <button class="btn-tambah" onclick="tambahBarang()">+ TAMBAHKAN KE KERANJANG</button>
  </div>

  <!-- TABEL TRANSAKSI -->
  <table id="tabel">
    <tr><th>No</th><th>Barang</th><th>Harga</th><th></th></tr>
  </table>

  <!-- TOTAL & BAYAR -->
  <div class="total-box">
    <h3>TOTAL BELANJA</h3>
    <div class="total">Rp <span id="total">0</span></div>
    
    <label style="font-weight:bold;">Uang Bayar</label>
    <div class="bayar-box">
      <input type="number" id="uangBayar" placeholder="Masukkan uang bayar" oninput="hitungKembalian()">
    </div>
    <div>Kembalian: <span class="kembalian">Rp <span id="kembalian">0</span></span></div>
    
    <button class="btn-tambah" style="background:#007bff;" onclick="reset()">RESET TRANSAKSI BARU</button>
  </div>
</div>

<script>
let data = JSON.parse(localStorage.getItem('kasirMadura')) || [];

function tambahBarang(){
  let nama = document.getElementById('namaBarang').value;
  let harga = document.getElementById('hargaBarang').value;
  
  if(!nama || !harga){ alert('Isi Nama dan Harga dulu'); return; }
  
  data.push({nama: nama, harga: parseInt(harga)});
  localStorage.setItem('kasirMadura', JSON.stringify(data));
  document.getElementById('namaBarang').value = '';
  document.getElementById('hargaBarang').value = '';
  document.getElementById('namaBarang').focus();
  tampilkan();
}

function hapus(index){
  data.splice(index, 1);
  localStorage.setItem('kasirMadura', JSON.stringify(data));
  tampilkan();
}

function tampilkan(){
  let tabel = document.getElementById('tabel');
  let total = 0;
  
  tabel.innerHTML = '<tr><th>No</th><th>Barang</th><th>Harga</th><th></th></tr>';
  
  data.forEach((d, i) => {
    total += d.harga;
    tabel.innerHTML += `
      <tr>
        <td>${i+1}</td>
        <td>${d.nama}</td>
        <td>Rp ${d.harga.toLocaleString('id-ID')}</td>
        <td><button class="btn-hapus" onclick="hapus(${i})">X</button></td>
      </tr>
    `;
  });
  
  document.getElementById('total').innerText = total.toLocaleString('id-ID');
  hitungKembalian();
}

function hitungKembalian(){
  let total = data.reduce((sum, d) => sum + d.harga, 0);
  let bayar = parseInt(document.getElementById('uangBayar').value) || 0;
  document.getElementById('kembalian').innerText = (bayar - total).toLocaleString('id-ID');
}

function reset(){
  if(confirm('Mulai transaksi baru?')){
    data = [];
    localStorage.removeItem('kasirMadura');
    document.getElementById('uangBayar').value = '';
    tampilkan();
  }
}

document.getElementById('hargaBarang').addEventListener('keypress', function(e){
  if(e.key === 'Enter') tambahBarang();
});
tampilkan();

// ===== KODE PWA LENGKAP =====
let deferredPrompt;
const installBtn = document.getElementById('installBtn');
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBtn.style.display = 'block';
});
installBtn.addEventListener('click', async () => {
  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  installBtn.style.display = 'none';
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js');
}
</script>

</body>
</html>