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


def eval_arg_1(link: str) -> bool:
    """
    Tato funkce vyhodnoti jestli prvni argument zadan uzivatelem byl zadan spravne. Jestli ano, vrati True, jinak False.
    """
    if link.startswith("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=") and "&xnumnuts" in link:
        return True
    else:
        return False


def eval_arg_2(name_csv: str) -> bool:
    """
    Tato funkce vyhonoti jestli druhy argument zadan uzivatelem byl zadan spravne,vcetne pripony .csv. Jestli ano, vrati True, jinak False.
    """
    if name_csv.endswith(".csv"):
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

    if eval_1 and eval_2:
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
            "Chyba v zadani argumentu. Je potreba zadat nejdriv odkaz na uzemni celek s moznosti vyberu obci a pak jmeno souboru s priponou .csv."
        )


def create_list_of_links(link: str) -> list:
    """
    Tato funkce prehleda vstupni web a vytvori seznam odkazu na jednotlive obce ve vybranem uzemnim celku. 
    """
    answer = get(link)
    split_html = bs(answer.text, features="html.parser")
    all_links = split_html.find_all("a")

    links = []
    for a_tag in all_links:
        if a_tag.attrs["href"] in links:
            continue
        else:
            links.append(a_tag.attrs["href"])

    links_final = []

    for link in links:
        if "xvyber" in link:
            links_final.append("https://www.volby.cz/pls/ps2017nss/" + link)

    return links_final


def create_header(links_final: list) -> list:
    """
    Tato funkce vytvori hlavicku vystupniho .csv souboru.
    """
    header = [
        "Kód obce",
        "Název obce",
        "Voliči v seznamu",
        "Vydané obálky",
        "Platné hlasy",
    ]
    answer = get(links_final[0])
    split_html = bs(answer.text, features="html.parser")
    all_parties = split_html.find_all("td", {"class": "overflow_name"})

    for party in all_parties:
        party = str(party)
        party_split = party.split(">")
        party_name_clean = str(party_split[1]).strip("</td>")
        header.append(party_name_clean)

    return header


def read_data_from_link(link: str) -> list:
    """
    Tato funkce prechazi data z vybraneho odkazu a dohledava informace definovane v hlavicce, ktere ocisti a uklada do listu 'row'. 
    """
    row = []

    town_code = link.split("&x")
    row.append(town_code[2].strip("obec="))

    answer = get(link)
    split_html = bs(answer.text, features="html.parser")

    town_names = split_html.find_all("h3")
    data = split_html.find_all("td", {"class": "cislo"})

    for name in town_names:
        if "Obec:" in str(name):
            name_split = str(name).split("Obec: ")
            row.append(name_split[1].strip("\n</h3>"))
        else:
            continue

    for result in data:
        result_split = str(result).split(">")
        result_clean = result_split[1].strip("</td>")

        if "sa2" in result.attrs["headers"]:
            row.append(result_clean)
        elif "sa3" in result.attrs["headers"]:
            row.append(result_clean)
        elif "sa6" in result.attrs["headers"]:
            row.append(result_clean)
        elif "t1sa2" in result.attrs["headers"] and "t1sb3" in result.attrs["headers"]:
            row.append(result_clean)
        elif "t2sa2" in result.attrs["headers"] and "t2sb3" in result.attrs["headers"]:
            row.append(result_clean)
        else:
            continue

    return row


def write_data(name_csv: str, links_final: list):
    """
    Tato funkce zapise hlavicku a jednotlive radky do souboru .csv.
    """
    with open(name_csv, mode="w", encoding="utf-16") as csv_file:
        header = create_header(links_final)
        writer = csv.writer(csv_file, dialect="excel-tab", lineterminator="\n")
        writer.writerow(header)

        for odkaz in links_final:
            writer.writerow(read_data_from_link(odkaz))

    print("Vsechna data zapsana.")


def main():
    """
    Tato funkce vyhodnoti jestli argumenty splnuji vsechny pozadavky, jestli ano, spusti funkci na vytvoreni zoznamu odkazu a nasledne spusti proces zapisu dat do .csv.
    """
    if eval_arg_len() == True:
        if eval_args(sys.argv[1], sys.argv[2]) == True:
            links_final = create_list_of_links(sys.argv[1])
            write_data(sys.argv[2], links_final)


if __name__ == "__main__":
    main()

