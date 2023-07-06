import os
import sqlite3
import datetime
import csv

# Pobieranie ścieżki do katalogu bieżącego
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'Base.db')

# Tworzenie połączenia z bazą danych
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tworzenie tabeli Samochod jesli nie istnieje w bazie Offline
c.execute('''
    CREATE TABLE IF NOT EXISTS Samochod (
        ID INTEGER PRIMARY KEY,
        Marka TEXT,
        Model TEXT,
        RokProdukcji INTEGER,
        Silnik TEXT,
        TypPaliwa TEXT,
        TypNadwozia TEXT,
        MasaPojazdu REAL
    )
''')

# Tworzenie tabeli Pomiary jesli nie istnieje w bazie Offline
c.execute('''
    CREATE TABLE IF NOT EXISTS Pomiary (
        ID INTEGER PRIMARY KEY,
        Data TEXT,
        Godzina TEXT,
        SzerokoscGeograficzna REAL,
        DlugoscGeograficzna REAL,
        Silnik TEXT,
        Moc REAL,
        MomentObrotowy REAL,
        CO REAL,
        HC REAL,
        NO REAL,
        PM REAL,
        SamochodID INTEGER,
        FOREIGN KEY (SamochodID) REFERENCES Samochod (ID)
    )
''')

# Dodawanie samochodu do bazy danych aplikacji offline
def dodaj_samochod(marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu):
    c.execute('''
        INSERT INTO Samochod (Marka, Model, RokProdukcji, Silnik, TypPaliwa, TypNadwozia, MasaPojazdu)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu))

    conn.commit()
    print('=============\nSamochód dodany do bazy danych (Offline).=============\n')
        
def dodaj_pomiar(szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, samochod_id):
    data = datetime.date.today()
    godzina = datetime.datetime.now().strftime('%H:%M:%S')

    c.execute('''
        INSERT INTO Pomiary (Data, Godzina, SzerokoscGeograficzna, DlugoscGeograficzna, Silnik, Moc, MomentObrotowy, CO, HC, NO, PM, SamochodID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data, godzina, szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, samochod_id))

    conn.commit()
    print('=============\nPomiar dodany do bazy danych (Offline).=============\n')
    
def zapisz_tabele_do_csv():
    # Zapis tabeli Samochod
    c.execute('SELECT * FROM Samochod')
    samochody = c.fetchall()

    if not samochody:
        print('=============\nBrak danych w tabeli Samochod.=============\n')
    else:
        nazwa_pliku_samochody = 'samochody.csv'
        naglowki_samochody = [opis[0] for opis in c.description]

        with open(nazwa_pliku_samochody, 'w', newline='') as plik_csv:
            writer = csv.writer(plik_csv)
            writer.writerow(naglowki_samochody)
            writer.writerows(samochody)

        print(f'Dane z tabeli Samochod zostały zapisane w pliku {nazwa_pliku_samochody}.')

    # Zapis tabeli Pomiary
    c.execute('''
        SELECT P.Data, P.Godzina, S.Marka, S.Model, P.Silnik, P.Moc, P.MomentObrotowy, P.CO, P.HC, P.NO, P.PM
        FROM Pomiary AS P
        JOIN Samochod AS S ON P.SamochodID = S.ID
    ''')
    pomiary = c.fetchall()

    if not pomiary:
        print('=============\nBrak danych w tabeli Pomiary.=============\n')
    else:
        nazwa_pliku_pomiary = 'pomiary.csv'
        naglowki_pomiary = [opis[0] for opis in c.description]

        with open(nazwa_pliku_pomiary, 'w', newline='') as plik_csv:
            writer = csv.writer(plik_csv)
            writer.writerow(naglowki_pomiary)
            writer.writerows(pomiary)

        print(f'=============\nDane z tabeli Pomiary zostały zapisane w pliku {nazwa_pliku_pomiary}.=============\n')

def interfejs():
    while True:
        opcja = input('Wybierz opcję:\n1. Dodaj samochód\n2. Dodaj pomiar\n3. <Zapisz do .csv>\n4. Wyjscie\n')
        
        if opcja == '1':
            marka = input('Podaj markę samochodu: ')
            model = input('Podaj model samochodu: ')
            rok_produkcji = int(input('Podaj rok produkcji samochodu: '))
            silnik = input('Podaj litraż silnika samochodu: ')
            typ_paliwa = input('Podaj typ paliwa samochodu: ')
            typ_nadwozia = input('Podaj typ nadwozia samochodu: ')
            masa_pojazdu = float(input('Podaj masę pojazdu samochodu[kg]: '))

            dodaj_samochod(marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu)
        
        elif opcja == '2':
            szerokosc_geograficzna = float(input('Podaj szerokość geograficzną: '))
            dlugosc_geograficzna = float(input('Podaj długość geograficzną: '))
            silnik = input('Podaj typ paliwa: ')
            moc = float(input('Podaj moc[hp]: '))
            moment_obrotowy = float(input('Podaj moment obrotowy[nm]: '))
            co = float(input('Podaj wartość CO: '))
            hc = float(input('Podaj wartość HC (jeśli brak, wpisz 0): '))
            no = float(input('Podaj wartość NO: '))
            pm = float(input('Podaj wartość PM: '))
            samochod_id = int(input('Podaj ID samochodu: '))

            dodaj_pomiar(szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, samochod_id)
        
        elif opcja=='3':
            zapisz_tabele_do_csv()
            
        elif opcja== '4':
            break
        
        else:
            print('=============\nNieprawidłowa opcja. Spróbuj ponownie.=============\n')

interfejs()
conn.close()