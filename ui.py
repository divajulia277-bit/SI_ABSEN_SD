"""Antarmuka grafis SI ABSEN SD menggunakan Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from services import AttendanceManager

RED = "#B71C1C"
DARK_RED = "#8E0000"
LIGHT_RED = "#FCE8E6"
WHITE = "#FFFFFF"
TEXT = "#292929"

class AttendanceApp:
    """Membuat tampilan dan menghubungkan tombol dengan logika absensi."""

    def __init__(self, root):
        self.root = root
        self.manager = AttendanceManager()
        self.root.title("SI ABSEN SD - Absensi Wali Kelas")
        self.root.geometry("1050x680")
        self.root.minsize(850, 580)
        self.root.configure(bg=LIGHT_RED)
        self._style()
        self._build()
        self.refresh_table()

    def _style(self):
        """Mengatur tema tabel dan tombol."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=29, font=("Arial", 10),
                        background=WHITE, fieldbackground=WHITE)
        style.configure("Treeview.Heading", background=RED, foreground=WHITE,
                        font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#F5B7B1")],
                  foreground=[("selected", TEXT)])

    def _build(self):
        """Menyusun header, form input, pencarian, tabel, dan rekap."""
        header = tk.Frame(self.root, bg=RED, height=95)
        header.pack(fill="x")
        tk.Label(header, text="SI ABSEN SD", bg=RED, fg=WHITE,
                 font=("Arial", 23, "bold")).pack(pady=(15, 2))
        tk.Label(header, text="Sistem Informasi Absensi Siswa - Wali Kelas",
                 bg=RED, fg=WHITE, font=("Arial", 10)).pack()

        body = tk.Frame(self.root, bg=LIGHT_RED, padx=20, pady=14)
        body.pack(fill="both", expand=True)

        form = tk.LabelFrame(body, text=" Input Absensi Siswa ", bg=WHITE,
                             fg=DARK_RED, font=("Arial", 11, "bold"), padx=12, pady=10)
        form.pack(fill="x")
        self.date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.nis_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.class_var = tk.StringVar(value="6")
        self.status_var = tk.StringVar(value="Hadir")

        fields = [
            ("Tanggal (YYYY-MM-DD)", self.date_var, 18),
            ("NIS", self.nis_var, 15),
            ("Nama Siswa", self.name_var, 22),
            ("Kelas", self.class_var, 8)
        ]
        for col, (label, variable, width) in enumerate(fields):
            tk.Label(form, text=label, bg=WHITE, fg=TEXT).grid(
                row=0, column=col, sticky="w", padx=5, pady=(0, 4))
            tk.Entry(form, textvariable=variable, width=width,
                     font=("Arial", 10)).grid(row=1, column=col, padx=5, pady=3)
        tk.Label(form, text="Status", bg=WHITE, fg=TEXT).grid(
            row=0, column=4, sticky="w", padx=5)
        ttk.Combobox(form, textvariable=self.status_var,
                     values=("Hadir", "Izin", "Sakit", "Alpa"),
                     state="readonly", width=10).grid(row=1, column=4, padx=5)
        tk.Button(form, text=" + Simpan Absensi ", command=self.add_record,
                  bg=RED, fg=WHITE, activebackground=DARK_RED,
                  activeforeground=WHITE, relief="flat", padx=8, pady=5).grid(
                      row=1, column=5, padx=8)

        tools = tk.Frame(body, bg=LIGHT_RED)
        tools.pack(fill="x", pady=12)
        tk.Label(tools, text="Cari nama / NIS:", bg=LIGHT_RED,
                 fg=TEXT).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(tools, textvariable=self.search_var, width=25)
        search_entry.pack(side="left", padx=7)
        search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())
        tk.Button(tools, text="Cari", command=self.refresh_table,
                  bg=DARK_RED, fg=WHITE, relief="flat", padx=12).pack(side="left")
        tk.Button(tools, text="Tampilkan Semua", command=self.clear_search,
                  bg=RED, fg=WHITE, relief="flat", padx=10).pack(side="left", padx=6)

        tk.Label(tools, text="Urutkan:", bg=LIGHT_RED, fg=TEXT).pack(side="left", padx=(18, 4))
        self.sort_var = tk.StringVar(value="nama")
        sort_box = ttk.Combobox(tools, textvariable=self.sort_var,
                                values=("tanggal", "nis", "nama", "kelas", "status"),
                                state="readonly", width=12)
        sort_box.pack(side="left")
        sort_box.bind("<<ComboboxSelected>>", lambda event: self.refresh_table())

        table_frame = tk.Frame(body, bg=WHITE)
        table_frame.pack(fill="both", expand=True)
        columns = ("tanggal", "nis", "nama", "kelas", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {"tanggal": "Tanggal", "nis": "NIS", "nama": "Nama Siswa",
                    "kelas": "Kelas", "status": "Keterangan"}
        widths = {"tanggal": 130, "nis": 120, "nama": 300, "kelas": 100, "status": 140}
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col], anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom = tk.Frame(body, bg=LIGHT_RED)
        bottom.pack(fill="x", pady=(10, 0))
        self.summary_label = tk.Label(bottom, text="", bg=LIGHT_RED,
                                      fg=DARK_RED, font=("Arial", 10, "bold"))
        self.summary_label.pack(side="left")
        tk.Button(bottom, text="Hapus Baris Terpilih", command=self.delete_record,
                  bg="#555555", fg=WHITE, relief="flat", padx=10).pack(side="right")

    def add_record(self):
        """Mengambil input form dan menyimpan absensi."""
        try:
            self.manager.add_record(
                self.date_var.get(), self.nis_var.get(), self.name_var.get(),
                self.class_var.get(), self.status_var.get()
            )
            messagebox.showinfo("Berhasil", "Data absensi berhasil disimpan.")
            self.nis_var.set("")
            self.name_var.set("")
            self.refresh_table()
        except (ValueError, OSError) as error:
            messagebox.showerror("Tidak dapat menyimpan", str(error))

    def refresh_table(self):
        """Memperbarui tabel berdasarkan pencarian dan pilihan urutan."""
        for item in self.table.get_children():
            self.table.delete(item)
        rows = self.manager.search(self.search_var.get())
        rows = self.manager.sort_records(rows, self.sort_var.get())
        for row in rows:
            self.table.insert("", "end", values=(
                row["tanggal"], row["nis"], row["nama"], row["kelas"], row["status"]
            ))
        counts = self.manager.summary()
        self.summary_label.config(
            text=f"Total: {len(self.manager.records)}   |   Hadir: {counts['Hadir']}   "
                 f"|   Izin: {counts['Izin']}   |   Sakit: {counts['Sakit']}   "
                 f"|   Alpa: {counts['Alpa']}"
        )

    def clear_search(self):
        """Mengosongkan pencarian dan menampilkan seluruh data."""
        self.search_var.set("")
        self.refresh_table()

    def delete_record(self):
        """Menghapus catatan yang dipilih dari tabel dan file."""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Pilih data", "Pilih baris yang ingin dihapus.")
            return
        values = self.table.item(selected[0], "values")
        target = tuple(values)
        self.manager.records = [
            row for row in self.manager.records
            if (row["tanggal"], row["nis"], row["nama"], row["kelas"], row["status"]) != target
        ]
        try:
            self.manager.storage.save_all(self.manager.records)
            self.refresh_table()
        except OSError as error:
            messagebox.showerror("Gagal menghapus", str(error))
