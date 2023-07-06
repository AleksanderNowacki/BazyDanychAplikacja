import os
import json
import psycopg
import csv

# Wczytanie danych do połączenia z pliku database_creds.json
with open("database_creds.json") as file:
    creds = json.load(file)

# Pobranie danych do połączenia z bazą danych
user = creds['user_name']
password = creds['password']
host = creds['host_name']
port = creds['port_number']
dbname = creds['db_name']  # Zmieniono nazwę zmiennej na "dbname"

# Połączenie z bazą danych
connection = psycopg.connect(
    host=host,
    port=port,
    dbname=dbname,  # Zmieniono opcję na "dbname"
    user=user,
    password=password
)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Samochod (
        NumerVIN TEXT PRIMARY KEY,
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
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pomiary (
        ID SERIAL PRIMARY KEY,
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
        NumerVIN TEXT,
        FOREIGN KEY (NumerVIN) REFERENCES Samochod (NumerVIN)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Norma (
        ID SERIAL PRIMARY KEY,
        Nazwa TEXT,
        TypPaliwa TEXT,
        CO_limit REAL,
        HC_limit REAL,
        NO_limit REAL,
        PM_limit REAL
    )
''')




# Metoda do importowania danych samochodów
def importuj_samochody(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Pominięcie nagłówka
            for row in reader:
                numer_vin, marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu = row
                dodaj_samochod(numer_vin, marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu)
        print('Import danych samochodów zakończony sukcesem.')
    except FileNotFoundError:
        print(f'Błąd: Plik "{nazwa_pliku}" nie został znaleziony.')
    except psycopg.Error as e:
        print('Błąd podczas importowania danych samochodów:', e)


# Metoda do importowania danych pomiarów
def importuj_pomiary(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=',')  # Zmieniono separator na przecinek
            next(reader)  # Pominięcie nagłówka
            for row in reader:
                try:
                    if len(row) != 13:
                        print("Błąd w wierszu:", row)
                        print("Liczba wartości:", len(row))
                        continue
                    numer, data, godzina, szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, numer_vin = row

                    # Konwersja pól na odpowiednie typy danych
                    numer = int(numer)
                    szerokosc_geograficzna = float(szerokosc_geograficzna)
                    dlugosc_geograficzna = float(dlugosc_geograficzna)
                    moc = float(moc)
                    moment_obrotowy = float(moment_obrotowy)
                    co = float(co)
                    hc = float(hc)
                    no = float(no)
                    pm = float(pm)

                    dodaj_pomiar(data, godzina, szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, numer_vin)
                except Exception as e:
                    print("Błąd w wierszu:", row)
                    print("Wyjątek:", e)
        connection.commit()  # Zapisanie zmian w bazie danych
        print('Import danych pomiarów zakończony sukcesem.')
    except FileNotFoundError:
        print(f'Błąd: Plik "{nazwa_pliku}" nie został znaleziony.')
    except psycopg.Error as e:
        print('Błąd podczas importowania danych pomiarów:', e)




# Metoda do wypisywania danych samochodów
def wypisz_samochody():
    cursor.execute("SELECT * FROM Samochod")
    samochody = cursor.fetchall()

    print("========= SAMOCHODY =========")
    for samochod in samochody:
        print("Numer VIN:", samochod[0])
        print("Marka:", samochod[1])
        print("Model:", samochod[2])
        print("Rok produkcji:", samochod[3])
        print("Silnik:", samochod[4])
        print("Typ paliwa:", samochod[5])
        print("Typ nadwozia:", samochod[6])
        print("Masa pojazdu:", samochod[7])
        print("=============================")

# Metoda do wypisywania danych pomiarów
def wypisz_pomiary():
    cursor.execute("SELECT * FROM Pomiary")
    pomiary = cursor.fetchall()

    print("========== POMIARY ==========")
    for pomiar in pomiary:
        print("ID:", pomiar[0])
        print("Data:", pomiar[1])
        print("Godzina:", pomiar[2])
        print("Szerokość geograficzna:", pomiar[3])
        print("Długość geograficzna:", pomiar[4])
        print("Silnik:", pomiar[5])
        print("Moc:", pomiar[6])
        print("Moment obrotowy:", pomiar[7])
        print("CO:", pomiar[8])
        print("HC:", pomiar[9])
        print("NO:", pomiar[10])
        print("PM:", pomiar[11])
        print("Numer VIN samochodu:", pomiar[12])
        print("=============================")
        
# Metoda do wypisywania tabeli Norma
def wypisz_tabele_norm():
    cursor.execute('SELECT * FROM Norma')
    normy = cursor.fetchall()

    if not normy:
        print('Brak danych w tabeli Norma.')
        return

    print('Tabela Norma:')
    print('ID  | Nazwa              | Typ Paliwa   | CO Limit | HC Limit | NO Limit | PM Limit')
    print('----|--------------------|--------------|----------|----------|----------|---------')

    for norma in normy:
        norma_id, nazwa, typ_paliwa, co_limit, hc_limit, no_limit, pm_limit = norma
        print(f'{norma_id:3} | {nazwa:18} | {typ_paliwa:12} | {co_limit:8.2f} | {hc_limit:8.2f} | {no_limit:8.2f} | {pm_limit:8.4f}')

    print('----|--------------------|--------------|----------|----------|----------|---------')


# Metoda do dodawania samochodu
def dodaj_samochod(numer_vin, marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu):
    cursor.execute('''
        INSERT INTO Samochod (NumerVIN, Marka, Model, RokProdukcji, Silnik, TypPaliwa, TypNadwozia, MasaPojazdu)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (numer_vin, marka, model, rok_produkcji, silnik, typ_paliwa, typ_nadwozia, masa_pojazdu))

    connection.commit()
    print("Samochód dodany do bazy danych.")

# Metoda do dodawania pomiaru do bazy danych
def dodaj_pomiar(data, godzina, szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, numer_vin):
    try:
        cursor.execute("INSERT INTO Pomiary (Data, Godzina, SzerokoscGeograficzna, DlugoscGeograficzna, Silnik, Moc, MomentObrotowy, CO, HC, NO, PM, NumerVIN) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (data, godzina, szerokosc_geograficzna, dlugosc_geograficzna, silnik, moc, moment_obrotowy, co, hc, no, pm, numer_vin))
        print('Pomiar dodany do bazy danych.')
    except psycopg.Error as e:
        print('Błąd podczas dodawania pomiaru:', e)
    connection.commit()
    print("Pomiar dodany do bazy danych.")
    
# Metoda do dodawania normy do bazy danych
def dodaj_norme(nazwa, typ_paliwa, co_limit, hc_limit, no_limit, pm_limit):
    cursor.execute('''
        INSERT INTO Norma (Nazwa, TypPaliwa, CO_limit, HC_limit, NO_limit, PM_limit)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nazwa, typ_paliwa, co_limit, hc_limit, no_limit, pm_limit))

    connection.commit()
    print('Norma dodana do bazy danych.')


# Metoda do obsługi menu głównego
def menu_glowne():
    while True:
        print("========= MENU GŁÓWNE =========")
        print("1. Importuj samochody")
        print("2. Importuj pomiary")
        print("3. Dodaj normę")
        print("4. Wypisz samochody")
        print("5. Wypisz pomiary")
        print("6. Wypisz tabelę norm")
        print("7. Zakończ")
        print("===============================")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            nazwa_pliku = input("Podaj nazwę pliku z danymi samochodów: ")
            importuj_samochody(nazwa_pliku)
        elif wybor == "2":
            nazwa_pliku = input("Podaj nazwę pliku z danymi pomiarów: ")
            importuj_pomiary(nazwa_pliku)
        elif wybor == "3":
            nazwa = input("Podaj nazwę normy: ")
            typ_paliwa = input("Podaj typ paliwa: ")
            co_limit = float(input("Podaj limit CO: "))
            hc_limit = float(input("Podaj limit HC: "))
            no_limit = float(input("Podaj limit NO: "))
            pm_limit = float(input("Podaj limit PM: "))
            dodaj_norme(nazwa, typ_paliwa, co_limit, hc_limit, no_limit, pm_limit)
        elif wybor == "4":
            wypisz_samochody()
        elif wybor == "5":
            wypisz_pomiary()
        elif wybor == "6":
            wypisz_tabele_norm()
        elif wybor == "7":
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            
    cursor.close()
    connection.close()

# Uruchomienie menu głównego
menu_glowne()
