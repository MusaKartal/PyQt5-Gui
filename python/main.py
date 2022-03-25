from Core.Classlar.EventTable import Ui_MainWindow_EVENT
from Core.Classlar.Profile import Ui_MainWindow_PROFILE
from Core.Classlar.Register import Ui_MainWindow_REGISTER
from Core.Classlar.MainPage import Ui_MainWindow_MAINPAGE
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Core.Database.database import *

#-----anasayfa
app_main_page=QApplication(sys.argv)
window_main_page=QMainWindow()
ui= Ui_MainWindow_MAINPAGE()
ui.setupUi(window_main_page)
window_main_page.show()
#----kayıt ekranı
window_register=QMainWindow()
ui2=Ui_MainWindow_REGISTER()
ui2.setupUi(window_register)
#----profil
window_profile=QMainWindow()
ui3=Ui_MainWindow_PROFILE()
ui3.setupUi(window_profile)
#------etkinlik panosu
window_event=QMainWindow()
ui4= Ui_MainWindow_EVENT()
ui4.setupUi(window_event)

def CloseWindow():
    if window_main_page:
       window_main_page.hide()
    if window_register:
        window_main_page.hide()
    if window_profile:
        window_main_page.hide()
    if window_event:
       window_main_page.hide()
    else:
        print("error")
def EventTable():
    window_event.show()
    CloseWindow()
def ProfileWindow():
    window_profile.show()
    CloseWindow()
def RegisterWindow():
    window_register.show() 
    CloseWindow()
#------ anasayfa giris
def Singup():
    try:
        girisokulno= ui.lineEdit_OgrncNo.text()
        girissifre= ui.lineEdit_Sfre.text()
        curs.execute("SELECT * FROM KayitOl WHERE  OKULNO =? AND SIFRE =?",\
        (girisokulno,girissifre))
        results = curs.fetchone()     
        if results :
            ProfileWindow()
            CloseWindow()
        else:
            QMessageBox.about(window_main_page,"HATA"," ÖĞRENCİ NO VEYA ŞİFRE HATALI ?")
    except Exception as HATA:
        ui.statusbar.showMessage("Hata var "+str(HATA))
#-----kayıt olma ekranında  verileri veritabanına yazan yer
def Register():
    cevap=QMessageBox.question(window_register,"KAYIT OL","Kayıt olmak  istediğinize emin misiniz ?",\
        QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes :    
        try:
            okul_no = ui2.lE_OGNCNO.text()
            isim = ui2.lE_ISIM.text()
            soyisim = ui2.lE_Soisim.text()
            tel_no = ui2.lE_TelNo.text()
            sifre = ui2.lE_Sifre.text()
            curs.execute("INSERT INTO KayitOl \
                        (OKULNO,ISIM,SOYISIM,TELNO,SIFRE)\
                            VALUES (?,?,?,?,?)",\
                           (okul_no,isim,soyisim,tel_no,sifre ))   
            conn.commit() 
            results = curs.fetchall()
            if results :
                QMessageBox.about(window_register,"KAYIT"," BAŞARILI BİR ŞEKİLDE KAYIT OLUNDU. ")
            else:
                QMessageBox.about(window_register,"HATA"," BOŞ BIRAKMAYINIZ.")
        except Exception as Hata:
             ui.statusbar.showMessage("Hata var "+str(Hata))
    else:
        ui.statusbar.showMessage("Kaydetme işlemi iptal edildi ",10000)
#--------profil ekranında ki fonksiyonları kullanma
# ------ kaydet
def INSERT():
  # curs.execute("SELECT * FROM KayitOl " )
    lnokulno= 1
    lnisim=1
    lnsoyisim=1
    lnetkinliktürü=ui3.cB_EtkinlikTur.currentText()
    lnetelno=1
    lnetkinlikgünü= ui3.lE_EtkinikGUNU.text()
    lneaciklama=ui3.lineEdit.text()

    cevap=QMessageBox.question(window_profile,"KAYDET","kaydetmek istediğinize emin misiniz ?",\
        QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes :    
        try:
            curs.execute("INSERT INTO Profil  \
                (OKULNO,ISIM,SOYISIM,ETKINLIKTURU,TELNO,TARIH,ACIKLAMA)\
                    VALUES (?,?,?,?,?,?,?)",\
                   ( lnokulno,lnisim,lnsoyisim,lnetkinliktürü,lnetelno,lnetkinlikgünü,lneaciklama ))   
            conn.commit() 
        except Exception:
            ui3.statusbar.showMessage("Boş bırakmayın ",10000) 
    else:
        ui3.statusbar.showMessage("Kaydetme işlemi iptal edildi ",10000)


def LIST():
    ui3.tableWidget_TABLO.clear()
    ui3.tableWidget_TABLO.setHorizontalHeaderLabels(("OKULNO","ISIM","SOYISIM","ETKINLIK TURU","TEL NO","TARIH","ACIKLAMA"))
    ui3.tableWidget_TABLO.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    curs.execute("SELECT * FROM Profil ")
    for satirIndeks, satirveri in enumerate(curs):
        for sutunIndeks,sutunveri in enumerate(satirveri):
            ui3.tableWidget_TABLO.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunveri)))
