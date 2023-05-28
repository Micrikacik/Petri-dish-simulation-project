# Rozhraní
Popis jednotlivých částí okna zleva doprava, shora dolů. Je přehlednější mít při čtení manuálu spuštěný program.

## Petriho miska
Levá polovina okna zobrazuje petriho misku a buňky v ní. Umožňuje interakci s konkrétními buňkami. Kliknutím levým tlačítkem myši na buňku se buňka označí, bude zvýrazněná a lze ji dočasně uložit (více v >[**Interakční tlačítka**](INTERFACE_MANUAL.md#in)) a zvlášť pozorovat (více v **Informace o buňkách**). Kliknutím pravým tlačítkem myši lze na dané políčko vložit uloženou buňku, nebo smazat z daného políčka buňku (více v **Interakční tlačítka**). Políčka mají speciální souřadnicový systém blíže vysvětlený na stránkách https://www.redblobgames.com/grids/hexagons/. Obrázek ukazuje souřadnice sousedů políčka relativně k němu.

![Obrázek souřadnicového systému](/Petri_dish_simulation/Sprites/Coordinates.png)

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
Pravá horní část okna je vymezená pro dvě části rozhraní. Panel **Statistiky, rychlost simulace** je zobrazená, pokud je daný experiment vytvořený. Panel **Počáteční nastavení** je zobrazená, pokud není zvolený experiment vytvořený.
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

## Přepínací tlačítko
Pod panelem **Experimenty** je tlačítko **`SETTINGS`**, které slouží k přepínání panelu v pravé dolní části okna.
* **`SETTINGS`** Po stisknutí se pravý dolní panel změní na **Základní nastavení** a tlačítko se změní na **`ADVANCED SETTINGS`**.
* **`ADVANCED SETTINGS`** Po stisknutí se pravý dolní panel změní na **Pokročilé nastavení** a tlačítko se změní na **`CELL STATS`**.
* **`CELL STATS`** Po stisknutí se pravý dolní panel změní na **Informace o buňkách** a tlačítko se změní na **`SETTINGS`**.

## Informace o buňkách / Základní nastavení / Pokročilé nastavení
Pravá dolní část okna je vymezena pro tři části rozhraní. Mezi těmito částmi se přepíná pomocí tlačítka nad levým horním rohem panelu.
### Informace o buňkách
Panel je rozdělen na dva sloupce, a to **Cursor cell** a **Marked cell**. Oba ukazují informace o buňce. Sloupec **Cursor cell** ukazuje buňku v Petriho misce nad kterou je kurzor (pozn. zkoumaná buňka se může změnit pouze pohybem kurzoru). Sloupec **Marked cell** ukazuje buňku v petriho misce která je označená. Buňka se označuje kliknutím levého tlačítka myši na ni. Označená buňka je v Petriho misce zvýrazněná obrysem.

Oba sloupce ukazují stejné typy informací.
* První řádek (červený) ukazuje informace o políčku na němž je buňka, a to jeho hexagonov souřadnice tvaru `XX, XX, XX` (více v **Petriho miska**) a energii obsaženou v políčku `energy: XXXX`.
* Druhý řádek (zelený) ukazuje základní informace o buňce, a to její hexagonovou pozici `Hex pos: XX, XX, XX`, kolik má energie `energy: XXXX`, jakou má velikost `size: XXXX` a jak je stará `age: XXXX`.
