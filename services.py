"""Logika pengolahan, pencarian, pengurutan, dan rekap absensi."""
from storage import AttendanceStorage
from validation import validate_attendance

class AttendanceManager:
    """Mengelola data absensi dan berkomunikasi dengan penyimpanan."""

    def __init__(self, storage=None):
        self.storage = storage or AttendanceStorage()
        self.records = self.storage.load()

    def add_record(self, date, student_id, name, classroom, status):
        """Memvalidasi dan menambahkan data absensi."""
        validate_attendance(name, student_id, date, status)
        record = {
            "tanggal": date.strip(),
            "nis": student_id.strip(),
            "nama": name.strip(),
            "kelas": classroom.strip(),
            "status": status
        }
        # Satu siswa hanya boleh memiliki satu catatan per tanggal.
        for old in self.records:
            if old["nis"] == record["nis"] and old["tanggal"] == record["tanggal"]:
                raise ValueError("Absensi siswa tersebut pada tanggal ini sudah ada.")
        self.records.append(record)
        self.storage.save_all(self.records)
        return record

    def search(self, keyword="", **filters):
        """Mencari berdasarkan nama/NIS dan menerima filter tambahan."""
        keyword = keyword.lower().strip()
        result = [
            row for row in self.records
            if keyword in row["nama"].lower() or keyword in row["nis"].lower()
        ]
        for key, value in filters.items():
            if value:
                result = [row for row in result if row.get(key) == value]
        return result

    def sort_records(self, records=None, key="nama", reverse=False):
        """Mengurutkan data dengan key fungsi; lambda menentukan kolom."""
        data = list(self.records if records is None else records)
        allowed = ("tanggal", "nis", "nama", "kelas", "status")
        if key not in allowed:
            raise ValueError("Kolom pengurutan tidak dikenal.")
        return sorted(data, key=lambda row: row[key].lower(), reverse=reverse)

    def summary(self, *statuses):
        """Menghitung jumlah status; *args dapat berisi beberapa status."""
        selected = statuses or ("Hadir", "Izin", "Sakit", "Alpa")
        return {status: sum(1 for row in self.records if row["status"] == status)
                for status in selected}
