# Rozhraní
Popis jednotlivých částí okna zleva doprava, shora dolů. Je přehlednější mít při čtení manuálu spuštěný program.
## Petriho miska
Levá polovina okna zobrazuje petriho misku a buňky v ní. Umožňuje interakci s konkrétními buňkami. Kliknutím levým tlačítkem myši na buňku se buňka označí, bude zvýrazněná a lze ji dočasně uložit (více v **Interakční tlačítka**) a zvlášť pozorovat (více v **Informace o buňkách**). Kliknutím pravým tlačítkem myši lze na dané políčko vložit uloženou buňku, nebo smazat z daného políčka buňku (více v Interakční tlačítka). Políčka mají speciální souřadnicový systém blíže vysvětlený na stránkách https://www.redblobgames.com/grids/hexagons/. Obrázek ukazuje souřadnice sousedů políčka relativně k němu.

![Obrázek souřadnicového systému](/Z%C3%A1po%C4%8Dtov%C3%BD%20program/Sprites/Coordinates.png)
## Experimenty
Pomocí tří tlačítek s nápisy **`EXPERIMENT 1`**, **`EXPERIMENT 2`**, **`EXPERIMENT 3`** lze přepínat mezi pozorovanými experimentry v Petriho miskách. Aktuálně pozorovaný experiment má své tlačítko vybarvené červeně. Všechny experimenty jsou simulovány zvlášť, nezávisle na pozorovaném experimentu. Pod třemi tlačítky jsou vypsány celkové počty buněk v jednotlivých experimentech.
## Interakční tlačítka
Sloupeček 4 tlačítek **`FLUSH`**, **`KILL ALL`**, **`COPY`**, **`MODE: ---`** slouží k základní interakci s experimentem.
* **`FLUSH`** Po stisknutí (levým tlačítkem myši) smaže pozorovaný experiment a změní se na tlačítko **`CREATE`**.
* **`CREATE`** Po stisknutí vytvoří nový experiment s náhodnými buňkami. Experiment lze nastavit v části okna **Počáteční nastavení**.
* **`KILL ALL`** Po stisknutí všechny buňky v pozorovaném experimentu zahynou.
* **`COPY`** Po sisknutí dočasně uloží (aktuálně jen po dobu běhu programu) označenou buňku. Aktuálně lze mít uloženou nejvýše jednu buňku.
* **`MODE: ---`** Po stisknutí změní funkci pravého tlačítka myši. Pokud je **`MODE: PASTE`**, tak pravé tlačítko myši vloží dočasně uloženou buňku na políčko v       petriho misce na kterém je kurzor. Pokud je **`MODE: KILL`**, tak pravé tlačítko myši smaže buňku z políčka v petriho misce na kterém je kurzor. 
## Statistiky, rychlost simulace / Počáteční nastavení
Pravá horní část okna je vymezená pro dvě části rozhraní. Tabulka **Statistiky, rychlost simulace** je zobrazená, pokud je daný experiment vytvořený. Tabulka **Počáteční nastavení** je zobrazená, pokud není zvolený experiment vytvořený.
### Statistiky, rychlost simulace
Tabulka obsahuje sloupeček s tlačítkem **`PAUSE`** a 6 cedulkami se statistikami **`MIDAGE`**, **`MEDAGE`**, **`MAXAGE`**, **`MAXCLUS`**, **`MIDCLUS`**, **`DURATION`** a 2 posuvníky **`KILL CELL PERCENTAGE`**, **`SIMULATION SPEED`**.
* **`PAUSE`** Po stisknutí pozastaví simulaci a změní se na tlačítko **`PLAY`**.
* **`PLAY`** Po stisknutí ukončí pozastavení simulace a změní se na tlačítko **`PAUSE`**.
* **`MIDAGE`** Ukazuje aktuální aritmetický průměr věku buněk.
* **`MEDAGE`** Ukazuje aktuální medián věku buněk.
* **`MAXAGE`** Ukazuje aktuální nejvyšší věk buněk (tj. věk nejstarší buňky). Na cedulku lze kliknout lrvým tlačítkem myši a označit tak nejstarší buňku.
* **`MAXCLUS`** Ukazuje aktuální velikost největšího klastru buněk. 3 buňky jsou ve stejném klastru, jestliže každá sousedí s každou (tvoří trojúhelník).
* **`MIDCLUS`** Ukazuje aktuální aritmetický průměr velikostí klastrů buněk.
* **`DURATION`** Ukazuje aktuální dobu trvání simulace, neboli počet odsimulovaných cyklů.
* **`KILL CELL PERCENTAGE`** Po stisknutí tlačítka nad posuvníkem se z Petriho misky vymaže procento buněk určené hodnotou posuvníku.
* **`SIMULATION SPEED`** Hodnota posuvníku určuje dobu mezi jednotlivými cykly simulace. Hodnota 1 odpovídá 5 sekundám, hodnota 0 odpovídá 0,5 neboli 1/2 sekundy,  hodnota -1 odpovídá 0,05 neboli 1/20 sekundy. Průběh mezi je přibližně exponenciální. Je možné, že při vysokém počtu buněk simulace cyklu zabere delší dobu než je nastaveno.
### Počáteční nastavení
Tabulka obsahuje 4 posuvníky **`GRID RADIUS`**, **`INITIAL CELL PERCENTAGE`**, **`INITIAL CELL ENERGY PERCENTAGE`**, **`INITIAL CELL SIZE PERCENTAGE`**. Všechny tyto posuvníky se používají při vytváření nového experimentu.
* **`GRID RADIUS`** Hodnota posuvníku určuje poloměr Petriho misky, tj. počet políček od středu k okraji.
* **`INITIAL CELL PERCNTAGE`** Hodnota posuvníku určuje, kolik procent políček bude obsazeno buňkami při vytvoření nového experimentu (buňky jsou náhodně generované).
* **`INITIAL CELL ENERGY PERCENTAGE`** Hodnota posuvníku určuje hodnotu počáteční energie buněk. Ta se odvíjí od maximální energie uskladněné na políčku a hodnota posuvníku určuje kolik procent této energie mají buňky při vytvoření experimentu (políčka, na němž jsou buňky, zůstanou při vytvoření experimentu plná energie).
* **`INITIAL CELL SIZE PERCENTAGE`** Hodnota posuvníku určuje, kolik procent své maximální velikosti mají buňky při vytvoření experimentu.
