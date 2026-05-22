import datetime
import webbrowser
from collections import Counter

def tampilkan_menu():
    """Menampilkan menu pilihan"""
    print("\n========= BROWSER SEDERHANA =========")
    print("1. Buka Website")
    print("2. Lihat Semua History")
    print("3. Cari History")
    print("4. Lihat Situs Paling Sering Dikunjungi")
    print("5. Filter History Berdasarkan Tanggal")
    print("6. Hapus History")
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
        
def top_situs():
    """Menampilkan situs yang paling sering dikunjungi (Poin 2)"""
    isi_history = baca_history()
    if not isi_history:
        print("\nHistory masih kosong!")
        return

    list_url = []
    for baris in isi_history:
        parts = baris.strip().split(" | ", 1)
        if len(parts) == 2:
            list_url.append(parts[1])
            
    # Menghitung kemunculan URL menggunakan Counter
    hitungan_situs = Counter(list_url)
    top_5 = hitungan_situs.most_common(5)
    
    print("\n=== 5 SITUS PALING SERING DIKUNJUNGI ===")
    print(f"{'Peringkat':<9} | {'Jumlah Buka':<12} | {'URL Website'}")
    print("-" * 75)
    for i, (url, jumlah) in enumerate(top_5):
        print(f"#{i+1:<8} | {jumlah:<12} | {url}")
    print("-" * 75)

def filter_waktu_history():
    """Filter history berdasarkan tanggal"""

    isi_history = baca_history()

    if not isi_history:
        print("\nHistory masih kosong!")
        return

    print("\nFormat tanggal: YYYY-MM-DD")
    tanggal_cari = input("Masukkan tanggal: ")

    hasil_filter = []

    for baris in isi_history:
        parts = baris.strip().split(" | ", 1)

        if len(parts) == 2:
            waktu = parts[0]
            tanggal_history = waktu.split(" ")[0]

            if tanggal_history == tanggal_cari:
                hasil_filter.append(baris)

    if hasil_filter:
        tampilkan_tabel_history(
            hasil_filter,
            f"HISTORY TANGGAL {tanggal_cari}"
        )
    else:
        print(f"\n✗ Tidak ada history pada tanggal {tanggal_cari}")


def hapus_history():
    """Fungsi untuk menghapus history"""
    isi_history = baca_history()

    if not isi_history:
        print("\nHistory masih kosong!")
        return

    print("\n=== MENU HAPUS ===")
    print("1. Pilih history yang mau dihapus")
    print("2. Hapus SEMUA history")
    print("0. Batal")
    print("==================")

    pilihan_menu = input("\nPilih menu: ")

    try:
        nomor_menu = int(pilihan_menu)

        if nomor_menu == 0:
            konfirmasi_batal = input("Yakin nih mau dibatalin? (y/n): ")
            if konfirmasi_batal.lower() == "y":
                print("✗ Penghapusan dibatalkan, kembali ke menu utama")
            else:
                print("✓ Oke, balik lagi nih ke menu hapus.")
                hapus_history()

        elif nomor_menu == 1:
            tampilkan_tabel_history(isi_history, "MENGHAPUS HISTORY (Pilih Nomor)")

            pilihan_nomor = input(f"\nMasukkan nomor history yang mau dihapus (1-{len(isi_history)}): ")
            try:
                nomor_hapus = int(pilihan_nomor)

                if 1 <= nomor_hapus <= len(isi_history):
                    item_dihapus = isi_history[nomor_hapus - 1]
                    print(f"\nAnda akan menghapus:")
                    print(f"  {item_dihapus.strip()}")

                    konfirmasi = input("\nYakin nih mau dihapus? (y/n): ")

                    if konfirmasi.lower() == "y":
                        isi_history.pop(nomor_hapus - 1)
                        with open("history.txt", "w") as file:
                            file.writelines(isi_history)

                        print(f"✓ History nomor {nomor_hapus} berhasil dihapus!")
                    else:
                        print("✗ Penghapusan dibatalkan")
                else:
                    print(f"✗ Pilih yang bener dong! Pilih 1-{len(isi_history)}")

            except ValueError:
                print("✗ Input yang bener lah! Harus pake nomor")

        elif nomor_menu == 2:
            konfirmasi = input("Yakin mau hapus SEMUA history? (y/n): ")
            if konfirmasi.lower() == "y":
                with open("history.txt", "w") as file:
                    file.write("")
                print("✓ Semua history berhasil dihapus!")
            else:
                print("✗ Penghapusan dibatalkan")

        else:
            print("✗ Pilih yang bener dong! Pilih 0, 1, atau 2")

    except ValueError:
        print("✗ Input yang bener lah! Harus pake nomor")


def main():
    print("Selamat datang di Browser Sederhana!")
    
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-6): ")
        
        if pilihan == "1":
            buka_website()
        elif pilihan == "2":
            lihat_history()
        elif pilihan == "3":
            cari_history()
        elif pilihan == "4":
            top_situs()
        elif pilihan == "5":
            filter_waktu_history()
        elif pilihan == "6":
            hapus_history()
        elif pilihan == "0":
            print("\nTerima kasih! Sampai jumpa!")
            break
        else:
            print("\n✗ Pilih yang bener dong! Pilih 0-6")

if __name__ == "__main__":
    main()
