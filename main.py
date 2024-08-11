from ast import Index
import enum
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from panel import *
import sqlite3

# Arayüz İşlemleri

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()

# Veritabanı İşlemleri

connect = sqlite3.connect("kayit.db")
cursor = connect.cursor()
connect.commit()

table = cursor.execute("Create Table if Not Exists Kayit(Ad text, Soyad text, Sirket text)")
connect.commit()

ui.liste.setHorizontalHeaderLabels(("Ad", "Soyad", "Şirket"))

# Fonksiyonlar

def kayit_ekle():
    Ad = ui.ad_ln.text()
    Soyad = ui.soyad_ln.text()
    Sirket = ui.sirket_combo.currentText()

    try:
        add = "INSERT INTO Kayit(Ad, Soyad, Sirket) VALUES (?, ?, ?)"
        cursor.execute(add, (Ad, Soyad, Sirket))
        connect.commit()
        print("Kayıt Eklendi")
        ui.statusbar.showMessage("Kayıt Eklendi", 10000)
        kayit_listele()
    except Exception as e:
        print(f"Kayıt Eklenemedi: {e}")
        ui.statusbar.showMessage("Kayıt Eklenemedi", 10000)

def kayit_listele():
    ui.liste.clear()
    ui.liste.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.liste.setHorizontalHeaderLabels(("Ad", "Soyad", "Şirket"))
    sorgu = "SELECT * FROM Kayit"
    cursor.execute(sorgu)

    for indexSatir, kayitNumarasi in enumerate(cursor):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.liste.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))

def kayit_sil():
    delete_message = QMessageBox.question(window, "Silme Onayı", "Silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)

    if delete_message == QMessageBox.Yes:
        secilen_kayit = ui.liste.selectedItems()
        
        if not secilen_kayit:
            QMessageBox.warning(window, "Uyarı", "Silmek için bir kayıt seçmelisiniz.")
            return
        
        try:
            silinecek_kayit = secilen_kayit[0].text()
            sorgu = "DELETE FROM Kayit WHERE Ad = ?"
            cursor.execute(sorgu, (silinecek_kayit,))
            connect.commit()
            ui.statusbar.showMessage("Kayıt Silindi", 10000)
            kayit_listele()
        except Exception as e:
            print(f"Kayıt Silinemedi: {e}")
            ui.statusbar.showMessage("Kayıt Silinemedi", 10000)
    else:
        ui.statusbar.showMessage("İşlem İptal Edildi", 10000)

def sirkete_gore_listele():
    listelenecek_sirket = ui.filtre_combo.currentText()
    sorgu = "SELECT * FROM Kayit WHERE Sirket = ?"
    cursor.execute(sorgu, (listelenecek_sirket,))
    ui.liste.clear()
    ui.liste.setHorizontalHeaderLabels(("Ad", "Soyad", "Şirket"))
    for indexSatir, kayitNumarasi in enumerate(cursor):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.liste.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))

# Butonlar

ui.ekle_btn.clicked.connect(kayit_ekle)
ui.sil_btn.clicked.connect(kayit_sil)
ui.filtren_btn.clicked.connect(sirkete_gore_listele)

kayit_listele()
sys.exit(app.exec_())
