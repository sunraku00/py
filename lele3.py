import datetime
from tabulate import tabulate

class Kamar:
    def __init__(self):
        self.tipe_kamar_list = [
            "Standard Room",
            "Deluxe Room", 
            "Family Room (2 tempat tidur)",
            "Family Room (3 tempat tidur)"
        ]

        self.fasilitas_kamar = {
            "Standard Room": ["Kasur nyaman ukuran Queen", "AC & Wi-Fi gratis", "TV LED 32 inci", "Kamar mandi dengan shower"],
            "Deluxe Room": ["Kasur ukuran King", "AC & Wi-Fi", "TV LED 42 inci dengan layanan streaming", "Kamar mandi dengan bathtub", "Balkon"],
            "Family Room (2 tempat tidur)": ["2 Kasur ukuran Queen", "AC & Wi-Fi", "TV LED 50 inci dengan layanan streaming", "Kamar mandi luas dengan bathtub", "Ruang tamu kecil", "Sarapan gratis"],
            "Family Room (3 tempat tidur)": ["2 Kasur ukuran Queen", "AC & Wi-Fi", "TV LED 50 inci dengan layanan streaming", "Kamar mandi luas dengan bathtub", "Ruang tamu kecil", "Sarapan gratis"]
        }

        self.nomor_kamar = {
            "Standard Room": ["1A", "2B", "3C", "4C", "5D"],
            "Deluxe Room": ["6E", "7F", "8G"],
            "Family Room (2 tempat tidur)": ["9H", "10J", "11K"],
            "Family Room (3 tempat tidur)": ["12L", "13M", "14N"]
        }

        self.harga_kamar = {
            "Standard Room": 150000,
            "Deluxe Room": 225000,
            "Family Room (2 tempat tidur)": 345000,
            "Family Room (3 tempat tidur)": 410000
        }

    def tampil_info_kamar(self):
        print("Tipe Kamar yang Tersedia:")
        for i, tipe in enumerate(self.tipe_kamar_list, start=1):
            print(f"{i}. {tipe} - Rp {self.harga_kamar[tipe]:,}")
            print("   Fasilitas:")
            for fasilitas in self.fasilitas_kamar[tipe]:
                print(f"   - {fasilitas}")

    def kamar_terisi(self):
        terisi = set()
        try:
            with open("data_checkin.txt", "r") as file:
                for line in file:
                    data = line.strip().split(" | ")
                    if len(data) >= 14 and data[13] == "BELUM":
                        kamar_data = data[14:]
                        for i in range(1, len(kamar_data), 3):
                            if i < len(kamar_data):
                                terisi.add(kamar_data[i])
        except FileNotFoundError:
            pass
        return terisi

    def tampil_status_kamar(self, tipe_kamar_dipilih=None):
        """Menampilkan status kamar dalam format tabel"""
        if tipe_kamar_dipilih is None:
            tipe_kamar_dipilih = self.tipe_kamar_list
            
        kamar_terisi = self.kamar_terisi()
        
        headers = ["Tipe Kamar", "Kamar 1", "Kamar 2", "Kamar 3", "Kamar 4", "Kamar 5"]
        table = []
        for tipe in self.tipe_kamar_list:
            row = [tipe]
            kamar_list = self.nomor_kamar[tipe]
            for i in range(5):
                if i < len(kamar_list):
                    nomor = kamar_list[i]
                    status = "T" if nomor in kamar_terisi else "K"
                    cell = f"{nomor}/{status}"
                    row.append(cell)
                else:
                    row.append("---")
            table.append(row)
        
        print("\n" + "="*88)
        print("                     STATUS KAMAR PENGINAPAN CHOCO")
        print("="*88)
        print(tabulate(table, headers=headers, tablefmt="grid"))
        print("Keterangan:")
        print("  K = Kosong    T = Terisi    --- = Tidak Ada Kamar")
        print("="*88)

class Tamu:
    def __init__(self):
        self.nama = input("Masukkan nama pemesan: ")
        self._nik = self._validasi_nik()
        self._telepon = self._validasi_telepon()

    def _validasi_nik(self):
        while True:
            try:
                nik_input = input("Masukkan NIK: ")
                if not nik_input.isdigit():
                    raise ValueError("NIK hanya boleh berisi angka")
                if len(nik_input) != 16:
                    raise ValueError("NIK harus terdiri dari 16 digit")
                return nik_input
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Silakan coba lagi.")

    def _validasi_telepon(self):
        while True:
            try:
                telepon_input = input("Masukkan No. Telepon: ")
                if not telepon_input.isdigit():
                    raise ValueError("Nomor telepon hanya boleh berisi angka")
                if len(telepon_input) < 10 or len(telepon_input) > 13:
                    raise ValueError("Nomor telepon harus terdiri dari 10-13 digit")
                return telepon_input
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Silakan coba lagi.")

