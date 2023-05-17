import matplotlib.pyplot as plt

def zapisz_wynik_do_pliku(nazwa_pliku, wynik):
    with open(nazwa_pliku, "a") as plik:
        plik.write(str(wynik) + "\n")

def wczytaj_wyniki_z_pliku(nazwa_pliku):
    wyniki = []
    with open(nazwa_pliku, "r") as plik:
        for linia in plik:
            wyniki.append(int(linia.strip()))
    return wyniki

def wypisz_wyniki(wyniki):
    for i, wynik in enumerate(wyniki):
        print(f"Wynik nr {i+1}: {wynik}")


def rysuj_wykres(wyniki,który_test):
    plt.plot(wyniki)
    plt.xlabel("Liczba testów")
    plt.ylabel("Wynik")
    plt.title(f"Wyniki testów{który_test}")
    plt.show()
