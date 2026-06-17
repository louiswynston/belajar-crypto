const tombol = document.getElementById("tombol");
const hasil = document.getElementById("hasil");

tombol.addEventListener("click", async () => {
    hasil.textContent = "Mengambil data...";
    
    const response = await fetch("https://api.coinbase.com/v2/prices/BTC-USD/spot");
    const data = await response.json();
    
    hasil.textContent = "Harga Bitcoin sekarang: $" + data.data.amount;
});