class Pemesanan(Kamar, Tamu):
    def __init__(self):
        Kamar.__init__(self)
        Tamu.__init__(self)
        
        self.jumlah_pesanan = int(input("Masukkan jumlah kamar yang ingin dipesan: "))
        self.tipe_kamar_dipilih = self._input_tipe_kamar()
        self.kamar_dipesan = self._pesan_kamar()
        self.waktu_checkin, self.lama_menginap, self.checkout = self._input_checkin_and_checkout()
        self.total_harga = self._hitung_total_harga()
        self.status_pembayaran, self.dp_dibayar, self.sisa_pembayaran = self._input_pembayaran()
        self.metode_pembayaran = self._input_metode_pembayaran()
        self.crash = 0
        self.id_transaksi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def _input_tipe_kamar(self):
        tipe_kamar_dipilih = []
        print("Pilih tipe kamar untuk tiap kamar yang dipesan:")
        for i in range(self.jumlah_pesanan):
            print(f"Pilihan tipe kamar ke-{i + 1}:")
            self.tampil_info_kamar()
            while True:
                pilihan = input(f"Pilih tipe kamar (1-{len(self.tipe_kamar_list)}): ")
                if pilihan.isdigit() and 1 <= int(pilihan) <= len(self.tipe_kamar_list):
                    tipe_kamar_dipilih.append(self.tipe_kamar_list[int(pilihan) - 1])
                    break
                print("Input tidak valid, silakan masukkan nomor yang benar.")
        return tipe_kamar_dipilih

    def _pesan_kamar(self):
        kamar_terisi = super().kamar_terisi()
        kamar_dipesan = []
        
        for tipe in self.tipe_kamar_dipilih:
            kamar_tersedia = [kamar for kamar in self.nomor_kamar[tipe] 
                             if kamar not in kamar_terisi]
            if not kamar_tersedia:
                print(f"Maaf, tidak ada kamar kosong untuk tipe {tipe}. Silakan batalkan dan coba pesan ulang.")
                exit()
            
            print(f"Kamar tersedia untuk tipe {tipe}: {', '.join(kamar_tersedia)}")
            while True:
                nomor_kamar = input(f"Pilih nomor kamar (tipe {tipe}): ").upper()
                if nomor_kamar in kamar_tersedia:
                    kamar_terisi.add(nomor_kamar)
                    harga = self.harga_kamar[tipe]
                    kamar_dipesan.append({'tipe': tipe, 'nomor': nomor_kamar, 'harga': harga})
                    break
                print("Nomor kamar tidak valid atau sudah terisi. Silakan pilih ulang.")
        
        return kamar_dipesan

    def _input_checkin_and_checkout(self):
        while True:
            try:
                tanggal = input("Masukkan tanggal check-in (DD-MM-YYYY): ")
                jam = input("Masukkan jam check-in (HH:MM): ")
                waktu_checkin = datetime.datetime.strptime(f"{tanggal} {jam}", "%d-%m-%Y %H:%M")
                
                lama_menginap = int(input("Masukkan lama menginap (malam): "))
                if lama_menginap <= 0:
                    print("Lama menginap harus lebih dari 0")
                    continue
                
                # Checkout adalah hari terakhir menginap + 1 hari pada jam 12:00
                checkout = waktu_checkin + datetime.timedelta(days=lama_menginap)
                checkout = checkout.replace(hour=12, minute=0, second=0, microsecond=0)
                
                return waktu_checkin, lama_menginap, checkout
            except ValueError:
                print("Format tanggal/jam tidak valid. Gunakan format DD-MM-YYYY untuk tanggal dan HH:MM untuk jam.")

    def _hitung_total_harga(self):
        return sum(item['harga'] for item in self.kamar_dipesan) * self.lama_menginap

    def _input_pembayaran(self):
        print(f"Total harga: Rp {self.total_harga:,}")
        print("Pilihan pembayaran:")
        print("1. Bayar DP 50% sekarang")
        print("2. Bayar lunas sekarang")
        
        while True:
            pilihan_bayar = input("Pilih opsi pembayaran (1/2): ")
            if pilihan_bayar in ['1', '2']:
                if pilihan_bayar == '1':
                    status_pembayaran = "DP"
                    dp_dibayar = self.total_harga // 2
                    sisa_pembayaran = self.total_harga - dp_dibayar
                    print(f"DP 50%: Rp {dp_dibayar:,}")
                    print(f"Sisa pembayaran: Rp {sisa_pembayaran:,}")
                else:
                    status_pembayaran = "LUNAS"
                    dp_dibayar = self.total_harga
                    sisa_pembayaran = 0
                return status_pembayaran, dp_dibayar, sisa_pembayaran

    def _input_metode_pembayaran(self):
        while True:
            metode_pembayaran = input("Metode pembayaran (Cash/Debit): ").capitalize()
            if metode_pembayaran in ["Cash", "Debit"]:
                return metode_pembayaran
            print("Metode pembayaran tidak valid. Pilih Cash atau Debit.")

    def simpan_data(self):
        with open("data_checkin.txt", "a") as file:
            kamar_info = ""
            for kamar in self.kamar_dipesan:
                kamar_info += f"{kamar['tipe']} | {kamar['nomor']} | {kamar['harga']} | "
            
            if kamar_info.endswith(' | '):
                kamar_info = kamar_info[:-3]
                
            file.write(f"{self.id_transaksi} | {self.nama} | {self._nik} | {self._telepon} | "
                      f"{self.jumlah_pesanan} | {self.waktu_checkin.strftime('%d-%m-%Y %H:%M')} | "
                      f"{self.checkout.strftime('%d-%m-%Y %H:%M')} | {self.lama_menginap} | "
                      f"{self.metode_pembayaran} | {self.total_harga} | {self.crash} | "
                      f"{self.status_pembayaran} | {self.sisa_pembayaran} | BELUM | {kamar_info}\n")
    
    def tampil_struk(self):
        print("\n" + "="*60)
        print("                      PENGINAPAN CHOCO                        ")
        print("             Jl. Coklat Manis No. 5, Surabaya                 ")
        print("                   Telp: (031) 888-9999                       ")
        print("="*60)
        
        print(f"\nNama Tamu         : {self.nama}")
        print(f"No. Telepon       : {self._telepon}")
        print(f"NIK               : {self._nik}")
        
        print("\nDetail kamar yang dipesan:")
        for idx, kamar in enumerate(self.kamar_dipesan, 1):
            print(f" {idx}. Tipe: {kamar['tipe']:<25} Nomor: {kamar['nomor']:<5} Harga/malam: Rp {kamar['harga']:,}")
        
        print(f"\nCheck-in          : {self.waktu_checkin.strftime('%d %B %Y (%H.%M)')}")
        print(f"Check-out         : {self.checkout.strftime('%d %B %Y (12.00)')}")
        print(f"Lama Menginap     : {self.lama_menginap} malam")
        
        print("\n--------------- INFORMASI PEMBAYARAN ----------------------")
        print(f"Total Harga       : Rp {self.total_harga:,}")
        if self.status_pembayaran == "DP":
            print(f"Status Pembayaran : DP 50%")
            print(f"DP Dibayar        : Rp {self.dp_dibayar:,}")
            print(f"Metode Pembayaran : {self.metode_pembayaran}")
            print(f"Sisa Pembayaran   : Rp {self.sisa_pembayaran:,}")
            print("(Sisa akan dibayar saat checkout)")
        else:
            print(f"Status Pembayaran : LUNAS")
            print(f"Metode Pembayaran : {self.metode_pembayaran}")
        
        print(f"Biaya Tambahan    : Rp {self.crash:,}")
        
        total_dibayar = self.dp_dibayar + self.crash
        print(f"Total yang Dibayar: Rp {total_dibayar:,}")
        print("="*60)

