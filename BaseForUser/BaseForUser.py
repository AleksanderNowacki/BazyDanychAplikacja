import psycopg
import json


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

def wyswietl_samochody():
    cursor = connection.cursor()
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
        print("==============================")

def wyswietl_pomiary():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Pomiary")
    pomiary = cursor.fetchall()

    print("========= POMIARY =========")
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
        print("Numer VIN:", pomiar[12])
        print("===========================")

def sprawdz_norme(numer_vin, nazwa_normy):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Norma WHERE Nazwa = %s AND TypPaliwa = (SELECT TypPaliwa FROM Samochod WHERE NumerVIN = %s)", (nazwa_normy, numer_vin))
    norma = cursor.fetchone()

    if norma:
        cursor.execute("SELECT * FROM Pomiary WHERE NumerVIN = %s", (numer_vin,))
        pomiary = cursor.fetchall()

        print("========= POMIARY NIE SPEŁNIAJĄCE NORMY DLA SAMOCHODU O NUMERZE VIN:", numer_vin, " =========")
        print("Norma:", nazwa_normy)
        print("CO limit:", norma[3])
        print("HC limit:", norma[4])
        print("NO limit:", norma[5])
        print("PM limit:", norma[6])
        print("======================================================")
        for pomiar in pomiary:
            if float(pomiar[8]) > float(norma[3]) or float(pomiar[9]) > float(norma[4]) or float(pomiar[10]) > float(norma[5]) or float(pomiar[11]) > float(norma[6]):
                print("ID:", pomiar[0])
                print("Data:", pomiar[1])
                print("Godzina:", pomiar[2])
                print("Szerokość geograficzna:", pomiar[3])
                print("Długość geograficzna:", pomiar[4])
                print("Silnik:", pomiar[5])
                print("Moc:", pomiar[6])
                print("Moment obrotowy:", pomiar[7])
                if float(pomiar[8]) > float(norma[3]):
                    print("CO przekracza limit:", pomiar[8])
                if float(pomiar[9]) > float(norma[4]):
                    print("HC przekracza limit:", pomiar[9])
                if float(pomiar[10]) > float(norma[5]):
                    print("NO przekracza limit:", pomiar[10])
                if float(pomiar[11]) > float(norma[6]):
                    print("PM przekracza limit:", pomiar[11])
                print("Numer VIN:", pomiar[12])
                print("===========================")
        if all(float(pomiar[8]) <= float(norma[3]) and float(pomiar[9]) <= float(norma[4]) and float(pomiar[10]) <= float(norma[5]) and float(pomiar[11]) <= float(norma[6]) for pomiar in pomiary):
            print("Wszystkie pomiary spełniają normy dla samochodu o numerze VIN:", numer_vin)
    else:
        print("Brak zdefiniowanej normy o nazwie:", nazwa_normy, "dla samochodu o numerze VIN:", numer_vin)

# Metoda do generowania raportu
def generuj_raport():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Pomiary")
    pomiary = cursor.fetchall()

    print("========= RAPORT =========")
    for pomiar in pomiary:
        numer_vin = pomiar[12]
        cursor.execute("SELECT * FROM Samochod WHERE NumerVIN = %s", (numer_vin,))
        samochod = cursor.fetchone()

        if samochod:
            typ_paliwa = samochod[5]
            cursor.execute("SELECT * FROM Norma WHERE TypPaliwa = %s", (typ_paliwa,))
            norma = cursor.fetchone()

            if norma:
                if float(pomiar[8]) <= float(norma[3]) and float(pomiar[9]) <= float(norma[4]) and float(pomiar[10]) <= float(norma[5]) and float(pomiar[11]) <= float(norma[6]):
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
                    print("Numer VIN:", pomiar[12])
                    print("Status: POMIAR W NORMIE")
                    print("===========================")
                else:
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
                    print("Numer VIN:", pomiar[12])
                    print("Status: POMIAR NIE SPEŁNIA NORMY")
                    print("===========================")
            else:
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
                print("Numer VIN:", pomiar[12])
                print("Status: BRAK ZDEFINIOWANEJ NORMY")
                print("===========================")
        else:
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
            print("Numer VIN:", pomiar[12])
            print("Status: BRAK DANYCH O SAMOCHODZIE")
            print("===========================")


# Metoda do wyszukiwania samochodu po numerze VIN
def wyszukaj_samochod(numer_vin):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Samochod WHERE NumerVIN = %s", (numer_vin,))
    samochod = cursor.fetchone()

    if samochod:
        print("========= INFORMACJE O SAMOCHODZIE O NUMERZE VIN:", numer_vin, " =========")
        print("Numer VIN:", samochod[0])
        print("Marka:", samochod[1])
        print("Model:", samochod[2])
        print("Rok produkcji:", samochod[3])
        print("Silnik:", samochod[4])
        print("Typ paliwa:", samochod[5])
        print("Typ nadwozia:", samochod[6])
        print("Masa pojazdu:", samochod[7])
        print("===========================")
    else:
        print("Brak samochodu o podanym numerze VIN:", numer_vin)

# Metoda do wyszukiwania pomiarów po numerze VIN
def wyszukaj_pomiary(numer_vin):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Pomiary WHERE NumerVIN = %s", (numer_vin,))
    pomiary = cursor.fetchall()

    print("========= POMIARY DLA SAMOCHODU O NUMERZE VIN:", numer_vin, " =========")
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
        print("===========================")
        
        
def menu():
    while True:
        print("========== MENU ==========")
        print("1. Wyświetl samochody")
        print("2. Wyświetl pomiary")
        print("3. Sprawdź normę dla samochodu")
        print("4. Generuj raport")
        print("5. Wyszukaj samochód po numerze VIN")
        print("6. Wyszukaj pomiary po numerze VIN")
        print("7.  Wyjście")

        wybor = input("Wybierz opcję (1-7): ")

        if wybor == "1":
            wyswietl_samochody()
        elif wybor == "2":
            wyswietl_pomiary()
        elif wybor == "3":
            numer_vin = input("Podaj numer VIN samochodu: ")
            nazwa_normy=input("Podaj nazwe normy: ")
            sprawdz_norme(numer_vin, nazwa_normy)
        elif wybor == "4":
            generuj_raport()
        elif wybor == "5":
            numer_vin = input("Podaj numer VIN samochodu: ")
            wyszukaj_samochod(numer_vin)
        elif wybor == "6":
            numer_vin = input("Podaj numer VIN samochodu: ")
            wyszukaj_pomiary(numer_vin)
        elif wybor == "7":
            break
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")

menu()
