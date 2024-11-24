# projekt_3.py: třetí projekt do Engeto Online Python Akademie
# author: Patrícia Kotrík Iliašová
# email: iliasovap@gmail.com
# discord: discord: iliasovap_54684

from bs4 import BeautifulSoup as bs
from requests import get
import sys
import csv


def eval_arg_len() -> bool:
    """
    Tato funkce vyhodnoti jestli byly zadany oba argumenty. Pokud ano, vrati True, pokud ne, vrati False.
    """
    if len(sys.argv) != 3:
        print(
            "Pro spusteni programu je potreba zadat nasledujici argumenty v tomhle poradi: 1: odkaz na uzemni celek, 2: jmeno vystupniho souboru vcetne pripony .csv."
        )
        return False
    else:
        return True


def eval_arg_1(odkaz: str) -> bool:
    """
    Tato funkce vyhodnoti jestli prvni argument zadan uzivatelem byl zadan spravne. Jestli ano, vrati True, jinak False.
    """
    if (
        odkaz.startswith("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=")
        and "&xnumnuts" in odkaz
    ):
        return True
    else:
        return False


def eval_arg_2(jmeno_csv: str) -> bool:
    """
    Tato funkce vyhonoti jestli druhy argument zadan uzivatelem byl zadan spravne,vcetne pripony .csv. Jestli ano, vrati True, jinak False.
    """
    if jmeno_csv.endswith(".csv"):
        return True
    else:
        return False


def eval_args(arg_1: str, arg_2: str) -> bool:
    """
    Tato funkce overi, jestli oba argumenty byly zadany spravne, anebo jestli uzivatel pri zadani argumentu pochybil. 
    Funkce upozorni uzivatele na chyby v zadani argumentu a vrati hodnotu False, pokud byl alespon jeden argument zadan spatne.
    Pokud byly oba argumenty zadany spravne, funkce oboznami uzivatele a vrati True.
    """
    eval_1 = eval_arg_1(arg_1)
    eval_2 = eval_arg_2(arg_2)

    if eval_1 == True and eval_2 == True:
        print("Argumenty byly zadany spravne, stahuji data.")
        return True

    elif eval_1 == True and eval_2 == False:
        print(
            "Argument jmeno souboru nebyl zadan spravne, je potreba zadat cely nazev souboru vcetne pripony .csv."
        )

    elif eval_1 == False and eval_2 == True:
        print(
            "Chyba v zadani prvniho argumentu. Je potreba zadat odkaz na uzemni celek."
        )

    else:
        print(
            "Chyba v zadani argumentu. Je potreba zada odkaz na uzemni celek s moznosti vyberu obci a jmeno souboru s priponou .csv."
        )


def create_list_of_links(odkaz: str) -> list:
    """
    Tato funkce prehleda vstupni web a vytvori seznam odkazu na jednotlive obce ve vybranem uzemnim celku. 
    """
    odpoved = get(odkaz)
    rozdelene_html = bs(odpoved.text, features="html.parser")
    vsechny_a_odkazy = rozdelene_html.find_all("a")

    odkazy = []
    for a_tag in vsechny_a_odkazy:
        if a_tag.attrs["href"] in odkazy:
            continue
        else:
            odkazy.append(a_tag.attrs["href"])

    odkazy_final = []

    for link in odkazy:
        if "xvyber" in link:
            odkazy_final.append("https://www.volby.cz/pls/ps2017nss/" + link)

    return odkazy_final


def vytvor_hlavicku(odkazy_final: list) -> list:
    """
    Tato funkce vytvori hlavicku vystupniho .csv souboru.
    """
    hlavicka = [
        "Kód obce",
        "Název obce",
        "Voliči v seznamu",
        "Vydané obálky",
        "Platné hlasy",
    ]
    odpoved = get(odkazy_final[0])
    rozdelene_html = bs(odpoved.text, features="html.parser")
    vsechny_strany = rozdelene_html.find_all("td", {"class": "overflow_name"})

    for strana in vsechny_strany:
        strana = str(strana)
        strana_split = strana.split(">")
        strana_jmeno_clean = str(strana_split[1]).strip("</td>")
        hlavicka.append(strana_jmeno_clean)

    return hlavicka


def cti_data_z_odkazu(odkaz: str) -> list:
    """
    Tato funkce prechazi data z vybraneho odkazu a dohledava informace definovane v hlavicce, ktere ocisti a uklada do listu 'radek'. 
    """
    radek = []
    kod_obce = odkaz.split("&x")
    radek.append(kod_obce[2].strip("obec="))
    odpoved = get(odkaz)
    rozdelene_html = bs(odpoved.text, features="html.parser")
    nazvy = rozdelene_html.find_all("h3")
    data = rozdelene_html.find_all("td", {"class": "cislo"})

    for nazev in nazvy:
        if "Obec:" in str(nazev):
            nazev_split = str(nazev).split("Obec: ")
            radek.append(nazev_split[1].strip("\n</h3>"))
        else:
            continue

    for vysledek in data:
        vysledek_split = str(vysledek).split(">")
        vysledek_clean = vysledek_split[1].strip("</td>")

        if "sa2" in vysledek.attrs["headers"]:
            radek.append(vysledek_clean)
        elif "sa3" in vysledek.attrs["headers"]:
            radek.append(vysledek_clean)
        elif "sa6" in vysledek.attrs["headers"]:
            radek.append(vysledek_clean)
        elif (
            "t1sa2" in vysledek.attrs["headers"]
            and "t1sb3" in vysledek.attrs["headers"]
        ):
            radek.append(vysledek_clean)
        elif (
            "t2sa2" in vysledek.attrs["headers"]
            and "t2sb3" in vysledek.attrs["headers"]
        ):
            radek.append(vysledek_clean)
        else:
            continue

    return radek


def zapis_data(jmeno_csv: str, odkazy_final: list):
    """
    Tato funkce zapise hlavicku a jednotlive radky do souboru .csv.
    """
    with open(jmeno_csv, mode="w", encoding="utf-16") as csv_soubor:
        hlavicka = vytvor_hlavicku(odkazy_final)
        zapisovac = csv.writer(csv_soubor, dialect="excel-tab", lineterminator="\n")
        zapisovac.writerow(hlavicka)

        for odkaz in odkazy_final:
            zapisovac.writerow(cti_data_z_odkazu(odkaz))

    return print("Vsechna data zapsana.")


def main():
    """
    Tato funkce vyhodnoti jestli argumenty splnuji vsechny pozadavky, jestli ano, spusti funkci na vytvoreni zoznamu odkazu a nasledne spusti proces zapisu dat do .csv.
    """
    eval_arg_len()
    if eval_arg_len() == True:
        if eval_args(sys.argv[1], sys.argv[2]) == True:
            odkazy_final = create_list_of_links(sys.argv[1])
            zapis_data(sys.argv[2], odkazy_final)


main()

