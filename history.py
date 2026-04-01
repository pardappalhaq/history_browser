import datetime
import webbrowser

def tampilkan_menu():
    """Menampilkan menu pilihan"""
    print("\n=== BROWSER SEDERHANA ===")
    print("1. Buka Website")
    print("========================")

def buka_website():
    """Fungsi untuk 'membuka' website"""
    url = input("Masukkan URL website: ")
    
    # Memastikan URL memiliki protokol http:// atau https://
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    # Mendapatkan waktu sekarang
    waktu_sekarang = datetime.datetime.now()
    waktu_format = waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S")
    
    # Menyimpan ke file history.txt
    with open("history.txt", "a") as file:
        file.write(f"{waktu_format} | {url}\n")
    
    # Membuka URL di browser
    print(f"🌐 Membuka {url} di browser...")
    webbrowser.open(url)
    
    print(f"✓ Berhasil membuka: {url}")
    print(f"✓ Tersimpan di history pada {waktu_format}")

# Program Utama
def main():
    print("Selamat datang di Browser Sederhana!")
    
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-4): ")
        
        if pilihan == "1":
            buka_website()

# Menjalankan program
if __name__ == "__main__":
    main()
