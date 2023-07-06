Instrukcja obsługi aplikacji klienckiej
=============================================

Elementy obsługi:
------------------------------------------------------------------------------------------------------------------------------------

1.	Dodaj samochód
------------------------------------------------------------------------------------------------------------------------------------
-	Użytkownik dodaje informacje o samochodzie do bazy danych podając po kolei parametry:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Marka samochodu
- Model samochodu
- Rok produkcji
- Litraż silnika
- Typ paliwa
- Typ nadwozia
- Masę pojazdu (w kg) 

2.	Dodaj pomiar
------------------------------------------------------------------
-	Użytkownik dodaje informacje o pomiarach emisji do bazy danych podając po kolei parametry:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Szerokość geograficzną
- Długość geograficzną
- Typ paliwa
- Moc silnika (w hp)
- Moment obrotowy silnika (w nm)
- Wartość CO
- Wartość HC (0 jeśli samochód nie posiada wartości HC)
- Wartość NO
- Wartość PM
- ID samochodu

3.	<Zapisz do .csv>
------------------------------------------------------------------------------------------------------------------------------------
-	Opcja ta zapisuje wcześniej wpisane wartości samochodów i pomiarów do odpowiednich plików CSV.~

4.	Wyjście
------------------------------------------------------------------------------------------------------------------------------------
-	Wyjście kończy działanie programu bez zapisu danych do plików CSV.

5.	Wpisanie nieistniejącej opcji
------------------------------------------------------------------------------------------------------------------------------------
-	Wypisywana jest wiadomość „Nieprawidłowa opcja. Spróbuj ponownie.”.
