
import sys
import math

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)

from kalulator import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("Kalkulator")
        self.kalkulator.setCurrentIndex(0)

        # Variabel perhitungan
        self.angka1 = 0.0
        self.operator = ""
        self.input_baru = True

        # Mengatur layout tab kalkulator
        layout_utama = QVBoxLayout(self.tab_3)
        layout_utama.setContentsMargins(6, 6, 6, 6)
        layout_utama.setSpacing(4)

        layout_display = QHBoxLayout()
        layout_display.addWidget(self.display)

        layout_tombol = QHBoxLayout()
        layout_tombol.addWidget(self.layoutWidget)

        layout_utama.addLayout(layout_display)
        layout_utama.addLayout(layout_tombol, 1)

        self.display.setMinimumHeight(35)
        self.display.setReadOnly(True)

        self.layoutWidget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Menghubungkan tombol angka
        tombol_angka = {
            self.btn_0: "0",
            self.btn_1: "1",
            self.btn_2: "2",
            self.btn_3: "3",
            self.btn_4: "4",
            self.btn_5: "5",
            self.btn_6: "6",
        }

        for tombol, angka in tombol_angka.items():
            tombol.clicked.connect(
                lambda checked=False, a=angka: self.input_angka(a)
            )

        # Menghubungkan tombol operasi pada tampilan
        self.pushButton.clicked.connect(
            lambda: self.pilih_operator("+")
        )
        self.pushButton_3.clicked.connect(
            lambda: self.pilih_operator("-")
        )
        self.pushButton_5.clicked.connect(
            lambda: self.pilih_operator("*")
        )
        self.pushButton_4.clicked.connect(
            lambda: self.pilih_operator("/")
        )

        self.pushButton_6.clicked.connect(self.kuadrat)
        self.pushButton_7.clicked.connect(self.invers)
        self.pushButton_8.clicked.connect(self.akar)

        self.btn_hasil.clicked.connect(self.hitung)
        self.btn_c.clicked.connect(self.clear)

        # Mengatur menu operasi
        self.menu_operation.setTitle("&Operation")

        self.action_tambah.setText("&Tambah")
        self.action_kurang.setText("Ku&rang")
        self.action_kali.setText("Ka&li")
        self.action_bagi.setText("&Bagi")
        self.action_kuadrat.setText("K&uadrat")
        self.action_invers.setText("I&nvers")
        self.action_clear.setText("&Clear")
        self.actionakar.setText("&Akar")

        
        # Mengatur shortcut Alt pada menu operasi
        self.action_tambah.setText("&Tambah")
        self.action_tambah.setShortcut("Alt+T")

        self.action_kurang.setText("&Kurang")
        self.action_kurang.setShortcut("Alt+K")

        self.action_kali.setText("K&ali")
        self.action_kali.setShortcut("Alt+A")

        self.action_bagi.setText("&Bagi")
        self.action_bagi.setShortcut("Alt+B")

        self.action_kuadrat.setText("K&uadrat")
        self.action_kuadrat.setShortcut("Alt+U")

        self.action_invers.setText("&Invers")
        self.action_invers.setShortcut("Alt+I")

        self.actionakar.setText("&Akar")
        self.actionakar.setShortcut("Alt+R")

        self.action_clear.setText("&Clear")
        self.action_clear.setShortcut("Alt+C")


        

        # Menghubungkan menu operasi
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
        self.actionakar.triggered.connect(self.akar)
        self.action_clear.triggered.connect(self.clear)

    # Memasukkan angka
    def input_angka(self, angka):
        if self.input_baru:
            self.display.setText(angka)
            self.input_baru = False
        else:
            teks = self.display.text()

            if teks in ("0", "Error"):
                self.display.setText(angka)
            else:
                self.display.setText(teks + angka)

    # Memilih operator
    def pilih_operator(self, op):
        teks = self.display.text()

        if not teks or teks == "Error":
            return

        try:
            angka = float(teks)
        except ValueError:
            return

        # Menghitung operasi sebelumnya jika ada
        if self.operator and not self.input_baru:
            if not self.hitung():
                return

            angka = float(self.display.text())

        self.angka1 = angka
        self.operator = op
        self.input_baru = True

    # Menghitung operasi dasar
    def hitung(self):
        if not self.operator:
            return True

        teks = self.display.text()

        if not teks or teks == "Error":
            return False

        try:
            angka2 = float(teks)

            if self.operator == "+":
                hasil = self.angka1 + angka2
            elif self.operator == "-":
                hasil = self.angka1 - angka2
            elif self.operator == "*":
                hasil = self.angka1 * angka2
            elif self.operator == "/":
                if angka2 == 0:
                    raise ZeroDivisionError
                hasil = self.angka1 / angka2
            else:
                return False

            self.tampil_hasil(hasil)
            self.reset()
            self.input_baru = True
            return True

        except (ValueError, OverflowError, ZeroDivisionError):
            self.display.setText("Error")
            self.reset()
            self.input_baru = True
            return False

    # Menghitung kuadrat
    def kuadrat(self):
        try:
            angka = float(self.display.text())
            self.tampil_hasil(angka ** 2)

        except (ValueError, OverflowError):
            self.display.setText("Error")

        self.reset()
        self.input_baru = True

    # Menghitung invers: 1 / x
    def invers(self):
        try:
            angka = float(self.display.text())

            if angka == 0:
                raise ZeroDivisionError

            self.tampil_hasil(1 / angka)

        except (ValueError, OverflowError, ZeroDivisionError):
            self.display.setText("Error")

        self.reset()
        self.input_baru = True

    # Menghitung akar kuadrat
    def akar(self):
        try:
            angka = float(self.display.text())

            if angka < 0:
                raise ValueError

            self.tampil_hasil(math.sqrt(angka))

        except (ValueError, OverflowError):
            self.display.setText("Error")

        self.reset()
        self.input_baru = True

    # Membersihkan layar
    def clear(self):
        self.display.clear()
        self.reset()
        self.input_baru = True

    # Mereset variabel operasi
    def reset(self):
        self.angka1 = 0.0
        self.operator = ""

    # Menampilkan hasil
    def tampil_hasil(self, hasil):
        hasil = float(hasil)

        if not math.isfinite(hasil):
            self.display.setText("Error")
        elif hasil == 0:
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