LIST()
#------sil
def DELETE():
    cevap=QMessageBox.question(window_profile,"KAYIT SİL","Kaydı silmek istediğinize emin misiniz ?",\
        QMessageBox.Yes | QMessageBox.No)

    if cevap == QMessageBox.Yes :
        secili=ui3.tableWidget_TABLO.selectedItems()  
        silinecek=secili[0].text()
        try:
            curs.execute("DELETE FROM Profil WHERE OKULNO ='%s'"%(silinecek))
            conn.commit()
            LIST()
            ui3.statusbar.showMessage("Silme işlemi tamamlandı ",10000)  
        except Exception as Hata:
            ui3.statusbar.showMessage("Hata var "+str(Hata))
    else:
        ui3.statusbar.showMessage("Silme işlemi iptal edildi ",10000)  
def UPDATE():
    cevap=QMessageBox.question(window_profile,"KAYIT GÜNCELLE","Kaydı güncellemek istediğinize emin misiniz ?",\
        QMessageBox.Yes | QMessageBox.No)    
    if cevap == QMessageBox.Yes:
        try:
            secili=ui3.tableWidget_TABLO.selectedItems()
            if secili:
                lnokulno=ui3.lE_OkulNO.text()
                lnisim=ui3.lE_ISIM.text()
                lnsoyisim=ui3.lE_Soyisim.text()
                lnetkinliktürü=ui3.cB_EtkinlikTur.currentText()
                lnetelno=ui3.lE_TelNO.text()
                lnetkinlikgünü= ui3.lE_EtkinikGUNU.text()
                lneaciklama=ui3.lineEdit.text()
            
                curs.execute("UPDATE Profil SET OKULNO=?,ISIM=?,SOYISIM=?,ETKINLIKTURU=?,\
                TELNO=?,TARIH=?,ACIKLAMA=? ",\
                (lnokulno,lnisim,lnsoyisim,lnetkinliktürü,lnetelno,lnetkinlikgünü,lneaciklama))
                conn.commit()
                LIST()
            else:
                ui3.statusbar.showMessage("Lütfen bir alan seç" )
        except Exception as Hata:
            ui3.statusbar.showMessage("hata meyadana geldi" +str(Hata))
    else:
        ui3.statusbar.showMessage("Güncelleme iptal edildi",10000)
def event_table_list():
    ui4.tableWidget_TABLO.clear()
    ui4.tableWidget_TABLO.setHorizontalHeaderLabels(("OKULNO","ISIM","SOYISIM","ETKINLIK TURU","TEL NO","TARIH","ACIKLAMA"))
    ui4.tableWidget_TABLO.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    curs.execute("SELECT * FROM ETKINLIKPANOSU ")
    for satirIndeks, satirveri in enumerate(curs):
        for sutunIndeks,sutunveri in enumerate(satirveri):
            ui4.tableWidget_TABLO.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunveri)))

event_table_list()
def event_table_add(): 
    cevap=QMessageBox.question(window_profile,"KAYDET","kaydetmek istediğinize emin misiniz ?",\
        QMessageBox.Yes | QMessageBox.No)

    if cevap == QMessageBox.Yes :    
        try:
            secili=ui3.tableWidget_TABLO.selectedItems()
            if secili:
                eklenecek1=secili[0].text()
                eklenecek2=secili[1].text()
                eklenecek3=secili[2].text()
                eklenecek4=secili[3].text()
                eklenecek5=secili[4].text()
                eklenecek6=secili[5].text()
                eklenecek7=secili[6].text()

                curs.execute("INSERT INTO ETKINLIKPANOSU \
                    (OKULNO,ISIM,SOYISIM,ETKINLIKTURU,TELNO,TARIH,ACIKLAMA)\
                        VALUES (?,?,?,?,?,?,?)",\
                       ( eklenecek1,eklenecek2,eklenecek3,eklenecek4,eklenecek5,eklenecek6,eklenecek7 ))   
                conn.commit() 
                event_table_list()
            else:
                ui3.statusbar.showMessage("Lütfen  kaydetmek istediğiniz alani seçin ",10000)
        except Exception:
            ui3.statusbar.showMessage("Daha önce kayit edilmiş  ",10000) 
    else:
        ui3.statusbar.showMessage("Kaydetme işlemi iptal edildi ",10000)
#----------butonlar
#anasayfa butonları
ui.pushButton_Kaydol.clicked.connect(RegisterWindow)
ui.pushButton_Giris.clicked.connect(Singup)
ui.pushButton_EtkinlikPanosu.clicked.connect(EventTable)
#ui.pushButton_SfreUnuttum.clicked.connect()
#kayıtolma butonları
ui2.pushButton_KAYDOL.clicked.connect(Register)
#profil  butonları
ui3.pushButton_KAYDET.clicked.connect(INSERT)
ui3.pushButton_KAYDET.clicked.connect(LIST)
ui3.pushButton_GUNCELLE.clicked.connect(UPDATE)
ui3.pushButton_SIL.clicked.connect(DELETE)
ui3.pushButton_AnaPanoyaGonder.clicked.connect(event_table_add)
ui3.pushButton_AnaPanoyaGonder.clicked.connect(event_table_list)

sys.exit(app_main_page.exec_())