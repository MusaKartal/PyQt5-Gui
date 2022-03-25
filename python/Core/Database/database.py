import sqlite3
global curs
global conn
#------ profil

conn =sqlite3.connect('veritabani.db')



curs=conn.cursor()
sorgucreat=("CREATE TABLE IF NOT EXISTS Profil(           \
    OKULNO TEXT NOT NULL UNIQUE,                          \
    ISIM TEXT NOT NULL,                                   \
    SOYISIM TEXT NOT NULL,                                \
    ETKINLIKTURU TEXT NOT NULL,                           \
    TELNO TEXT NOT NULL UNIQUE,                           \
    TARIH  TEXT NOT NULL,                                 \
    ACIKLAMA TEXT NOT NULL)")
curs.execute(sorgucreat)
conn.commit()




#-------kayıt sistemi
curs=conn.cursor()
sorgu2creat=("CREATE TABLE IF NOT EXISTS KayitOl(          \
    OKULNO TEXT NOT NULL UNIQUE,                          \
    ISIM TEXT NOT NULL,                                   \
    SOYISIM TEXT NOT NULL,                                \
    TELNO TEXT NOT NULL UNIQUE,                             \
    SIFRE TEXT NOT NULL)")                                 
    
curs.execute(sorgu2creat)
conn.commit()




curs=conn.cursor()
sorgu3creat=("CREATE TABLE IF NOT EXISTS ETKINLIKPANOSU(           \
    OKULNO TEXT NOT NULL UNIQUE,                          \
    ISIM TEXT NOT NULL,                                   \
    SOYISIM TEXT NOT NULL,                                \
    ETKINLIKTURU TEXT NOT NULL,                           \
    TELNO TEXT NOT NULL UNIQUE,                           \
    TARIH  TEXT NOT NULL,                                 \
    ACIKLAMA TEXT NOT NULL)")
curs.execute(sorgu3creat)
conn.commit()