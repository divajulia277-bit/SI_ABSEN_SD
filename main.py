"""Titik awal aplikasi SI ABSEN SD."""
import tkinter as tk
from ui import AttendanceApp

def main():
    """Membuat jendela utama dan menjalankan aplikasi."""
    root = tk.Tk()
    AttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
