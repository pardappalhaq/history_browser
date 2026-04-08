import datetime
import webbrowser

def tampilkan_menu():
    """Menampilkan menu pilihan"""
    print("\n========= BROWSER SEDERHANA =========")
    print("1. Buka Website")
    print("2. Lihat Semua History (Tabel & Pagination)")
    print("3. Cari History (Berdasarkan Keyword)")
    print("0. Keluar")
    print("=====================================")

def baca_history():
    """Membaca isi history dan mengembalikan list of strings"""
    try:
        with open("history.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def tampilkan_tabel_history(isi_history, judul="HISTORY BROWSING"):
    """Menampilkan history dalam bentuk tabel dengan pagination (Poin 3 & 7)"""
    if not isi_history:
        print(f"\n{judul} masih kosong!")
        return

    # Param Pagination
    item_per_halaman = 10
    total_item = len(isi_history)
    total_halaman = (total_item + item_per_halaman - 1) // item_per_halaman
    
    halaman_sekarang = 1

    while True:
        print(f"\n=== {judul} ===")
        # Header Tabel
        print(f"{'No':<4} | {'Waktu Buka':<20} | {'URL Website'}")
        print("-" * 75)

        start_idx = (halaman_sekarang - 1) * item_per_halaman
        end_idx = start_idx + item_per_halaman
        item_ditampilkan = isi_history[start_idx:end_idx]

        for i, baris in enumerate(item_ditampilkan):
            nomor = int(start_idx) + int(i) + 1
            # Format history.txt: YYYY-MM-DD HH:MM:SS | URL
            parts = baris.strip().split(" | ", 1)
            if len(parts) == 2:
                waktu, url = parts
                print(f"{nomor:<4} | {waktu:<20} | {url}")
            else:
                # Fallback if format is missed
                print(f"{nomor:<4} | {'Tidak diketahui':<20} | {baris.strip()}")

        print("-" * 75)
        print(f"📄 Halaman {halaman_sekarang} dari {total_halaman} (Total {total_item} website)")
        
        if total_halaman > 1:
            print("\nNavigasi: 'n' (Next), 'p' (Prev), 'q' (Keluar)")
            aksi = input("Beri perintah atau lgsg tekan Enter untuk Keluar: ").lower()
            if aksi == 'n' and halaman_sekarang < total_halaman:
                halaman_sekarang += 1
            elif aksi == 'p' and halaman_sekarang > 1:
                halaman_sekarang -= 1
            else:
                break
        else:
            break

def buka_website():
    """Fungsi untuk 'membuka' website"""
    url = input("\nMasukkan URL website (contoh: google.com): ")
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    waktu_sekarang = datetime.datetime.now()
    waktu_format = waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S")
    
    with open("history.txt", "a") as file:
        file.write(f"{waktu_format} | {url}\n")
    
    print(f"🌐 Membuka {url} di browser...")
    webbrowser.open(url)
    
    print(f"✓ Berhasil membuka: {url}")
    print(f"✓ Tersimpan di history pada {waktu_format}")

def lihat_history():
    """Fungsi untuk melihat history browsing dengan tabel dan pagination"""
    isi_history = baca_history()
    tampilkan_tabel_history(isi_history, "SEMUA HISTORY")
    
def cari_history():
    """Mencari history berdasarkan keyword (Poin 1)"""
    isi_history = baca_history()
    if not isi_history:
        print("\nHistory masih kosong!")
        return
        
    keyword = input("\nMasukkan kata kunci website yang ingin dicari (contoh: youtube): ").lower()
    hasil_pencarian = []
    
    for baris in isi_history:
        if keyword in baris.lower():
            hasil_pencarian.append(baris)
            
    if hasil_pencarian:
        tampilkan_tabel_history(hasil_pencarian, f"HASIL PENCARIAN: '{keyword}'")
    else:
        print(f"\n✗ Tidak ada history yang cocok dengan kata kunci '{keyword}'.")

def main():
    print("Selamat datang di Browser Sederhana!")
    
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-3): ")
        
        if pilihan == "1":
            buka_website()
        elif pilihan == "2":
            lihat_history()
        elif pilihan == "3":
            cari_history()
        elif pilihan == "0":
            print("\nTerima kasih! Sampai jumpa!")
            break
        else:
            print("\n✗ Pilih yang bener dong! Pilih 1-3")

if __name__ == "__main__":
    main()
