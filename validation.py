"""Fungsi validasi input absensi."""

VALID_STATUSES = ("Hadir", "Izin", "Sakit", "Alpa")

def validate_attendance(name, student_id, date, status):
    """Memastikan seluruh kolom wajib diisi dan status valid."""
    if not name.strip():
        raise ValueError("Nama siswa wajib diisi.")
    if not student_id.strip():
        raise ValueError("NIS wajib diisi.")
    if not date.strip():
        raise ValueError("Tanggal wajib diisi.")
    if status not in VALID_STATUSES:
        raise ValueError("Status absensi tidak valid.")
    return True
