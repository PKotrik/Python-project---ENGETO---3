# Úvod

Tento program umožňuje stahovat výsledky voleb za rok 2017 z webu:  
[https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)  
pro každý územní celek. Výsledky program zapíše do `.csv` souboru.  
Výsledný soubor bude obsahovat data pro každou obec z vybraného územního celku.  

Program stáhne a zapíše následující informace:  
- kód obce,  
- název obce,  
- počet voličů v seznamu,  
- počet vydaných obálek,  
- počet platných hlasů,  
- celkový počet hlasů pro jednotlivé kandidující strany.  

---

# Instalace

Pro správné fungování projektu je nutné:

1. Nejprve vytvořit virtuální prostředí v příkazovém řádku pomocí knihovny `venv`:  

   python -m venv moje_prvni_prostredi

2. Aktivovat vytvořené virtuální prostředí:

    Windows:
    moje_prvni_prostredi\Scripts\Activate

    Linux/Mac OS:
    source moje_prvni_prostredi/bin/activate

Po spuštění virtuálního prostředí se jeho název zobrazí na začátku řádku v kulatých závorkách.

3. Po aktivaci virtuálního prostředí nainstalujte knihovny uvedené v souboru requirements.txt pomocí příkazu:

    pip install -r requirements.txt

---

# Spuštění

Pro správné spuštění je nejprve nutné vždy aktivovat vytvořené virtuální prostředí přes příkazový řádek, jak je uvedeno výše.

Pro následné spuštění je nutné zadat 2 argumenty ve správném pořadí:

1. Odkaz na vybraný územní celek s možností výběru obcí, například:
    https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
    
2. Název výsledného .csv souboru, včetně přípony, například:
    vysledky_stredocesky_kraj.csv

Příklad:
    python Task_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_stredocesky_kraj.csv"

Pokud byly argumenty zadány správně, program oznámí:

    "Argumenty byly zadány správně, stahuji data."

a pokračuje stahováním dat.

V případě nesprávného zadání jednoho nebo obou argumentů program oznámí chybu a je nutné jej znovu spustit se správnými argumenty.

Pokud program proběhne správně, oznámí:

    "Všechna data zapsaná."

Výsledný .csv soubor bude uložen ve stejné složce, kde je uložen projekt.




