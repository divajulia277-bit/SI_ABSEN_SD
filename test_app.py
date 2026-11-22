"""Pengujian unit untuk logika SI ABSEN SD."""
import unittest
import tempfile
from pathlib import Path
from storage import AttendanceStorage
from services import AttendanceManager

class TestAttendanceManager(unittest.TestCase):
    """Menguji penyimpanan, validasi, pencarian, dan pengurutan."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = AttendanceStorage(Path(self.temp_dir.name) / "test.csv")
        self.manager = AttendanceManager(self.storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def add_sample(self, nis="001", name="Alya", status="Hadir", day="2026-11-22"):
        return self.manager.add_record(day, nis, name, "6", status)

    def test_add_and_save_data(self):
        self.add_sample()
        self.assertEqual(len(self.storage.load()), 1)

    def test_search_by_name(self):
        self.add_sample()
        self.assertEqual(len(self.manager.search("aly")), 1)

    def test_search_by_nis(self):
        self.add_sample()
        self.assertEqual(len(self.manager.search("001")), 1)

    def test_sort_by_name(self):
        self.add_sample("002", "Citra")
        self.add_sample("001", "Alya")
        result = self.manager.sort_records(key="nama")
        self.assertEqual(result[0]["nama"], "Alya")

    def test_reject_duplicate_attendance(self):
        self.add_sample()
        with self.assertRaises(ValueError):
            self.add_sample()

    def test_reject_empty_name(self):
        with self.assertRaises(ValueError):
            self.add_sample(name="")

if __name__ == "__main__":
    unittest.main()
