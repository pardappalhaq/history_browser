import datetime
import webbrowser
from collections import Counter

try:
    from fpdf import FPDF
except ImportError:
    print("Install fpdf: pip install fpdf")
    exit(1)

def tampilkan_menu():
    """Menampilkan menu pilihan"""
    print("\n========= BROWSER SEDERHANA =========")
    print("1. Cari")
    print("2. Lihat History")
    print("3. Cari History")
    print("4. Lihat Situs Paling Sering Dikunjungi")
    print("5. Hapus History")
    print("6. Print History")
    print("0. Keluar")
    print("=====================================")

def baca_history():
    """Membaca isi history dan mengembalikan list of strings"""
    try:
        with open("history.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def get_hari_indonesia(tanggal_str):
    """Mengembalikan nama hari dalam bahasa Indonesia"""
    try:
        # Format: YYYY-MM-DD HH:MM:SS
        tanggal_obj = datetime.datetime.strptime(tanggal_str, "%Y-%m-%d %H:%M:%S")
        hari_inggris = tanggal_obj.strftime("%A")

        # Mapping hari Inggris ke Indonesia
        mapping_hari = {
            "Monday": "Senin",
            "Tuesday": "Selasa",
            "Wednesday": "Rabu",
            "Thursday": "Kamis",
            "Friday": "Jumat",
            "Saturday": "Sabtu",
            "Sunday": "Minggu"
        }
        return mapping_hari.get(hari_inggris, "-")
    except:
        return "-"

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
        print(f"{'No':<4} | {'Hari':<8} | {'Waktu Buka':<20} | {'URL Website'}")
        print("-" * 85)

        start_idx = (halaman_sekarang - 1) * item_per_halaman
        end_idx = start_idx + item_per_halaman
        item_ditampilkan = isi_history[start_idx:end_idx]

        for i, baris in enumerate(item_ditampilkan):
            nomor = int(start_idx) + int(i) + 1
            # Format history.txt: YYYY-MM-DD HH:MM:SS | URL
            parts = baris.strip().split(" | ", 1)
            if len(parts) == 2:
                waktu, url = parts
                hari = get_hari_indonesia(waktu)
                print(f"{nomor:<4} | {hari:<8} | {waktu:<20} | {url}")
            else:
                # Fallback if format is missed
                print(f"{nomor:<4} | {'-':<8} | {'Tidak diketahui':<20} | {baris.strip()}")

        print("-" * 85)
        print(f"[Page] Halaman {halaman_sekarang} dari {total_halaman} (Total {total_item} website)")
        
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

def cari_apapun():
    """Fungsi untuk mencari apapun di Google"""
    keyword = input("\nKamu mau cari apa?: ").strip()
    if not keyword:
        print("[X] Kata kunci tidak boleh kosong!")
        return

    # Buat URL pencarian Google
    url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"

    waktu_sekarang = datetime.datetime.now()
    waktu_format = waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S")

    with open("history.txt", "a") as file:
        file.write(f"{waktu_format} | {url}\n")

    print(f"[Search] Mencari '{keyword}' di Google...")
    webbrowser.open(url)
    print(f"[OK] Hasil pencarian terbuka")
    print(f"[OK] Tersimpan di history pada {waktu_format}")

def lihat_history():
    """Fungsi untuk melihat history browsing dengan tabel dan pagination"""
    print("\n=== PILIH TAMPILAN HISTORY ===")
    print("1. Lihat semua history")
    print("2. Lihat history hari ini")
    print("3. Lihat history beberapa hari terakhir")
    print("======================================")

    pilihan = input("Pilih menu (1/2/3): ")

    if pilihan == "2":
        # Lihat history hari ini
        from datetime import timedelta
        sekarang = datetime.datetime.now()
        batas_tanggal = sekarang.replace(hour=0, minute=0, second=0, microsecond=0)

        isi_history = baca_history()
        hasil_filter = []

        for baris in isi_history:
            parts = baris.strip().split(" | ", 1)
            if len(parts) == 2:
                waktu_str = parts[0]
                try:
                    waktu_obj = datetime.datetime.strptime(waktu_str, "%Y-%m-%d %H:%M:%S")
                    if waktu_obj >= batas_tanggal:
                        hasil_filter.append(baris)
                except:
                    pass

        if hasil_filter:
            tampilkan_tabel_history(hasil_filter, "HISTORY HARI INI")
        else:
            print("\n[X] Tidak ada history hari ini")

    elif pilihan == "3":
        try:
            hari = int(input("\nMasukkan jumlah hari terakhir yang ingin dilihat: "))
            if hari < 1:
                print("[X] Jumlah hari harus lebih dari 0")
                return

            from datetime import timedelta
            batas_tanggal = datetime.datetime.now() - timedelta(days=hari)

            isi_history = baca_history()
            hasil_filter = []

            for baris in isi_history:
                parts = baris.strip().split(" | ", 1)
                if len(parts) == 2:
                    waktu_str = parts[0]
                    try:
                        waktu_obj = datetime.datetime.strptime(waktu_str, "%Y-%m-%d %H:%M:%S")
                        if waktu_obj >= batas_tanggal:
                            hasil_filter.append(baris)
                    except:
                        pass

            if hasil_filter:
                tampilkan_tabel_history(hasil_filter, f"HISTORY {hari} HARI TERAKHIR")
            else:
                print(f"\n[X] Tidak ada history dalam {hari} hari terakhir")

        except ValueError:
            print("[X] Input harus berupa angka!")
    else:
        # Lihat semua history (default)
        isi_history = baca_history()
        tampilkan_tabel_history(isi_history, "SEMUA HISTORY")
    
def cari_history():
    """Mencari history berdasarkan keyword atau tanggal (Poin 1)"""
    isi_history = baca_history()
    if not isi_history:
        print("\nHistory masih kosong!")
        return

    print("\n=== PILIH JENIS PENCARIAN ===")
    print("1. Cari berdasarkan nama website")
    print("2. Cari berdasarkan tanggal")
    print("=================================")

    pilihan = input("Pilih menu (1/2): ")

    if pilihan == "2":
        # Cari berdasarkan tanggal
        print("\nFormat tanggal: YYYY-MM-DD")
        tanggal_cari = input("Masukkan tanggal yang ingin dicari: ").strip()

        hasil_pencarian = []
        for baris in isi_history:
            parts = baris.strip().split(" | ", 1)
            if len(parts) == 2:
                waktu = parts[0]
                tanggal_history = waktu.split(" ")[0]
                if tanggal_history == tanggal_cari:
                    hasil_pencarian.append(baris)

        if hasil_pencarian:
            tampilkan_tabel_history(hasil_pencarian, f"HISTORY TANGGAL {tanggal_cari}")
        else:
            print(f"\n[X] Tidak ada history pada tanggal {tanggal_cari}")

    else:
        # Cari berdasarkan keyword (default)
        keyword = input("\nMasukkan kata kunci website yang ingin dicari (contoh: youtube): ").lower()
        hasil_pencarian = []

        for baris in isi_history:
            if keyword in baris.lower():
                hasil_pencarian.append(baris)

        if hasil_pencarian:
            tampilkan_tabel_history(hasil_pencarian, f"HASIL PENCARIAN: '{keyword}'")
        else:
            print(f"\n[X] Tidak ada history yang cocok dengan kata kunci '{keyword}'.")
        
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
    print("-" * 85)
    for i, (url, jumlah) in enumerate(top_5):
        print(f"#{i+1:<8} | {jumlah:<12} | {url}")
    print("-" * 85)

def hapus_history():
    """Fungsi untuk menghapus history"""
    isi_history = baca_history()

    if not isi_history:
        print("\nHistory masih kosong!")
        return

    print("\n=== MENU HAPUS ===")
    print("1. Pilih history yang mau dihapus")
    print("2. Hapus beberapa hari terakhir")
    print("3. Hapus history hari ini")
    print("4. Hapus SEMUA history")
    print("0. Batal")
    print("==================")

    pilihan_menu = input("\nPilih menu: ")

    try:
        nomor_menu = int(pilihan_menu)

        if nomor_menu == 0:
            konfirmasi_batal = input("Yakin nih mau dibatalin? (y/n): ")
            if konfirmasi_batal.lower() == "y":
                print("[X] Penghapusan dibatalkan, kembali ke menu utama")
            else:
                print("[OK] Oke, balik lagi nih ke menu hapus.")
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

                        print(f"[OK] History nomor {nomor_hapus} berhasil dihapus!")
                    else:
                        print("[X] Penghapusan dibatalkan")
                else:
                    print(f"[X] Pilih yang bener dong! Pilih 1-{len(isi_history)}")

            except ValueError:
                print("[X] Input yang bener lah! Harus pake nomor")

        elif nomor_menu == 2:
            try:
                hari = int(input("\nMasukkan jumlah hari terakhir yang mau dihapus: "))
                if hari < 1:
                    print("[X] Jumlah hari harus lebih dari 0")
                    return

                from datetime import timedelta
                batas_tanggal = datetime.datetime.now() - timedelta(days=hari)

                hasil_hapus = []
                hasil_sisa = []

                for baris in isi_history:
                    parts = baris.strip().split(" | ", 1)
                    if len(parts) == 2:
                        waktu_str = parts[0]
                        try:
                            waktu_obj = datetime.datetime.strptime(waktu_str, "%Y-%m-%d %H:%M:%S")
                            if waktu_obj >= batas_tanggal:
                                hasil_hapus.append(baris)
                            else:
                                hasil_sisa.append(baris)
                        except:
                            hasil_sisa.append(baris)
                    else:
                        hasil_sisa.append(baris)

                if hasil_hapus:
                    print(f"\nAkan menghapus {len(hasil_hapus)} history:")
                    for h in hasil_hapus[:5]:
                        print(f"  - {h.strip()}")
                    if len(hasil_hapus) > 5:
                        print(f"  ... dan {len(hasil_hapus) - 5} lagi")

                    konfirmasi = input("\nYakin mau dihapus? (y/n): ")
                    if konfirmasi.lower() == "y":
                        with open("history.txt", "w") as file:
                            file.writelines(hasil_sisa)
                        print(f"[OK] {len(hasil_hapus)} history berhasil dihapus!")
                    else:
                        print("[X] Penghapusan dibatalkan")
                else:
                    print(f"\n[X] Tidak ada history dalam {hari} hari terakhir")

            except ValueError:
                print("[X] Input harus berupa angka!")

        elif nomor_menu == 3:
            # Hapus history hari ini
            from datetime import timedelta
            sekarang = datetime.datetime.now()
            batas_tanggal = sekarang.replace(hour=0, minute=0, second=0, microsecond=0)

            hasil_hapus = []
            hasil_sisa = []

            for baris in isi_history:
                parts = baris.strip().split(" | ", 1)
                if len(parts) == 2:
                    waktu_str = parts[0]
                    try:
                        waktu_obj = datetime.datetime.strptime(waktu_str, "%Y-%m-%d %H:%M:%S")
                        if waktu_obj >= batas_tanggal:
                            hasil_hapus.append(baris)
                        else:
                            hasil_sisa.append(baris)
                    except:
                        hasil_sisa.append(baris)
                else:
                    hasil_sisa.append(baris)

            if hasil_hapus:
                print(f"\nAkan menghapus {len(hasil_hapus)} history hari ini:")
                for h in hasil_hapus[:5]:
                    print(f"  - {h.strip()}")
                if len(hasil_hapus) > 5:
                    print(f"  ... dan {len(hasil_hapus) - 5} lagi")

                konfirmasi = input("\nYakin mau dihapus? (y/n): ")
                if konfirmasi.lower() == "y":
                    with open("history.txt", "w") as file:
                        file.writelines(hasil_sisa)
                    print(f"[OK] {len(hasil_hapus)} history hari ini berhasil dihapus!")
                else:
                    print("[X] Penghapusan dibatalkan")
            else:
                print("\n[X] Tidak ada history hari ini")

        elif nomor_menu == 4:
            konfirmasi = input("Yakin mau hapus SEMUA history? (y/n): ")
            if konfirmasi.lower() == "y":
                with open("history.txt", "w") as file:
                    file.write("")
                print("[OK] Semua history berhasil dihapus!")
            else:
                print("[X] Penghapusan dibatalkan")

        else:
            print("[X] Pilih yang bener dong! Pilih 0, 1, 2, 3, atau 4")

    except ValueError:
        print("[X] Input yang bener lah! Harus pake nomor")


def print_history():
    """Fungsi untuk print/save history ke file PDF"""
    print("\n=== PILIH JENIS PRINT ===")
    print("1. Print history hari ini")
    print("2. Print history beberapa hari terakhir")
    print("3. Print semua history")
    print("===================================")

    pilihan = input("Pilih menu (1/2/3): ")

    from datetime import timedelta
    sekarang = datetime.datetime.now()

    if pilihan == "1":
        batas_tanggal = sekarang.replace(hour=0, minute=0, second=0, microsecond=0)
        isi_history = baca_history()
        hasil_filter = []

        for baris in isi_history:
            parts = baris.strip().split(" | ", 1)
            if len(parts) == 2:
                waktu_str = parts[0]
                try:
                    waktu_obj = datetime.datetime.strptime(waktu_str, "%Y-%m-%d %H:%M:%S")
                    if waktu_obj >= batas_tanggal:
                        hasil_filter.append(baris)
                except:
                    pass

        if hasil_filter:
            simpan_ke_pdf(hasil_filter, "history_hari_ini.pdf", "HISTORY HARI INI")
        else:
            print("\n[X] Tidak ada history hari ini")

    elif pilihan == "2":
        try:
            hari = int(input("\nMasukkan jumlah hari terakhir: "))
            if hari < 1:
                print("[X] Jumlah hari harus lebih dari 0")
                return

            batas_tanggal = sekarang - timedelta(days=hari)
            isi_history = baca_history()
            hasil_filter = []

            for baris in isi_history:
                parts = baris.strip().split(" | ", 1)
                if len(parts) == 2:
                    waktu_str = parts[0]
                    try:
                        waktu_obj = datetime.datetime.strptime(waktu_str, "%Y-%m-%d %H:%M:%S")
                        if waktu_obj >= batas_tanggal:
                            hasil_filter.append(baris)
                    except:
                        pass

            if hasil_filter:
                nama_file = f"history_{hari}_hari.pdf"
                simpan_ke_pdf(hasil_filter, nama_file, f"HISTORY {hari} HARI TERAKHIR")
            else:
                print(f"\n[X] Tidak ada history dalam {hari} hari terakhir")

        except ValueError:
            print("[X] Input harus berupa angka!")

    else:
        isi_history = baca_history()
        if isi_history:
            simpan_ke_pdf(isi_history, "semua_history.pdf", "SEMUA HISTORY")
        else:
            print("\n[X] History masih kosong")


def simpan_ke_pdf(isi_history, nama_file, judul):
    """Simpan history ke file PDF yang rapih dan terstruktur"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, judul, ln=True, align="C")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(10, 8, "No", 1, 0, "C", True)
        pdf.cell(25, 8, "Hari", 1, 0, "C", True)
        pdf.cell(45, 8, "Waktu Buka", 1, 0, "C", True)
        pdf.cell(0, 8, "URL Website", 1, 1, "C", True)

        pdf.set_font("Arial", "", 9)
        for i, baris in enumerate(isi_history):
            parts = baris.strip().split(" | ", 1)
            if len(parts) == 2:
                waktu, url = parts
                hari = get_hari_indonesia(waktu)
                pdf.cell(10, 7, str(i + 1), 1, 0, "C")
                pdf.cell(25, 7, hari, 1, 0, "L")
                pdf.cell(45, 7, waktu, 1, 0, "L")
                pdf.cell(0, 7, url[:60] + ("..." if len(url) > 60 else ""), 1, 1, "L")

        pdf.ln(5)
        pdf.set_font("Arial", "I", 9)
        pdf.cell(0, 7, f"Total: {len(isi_history)} data", ln=True, align="R")

        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 7, f"Dicetak pada: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")

        pdf.output(nama_file)
        print(f"[OK] History berhasil disimpan ke file PDF: {nama_file}")
    except Exception as e:
        print(f"[X] Gagal menyimpan file PDF: {e}")


def main():
    print("Selamat datang di Browser Sederhana!")
    
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-6): ")
        
        if pilihan == "1":
            cari_apapun()
        elif pilihan == "2":
            lihat_history()
        elif pilihan == "3":
            cari_history()
        elif pilihan == "4":
            top_situs()
        elif pilihan == "5":
            hapus_history()
        elif pilihan == "6":
            print_history()
        elif pilihan == "0":
            print("\nTerima kasih! Sampai jumpa!")
            break
        else:
            print("\n[X] Pilih yang bener dong! Pilih 0-6")

if __name__ == "__main__":
    main()
