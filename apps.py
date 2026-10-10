import sys
import math

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)

from test1 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Memanggil tampilan dari Qt Designer
        self.setupUi(self)

        self.setWindowTitle("Kalkulator")
        self.kalkulator.setCurrentIndex(0)

        # Variabel perhitungan
        self.angka1 = 0
        self.operator = ""
        self.input_baru = True

        # Layout vertikal untuk display dan tombol
        layout_utama = QVBoxLayout(self.tab_3)
        layout_utama.setContentsMargins(6, 6, 6, 6)
        layout_utama.setSpacing(4)

        # Layout horizontal untuk display
        layout_display = QHBoxLayout()
        layout_display.setContentsMargins(0, 0, 0, 0)
        layout_display.addWidget(self.display)

        # Layout horizontal untuk area tombol
        layout_tombol = QHBoxLayout()
        layout_tombol.setContentsMargins(0, 0, 0, 0)
        layout_tombol.addWidget(self.widget)

        # Menggabungkan layout
        layout_utama.addLayout(layout_display)
        layout_utama.addLayout(layout_tombol, 1)

        # Agar ukuran mengikuti jendela
        self.display.setMinimumHeight(35)
        self.display.setReadOnly(True)

        self.widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Menghubungkan tombol angka
        self.btn_0.clicked.connect(
            lambda: self.input_angka("0")
        )
        self.btn_1.clicked.connect(
            lambda: self.input_angka("1")
        )
        self.btn_2.clicked.connect(
            lambda: self.input_angka("2")
        )
        self.btn_3.clicked.connect(
            lambda: self.input_angka("3")
        )
        self.btn_4.clicked.connect(
            lambda: self.input_angka("4")
        )
        self.btn_5.clicked.connect(
            lambda: self.input_angka("5")
        )
        self.btn_6.clicked.connect(
            lambda: self.input_angka("6")
        )

        # Tombol hasil dan Clear All
        self.btn_hasil.clicked.connect(self.hitung)
        self.btn_c.clicked.connect(self.clear)

        # Membuat menu menggunakan tanda &
        self.menu_operation.setTitle("&Operation")

        self.action_tambah.setText("&Tambah")
        self.action_kurang.setText("Ku&rang")
        self.action_kali.setText("Ka&li")
        self.action_bagi.setText("&Bagi")
        self.action_kuadrat.setText("K&uadrat")
        self.action_invers.setText("I&nvers")
        self.action_clear.setText("&Clear")

        # Menambahkan aksi akar kuadrat
        self.action_akar = QAction("A&kar", self)
        self.menu_operation.addAction(self.action_akar)

        # Menghubungkan menu dengan operasi
        self.action_tambah.triggered.connect(
            lambda: self.pilih_operator("+")
        )
        self.action_kurang.triggered.connect(
            lambda: self.pilih_operator("-")
        )
        self.action_kali.triggered.connect(
            lambda: self.pilih_operator("*")
        )
        self.action_bagi.triggered.connect(
            lambda: self.pilih_operator("/")
        )

        self.action_kuadrat.triggered.connect(self.kuadrat)
        self.action_invers.triggered.connect(self.invers)
        self.action_akar.triggered.connect(self.akar)
        self.action_clear.triggered.connect(self.clear)

    # Memasukkan angka melalui tombol mouse
    def input_angka(self, angka):
        if self.input_baru:
            self.display.setText(angka)
            self.input_baru = False
        else:
            teks = self.display.text()

            if teks == "0" or teks == "Error":
                self.display.setText(angka)
            else:
                self.display.setText(teks + angka)

    # Memilih operasi matematika
    def pilih_operator(self, op):
        teks = self.display.text()

        if teks == "" or teks == "Error":
            return

        try:
            angka = float(teks)
        except ValueError:
            return

        if self.operator != "" and not self.input_baru:
            if not self.hitung():
                return

            angka = float(self.display.text())

        self.angka1 = angka
        self.operator = op
        self.input_baru = True

    # Menghitung tambah, kurang, kali, dan bagi
    def hitung(self):
        if self.operator == "":
            return True

        try:
            angka2 = float(self.display.text())

            if self.operator == "+":
                hasil = self.angka1 + angka2

            elif self.operator == "-":
                hasil = self.angka1 - angka2

            elif self.operator == "*":
                hasil = self.angka1 * angka2

            elif self.operator == "/":
                if angka2 == 0:
                    self.display.setText("Error")
                    self.reset()
                    self.input_baru = True
                    return False

                hasil = self.angka1 / angka2

            else:
                return False

            self.tampil_hasil(hasil)
            self.reset()
            self.input_baru = True
            return True

        except (ValueError, OverflowError):
            self.display.setText("Error")
            self.reset()
            self.input_baru = True
            return False

    # Menghitung kuadrat: x * x
    def kuadrat(self):
        try:
            angka = float(self.display.text())
            hasil = angka * angka

            self.tampil_hasil(hasil)
            self.reset()
            self.input_baru = True

        except (ValueError, OverflowError):
            self.display.setText("Error")
            self.reset()
            self.input_baru = True

    # Menghitung invers: 1 / x
    def invers(self):
        try:
            angka = float(self.display.text())

            if angka == 0:
                self.display.setText("Error")
            else:
                hasil = 1 / angka
                self.tampil_hasil(hasil)

            self.reset()
            self.input_baru = True

        except (ValueError, OverflowError):
            self.display.setText("Error")
            self.reset()
            self.input_baru = True

    # Menghitung akar kuadrat
    def akar(self):
        try:
            angka = float(self.display.text())

            if angka < 0:
                self.display.setText("Error")
            else:
                hasil = math.sqrt(angka)
                self.tampil_hasil(hasil)

            self.reset()
            self.input_baru = True

        except (ValueError, OverflowError):
            self.display.setText("Error")
            self.reset()
            self.input_baru = True

    # Menghapus semua input
    def clear(self):
        self.display.clear()
        self.reset()
        self.input_baru = True

    # Mengatur ulang variabel operasi
    def reset(self):
        self.angka1 = 0
        self.operator = ""

    # Menampilkan hasil
    def tampil_hasil(self, hasil):
        if hasil == 0:
            self.display.setText("0")
        elif hasil.is_integer():
            self.display.setText(str(int(hasil)))
        else:
            self.display.setText(f"{hasil:.10g}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())