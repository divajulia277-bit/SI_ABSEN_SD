# SI ABSEN SD

Aplikasi desktop pencatatan absensi siswa untuk wali kelas SD.
Dibuat dengan Python Tkinter dan penyimpanan CSV (tanpa database).

## Cara menjalankan
1. Install Python 3.10 atau lebih baru.
2. Ekstrak folder proyek.
3. Buka terminal pada folder `SI_ABSEN_SD`.
4. Jalankan: `python main.py`

Tkinter biasanya sudah tersedia bersama instalasi Python.

## Cara menggunakan
1. Isi tanggal dengan format YYYY-MM-DD.
2. Isi NIS, nama siswa, kelas, dan pilih status.
3. Klik Simpan Absensi.
4. Gunakan kotak pencarian untuk mencari nama/NIS.
5. Pilih kolom pada menu Urutkan untuk mengurutkan tabel.
6. Pilih baris lalu klik Hapus Baris Terpilih jika perlu.

Data tersimpan otomatis pada `data_absensi.csv` di folder proyek.

## Menjalankan unit test
Jalankan: `python -m unittest -v`

## Isi folder
- main.py: titik awal aplikasi.
- ui.py: tampilan Tkinter.
- services.py: logika absensi, pencarian, pengurutan, rekap.
- storage.py: baca/tulis CSV menggunakan `with open()`.
- validation.py: validasi input.
- test_app.py: enam unit test.
- data_absensi.csv: dibuat otomatis ketika data pertama disimpan.

## Catatan
Isi data siswa melalui form setiap kali mencatat kehadiran. Satu NIS hanya boleh
memiliki satu catatan pada tanggal yang sama. Pastikan file CSV tidak dihapus
agar riwayat absensi tetap tersimpan.
