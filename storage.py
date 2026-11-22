"""Modul untuk membaca dan menyimpan data absensi dalam CSV."""
import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data_absensi.csv")
FIELDNAMES = ["tanggal", "nis", "nama", "kelas", "status"]

class AttendanceStorage:
    """Menangani seluruh operasi baca dan tulis file CSV."""

    def __init__(self, filename=DATA_FILE):
        self.filename = Path(filename)

    def load(self):
        """Membaca data; mengembalikan list kosong jika file belum ada."""
        try:
            with open(self.filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != FIELDNAMES:
                    raise ValueError("Format file CSV tidak sesuai.")
                return list(reader)
        except FileNotFoundError:
            return []
        except (csv.Error, UnicodeDecodeError) as error:
            raise ValueError(f"File data rusak atau tidak dapat dibaca: {error}")

    def save_all(self, records):
        """Menulis ulang seluruh data absensi ke file CSV."""
        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)

    def append(self, record):
        """Menambahkan satu data baru tanpa menghapus data sebelumnya."""
        exists = self.filename.exists()
        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            if not exists or self.filename.stat().st_size == 0:
                writer.writeheader()
            writer.writerow(record)