class CheckoutManager(Kamar):
    def __init__(self):
        super().__init__()

    def checkout_process(self):
        nik = input("Masukkan NIK untuk proses checkout: ")
        ditemukan = False
        
        try:
            with open("data_checkin.txt", "r") as file:
                lines = file.readlines()
            
            for line in lines:
                data = line.strip().split(" | ")
                if len(data) >= 14 and data[2] == nik and data[13] == "BELUM":
                    ditemukan = True
                    
                    # Load data dari file
                    self.id_transaksi = data[0]
                    self.nama = data[1]
                    self._nik = data[2]
                    self._telepon = data[3]
                    self.jumlah_pesanan = int(data[4])
                    self.waktu_checkin = datetime.datetime.strptime(data[5], "%d-%m-%Y %H:%M")
                    self.checkout_terjadwal = datetime.datetime.strptime(data[6], "%d-%m-%Y %H:%M")
                    self.lama_menginap = int(data[7])
                    self.metode_pembayaran = data[8]
                    self.total_harga_awal = int(data[9])
                    self.crash = int(data[10])
                    self.status_pembayaran = data[11]
                    self.sisa_pembayaran = int(data[12])
                    
                    # Process room data
                    kamar_data = data[14:]
                    self.kamar_dipesan = []
                    
                    for i in range(0, len(kamar_data), 3):
                        if i+2 < len(kamar_data):
                            kamar = {
                                'tipe': kamar_data[i],
                                'nomor': kamar_data[i+1],
                                'harga': int(kamar_data[i+2])
                            }
                            self.kamar_dipesan.append(kamar)
                    
                    print(f"\nData ditemukan untuk: {self.nama}")
                    print(f"Check-in: {self.waktu_checkin.strftime('%d-%m-%Y %H:%M')}")
                    print(f"Lama menginap: {self.lama_menginap} malam")
                    print(f"Check-out terjadwal: {self.checkout_terjadwal.strftime('%d-%m-%Y %H:%M')}")
                    print(f"Total harga kamar: Rp {self.total_harga_awal:,}")
                    print(f"Status pembayaran: {self.status_pembayaran}")
                    
                    if self.status_pembayaran == "DP":
                        print(f"Sisa pembayaran: Rp {self.sisa_pembayaran:,}")
                    
                    # Input waktu checkout aktual
                    while True:
                        try:
                            tanggal_checkout = input("Masukkan tanggal checkout aktual (DD-MM-YYYY): ")
                            jam_checkout = input("Masukkan jam checkout aktual (HH:MM): ")
                            waktu_checkout_aktual = datetime.datetime.strptime(f"{tanggal_checkout} {jam_checkout}", "%d-%m-%Y %H:%M")
                            break
                        except ValueError:
                            print("Format tanggal/jam tidak valid. Gunakan format DD-MM-YYYY untuk tanggal dan HH:MM untuk jam.")
                    
                    # Hitung keterlambatan
                    if waktu_checkout_aktual > self.checkout_terjadwal:
                        selisih = waktu_checkout_aktual - self.checkout_terjadwal
                        jam_terlambat = int(selisih.total_seconds() // 3600)
                        if selisih.total_seconds() % 3600 > 0:
                            jam_terlambat += 1
                        
                        self.crash = jam_terlambat * 50000
                        print(f"\nKeterlambatan checkout:")
                        print(f"Waktu checkout terjadwal: {self.checkout_terjadwal.strftime('%d-%m-%Y %H:%M')}")
                        print(f"Waktu checkout aktual: {waktu_checkout_aktual.strftime('%d-%m-%Y %H:%M')}")
                        print(f"Keterlambatan: {jam_terlambat} jam")
                        print(f"Biaya keterlambatan: {jam_terlambat} jam x Rp 50,000 = Rp {self.crash:,}")
                    else:
                        self.crash = 0
                        print(f"\nCheckout tepat waktu. Tidak ada biaya keterlambatan.")
                    
                    self.waktu_checkout_aktual = waktu_checkout_aktual
                    
                    # Proses pembayaran checkout
                    if self.status_pembayaran == "DP":
                        print("\nTotal yang harus dibayar saat checkout:")
                        print(f"Sisa pembayaran kamar: Rp {self.sisa_pembayaran:,}")
                        print(f"Biaya keterlambatan: Rp {self.crash:,}")
                        total_checkout = self.sisa_pembayaran + self.crash
                        print(f"Total checkout: Rp {total_checkout:,}")
                        
                        if total_checkout > 0:
                            while True:
                                metode = input("Metode pembayaran checkout (Cash/Debit): ").capitalize()
                                if metode in ["Cash", "Debit"]:
                                    self.metode_checkout = metode
                                    break
                                print("Metode pembayaran tidak valid. Pilih Cash atau Debit.")
                            
                            print("Pembayaran pelunasan berhasil!")
                        
                        self.status_pembayaran = "LUNAS"
                        self.sisa_pembayaran = 0
                    else:
                        if self.crash > 0:
                            print(f"\nBiaya keterlambatan yang harus dibayar: Rp {self.crash:,}")
                            while True:
                                metode = input("Metode pembayaran biaya keterlambatan (Cash/Debit): ").capitalize()
                                if metode in ["Cash", "Debit"]:
                                    self.metode_checkout = metode
                                    break
                                print("Metode pembayaran tidak valid. Pilih Cash atau Debit.")
                        else:
                            self.metode_checkout = self.metode_pembayaran
                    
                    self.total_harga = self.total_harga_awal + self.crash
                    
                    self.update_status_checkout(nik)
                    self.tampil_struk_checkout()
                    
                    break
        
        except FileNotFoundError:
            print("File data tidak ditemukan. Belum ada data pemesanan.")
        
        if not ditemukan:
            print("Data dengan NIK tersebut tidak ditemukan atau sudah checkout.")
    
    def tampil_struk_checkout(self):
        print("\n" + "="*60)
        print("                      PENGINAPAN CHOCO                        ")
        print("             Jl. Coklat Manis No. 5, Surabaya                 ")
        print("                   Telp: (031) 888-9999                       ")
        print("                    STRUK CHECKOUT                            ")
        print("="*60)
        
        print(f"\nNama Tamu         : {self.nama}")
        print(f"No. Telepon       : {self._telepon}")
        print(f"NIK               : {self._nik}")
        
        print("\nDetail kamar yang dipesan:")
        for idx, kamar in enumerate(self.kamar_dipesan, 1):
            print(f" {idx}. Tipe: {kamar['tipe']:<25} Nomor: {kamar['nomor']:<5} Harga/malam: Rp {kamar['harga']:,}")
        
        print(f"\nCheck-in          : {self.waktu_checkin.strftime('%d %B %Y (%H.%M)')}")
        print(f"Check-out Terjadwal: {self.checkout_terjadwal.strftime('%d %B %Y (%H.%M)')}")
        print(f"Check-out Aktual  : {self.waktu_checkout_aktual.strftime('%d %B %Y (%H.%M)')}")
        print(f"Lama Menginap     : {self.lama_menginap} malam")
        
        print("\n----------------- RINCIAN PEMBAYARAN ----------------------")
        subtotal = sum(item['harga'] for item in self.kamar_dipesan) * self.lama_menginap
        print(f"Subtotal Kamar    : Rp {subtotal:,}")
        
        if hasattr(self, 'dp_dibayar'):
            dp_amount = subtotal // 2
            pelunasan = subtotal - dp_amount
            print(f"DP saat Check-in  : Rp {dp_amount:,} ({self.metode_pembayaran})")
            if pelunasan > 0:
                print(f"Pelunasan Checkout: Rp {pelunasan:,} ({getattr(self, 'metode_checkout', self.metode_pembayaran)})")
        else:
            print(f"Pembayaran Lunas  : Rp {subtotal:,} ({self.metode_pembayaran})")
        
        if self.crash > 0:
            print(f"Biaya Keterlambatan: Rp {self.crash:,} ({getattr(self, 'metode_checkout', self.metode_pembayaran)})")
        
        total_final = subtotal + self.crash
        print(f"Total Akhir       : Rp {total_final:,}")
        print("Status Pembayaran : LUNAS")
        print("="*60)
    
    def update_status_checkout(self, nik):
        with open("data_checkin.txt", "r") as file:
            lines = file.readlines()
        
        with open("data_checkin.txt", "w") as file_baru:
            for line in lines:
                data = line.strip().split(" | ")
                if len(data) >= 14 and data[2] == nik and data[13] == "BELUM":
                    data[10] = str(self.crash)
                    data[11] = "LUNAS"
                    data[12] = "0"
                    data[13] = "SUDAH"
                    
                    file_baru.write(" | ".join(data) + "\n")
                    print("Status checkout berhasil diupdate.")
                else:
                    file_baru.write(line)

def main():
    while True:
        print("\n========== PENGINAPAN CHOCO ==========")
        print("1. Check-in")
        print("2. Checkout")
        print("3. Lihat Status Kamar")
        print("4. Keluar")

        pilihan = input("Pilih menu (1/2/3/4): ")
        if pilihan == "1":
            try:
                pemesanan = Pemesanan()
                pemesanan.simpan_data()
                pemesanan.tampil_struk()
            except KeyboardInterrupt:
                print("\nProses dibatalkan.")
            except Exception as e:
                print(f"Terjadi error: {e}")
                
        elif pilihan == "2":
            try:
                checkout_manager = CheckoutManager()
                checkout_manager.checkout_process()
            except KeyboardInterrupt:
                print("\nProses dibatalkan.")
            except Exception as e:
                print(f"Terjadi error: {e}")
                
        elif pilihan == "3":
            try:
                kamar = Kamar()
                kamar.tampil_status_kamar()
            except Exception as e:
                print(f"Terjadi error: {e}")
                
        elif pilihan == "4":
            print("Terima kasih telah menggunakan layanan kami.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()