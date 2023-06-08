# Rozhraní
Popis jednotlivých částí okna zleva doprava, shora dolů. Je přehlednější mít při čtení manuálu spuštěný program.

## Petriho miska
Levá polovina okna zobrazuje petriho misku a buňky v ní. Umožňuje interakci s konkrétními buňkami. Kliknutím levým tlačítkem myši na buňku se buňka označí, bude zvýrazněná a lze ji dočasně uložit (více v **Interakční tlačítka**) a zvlášť pozorovat (více v **Informace o buňkách**). Kliknutím pravým tlačítkem myši lze na dané políčko vložit uloženou buňku, nebo smazat z daného políčka buňku (více v **Interakční tlačítka**). Políčka mají speciální souřadnicový systém, blíže vysvětlený v [**CODE.md - Souřadnice**](CODE.md). Obrázek ukazuje souřadnice sousedů políčka relativně k němu.

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
Tabulka obsahuje sloupeček s tlačítkem **`PAUSE`** a 6 cedulkami se statistikami **`MIDAGE`**, **`MEDAGE`**, **`MAXAGE`**, **`MAXCLUS`**, **`MIDCLUS`**, **`CELLEAT`**, **`DURATION`** a 2 posuvníky **`KILL CELL PERCENTAGE`**, **`SIMULATION SPEED`**.
* **`PAUSE`** Po stisknutí pozastaví simulaci a změní se na tlačítko **`PLAY`**.
* **`PLAY`** Po stisknutí ukončí pozastavení simulace a změní se na tlačítko **`PAUSE`**.
* **`MIDAGE`** Ukazuje aktuální aritmetický průměr věku buněk.
* **`MEDAGE`** Ukazuje aktuální medián věku buněk.
* **`MAXAGE`** Ukazuje aktuální nejvyšší věk buněk (tj. věk nejstarší buňky). Na cedulku lze kliknout lrvým tlačítkem myši a označit tak nejstarší buňku.
* **`MAXCLUS`** Ukazuje aktuální velikost největšího klastru buněk. 3 buňky jsou ve stejném klastru, jestliže každá sousedí s každou (tvoří trojúhelník).
* **`MIDCLUS`** Ukazuje aktuální aritmetický průměr velikostí klastrů buněk.
* **`CELLEAT`** Ukazuje, kolik buňek bylo snězeno v posledním cyklu.
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
* První řádek (červený) ukazuje informace o políčku na němž je buňka, a to jeho hexagonov souřadnice tvaru `XX, XX, XX` (více v **Petriho miska**), energii obsaženou v políčku `energy: XXXX`.
* Druhý řádek (zelený) ukazuje základní informace o buňce, a to její hexagonovou pozici `Hex pos: XX, XX, XX`, kolik má energie `energy: XXXX`, jakou má velikost `size: XXXX`, jak je stará `age: XXXX`.
* Třetí řádek ukazuje aktuální stav buňky. Čtvrtý řádek a dále ukazují postupně všechny možné stavy buňky. Tyto řádky mají základně zelenou barvu. Žlutá barva zvýrazňuje ten stav, ve kterém se buňka aktuálně nachází. Pokud oba sloupce **Cursor cell** i **Marked cell** ukazují nějakou buňku, tak ty stavy, ve kterých se buňka ve sloupci **Cursor cell** liší od buňky ve sloupci **Marked cell**, jsou zvýrazněné červeně.Řádky ukazující stavy zobrazují číslo stavu `X`, akci `AKCE:`, vlastnost akce `VLASTNOST:`, podmínku `PODMÍNKA:`, vlastnost podmínky `VLASTNOST`, příští stavy `A:X B:X`.

#### Stavy buněk (vysvětlení značení)
**Značení akcí:**
* STILL - *odpočinek*, okamžitě následuje podmínka
* MOVE - *pohyb*, následuje směr pohybu
* DIV - *buněčné dělení*, následuje směr dělení
* SHARE - *sdílení energie*, následuje procento sdílené energie

**Značení podmínek:**
* ENER - *podmínka energie*, následuje, jakou nerovnost musí splňovat energie buňky
* SIZE - *podmínka velikosti*, následuje, jakou nerovnost musí splňovat velikost buňky
* SENS - *podmínka senzoru*, následuje směr senzoru, dále následuje typ senzoru (free - volné pole, cell - buňka na poli, ener - porovnání energie)

(všechny akce a stavy jsou vysvětleny v [**SIMULATION.md - Souřadnice**](SIMULATION.md)

### Základní nastavení
Panel obsahuje 4 posuvníky **`TILE REFILL PERCENTAGE`**, **`PERCENTAGE OF REFILLED TILES`**, **`CELL ENERGY ABSORB PERCENTAGE`**, **`CELL ENERGY CONSUMPTION PERCENTAGE`**, **`CELL ENERGY TILE LOSS PERCENTAGE`**, které slouží k jednoduché úpravě experimentu, a to i za běhu simulace.
* **`TILE REFILL PERCENTAGE`** Hodnota posuvníku udává, kolik procent energie z maximální energie se obnoví políčku v každém cyklu.
* **`PERCENTAGE OF REFILLED TILES`** Hodnota posuvníku udává, kolik procent políček se v kaýždém cyklu vybere pro obnovení energie, tj. tomuto procentu se energie obnoví podle hodnoty **`TILE REFILL PERCENTAGE`** a ostatním se energie neobnoví.
* **`CELL ENERGY ABSORB PERCENTAGE`** Hodnota posuvníku udává, kolik nejvýše (políčko nemusí mít dost energie) procent maximální energie políčka každá buňka absorbuje z políčka, na kterém se nachází, každý cyklus.
* **`CELL ENERGY CONSUMPTION PERCENTAGE`** Hodnota posuvníku udává, kolik energie buňka spotřebuje pro existenci každý cyklus. Tato hodnota se odvíjí od maximální energie políček a posuvník určuje, kolik procent této hodnoty políček buňka spotřebuje.
* **`CELL ENERGY TILE LOSS PERCENTAGE`** Hodnota posuvníku udává, kolik nejvýše může buňka ztratit energie do okolí každý cyklus. Tato hodnota se odvíjí od maximální energie políček a posuvník určuje, kolik procent této hodnoty políček buňka ztratí. Dále se tato hodnota odvíjí od počtu sousedních políček, na kterých nejsou buňky. Hodnota ztráty se vynásobí zlomkem hodnoty od 0 do 1, který udává podíl políček bez buňek ku 6 (tj. ku všem okolním políčkám).

### Pokročilé nastavení
Panel obsahuje 18 polí s hodnotami, které slouží ke složitějším úpravám experimentu, a to i za běhu simulace. Do každého pole lze napsat hodnotu od 0 do 100, nebo lze použít šipky na pravé straně pole které hodnotu změní o +0.1 (nahoru) nebo -0.1 (dolů).
* **`MAX ENERGY BASE PERCENTAGE`** Hodnota v poli udává, jaká je základní maximální energie buněk(buňky mají omezenou maximální energii). Tato hodnota se odvíjí od maximální energie políček a hodnota v poli určuje, kolik procent této hodnoty políček je základní maximální energie buňek.
* **`MAX ENERGY SIZE PERCENTAGE`** Hodnota v poli udává, kolik procent aktuální velikosti buněk je použito jako úložný prostor pro energii buněk (buňky mají omezenou maximální energii).
* **`ENERGY EAT PERCENTAGE`** Hodnota v poli udává, kolik procent energie z cizí buňky získá buňka, která tuto cizí buňu pohltí.
* **`BASE SIZE GAIN PERCENTAGE`** Hodnota v poli udává, kolik procent své maximální velikosti buňky každý cyklus získají.
* **`AROUND SIZE GAIN PERCENTAGE`** Hodnota v poli udává, kolik procent své maximální velikosti buňky každý cyklus získají navíc. Tato hodnota závisí na volných okolních políčkách a to tak, že se vynásobí zlomkem hodnoty od 0 do 1, který udává podíl volných políček ku 6 (tj. ku všem okolním políčkám).
* **`SIZE EAT PERCENTAGE`** Hodnota v poli udává, kolik procent velikosti z cizí buňky získá buňka, která tuto cizí buňku pohltí.
* **`SHARE MUTATION CHANGE PERCENTAGE`** Hodnota v poli udává, o jakou hodnotu se nejvýše může při mutaci změnit procento sdílené energie akce *sdílení energie*.
* **`MIN SHARE PERCENTAGE`** Hodnota v poli udává, jakou nejnižší hodnotu muže mít procento sdílené energie akce *sdílení energie*.
* **`MAX SHARE PERCENTAGE`** Hodnota v poli udává, jakou nejvyšší hodnotu může mít procento sdílené energie akce *sdílení energie*.
* **`MOVE ENERGY COST PERCENTAGE`** Hodnota v poli udává, kolik energie stojí akce *pohyb*. Tato hodnota se odvíjí od maximální energie políček a hodnota v poli určuje, kolik procent této hodnoty políček stojí akce *pohyb*.
* **`DIVIDE MUTATION CHANGE PERCENTAGE`** Hodnota v poli udává, o jakou hodnotu se nejvýše může při mutaci změnit procento předané energie a velikosti do nové buňky u akce *buněčné dělení*.
* **`MIN RESOURCES PERCENTAGE`** Hodnota v poli udává, kolik nejméně procent své energie a velikosti buňka předá nové buňce u akce *buněčné dělení*.
* **`MAX RESOURCES PERCENTAGE`** Hodnota v poli udává, kolik nejvíce procent své energie a velikosti buňka předá nové buňce u akce *buněčné dělení*.
* **`MUTATION CHANCE PERCENTAGE`** Hodnota v poli udává, jaká je procentuální šance, že nová buňka u akce *buněčné dělení* zmutuje. Pokud buňka zmutuje, tak má poloviční šanci, že zmutuje znovu a to se opakuje dokud mutuje.
* **`STRONG MUTATION CHANCE PERCENTAGE`** Hodnota v poli udává, jaká je procentuální šance, že při mutaci buňky dojde k silné mutaci, a to mutaci celé akce, podmínky nebo příštích stavů. Jinak proběhne slabá mutace pouze číselných hodnot akce nebo podmínky.
* **`DIVIDE ENERGY COST PERCENTAGE`** Hodnota v poli udává, kolik energie stojí akce *buněčné dělení*. Tato hodnota se odvíjí od maximální energie políček a hodnota v poli určuje, kolik procent této hodnoty políček stojí akce *buněčné dělení*.
* **`CON SIZE MUTATION CHANGE PERCENTAGE`** Hodnota v poli udává, o jakou hodnotu se může změnit kontrolní číslo v podmínce *podmínka velikosti*. Tato hodnota se odvíjí od maximální velikosti buňěk a hodnota v poli určuje, kolik procent této hodnoty buněk je nejvyšší možná změna v podmínce.
* **`CON EN MUTATION CHANGE PERCENTAGE`** Hodnota v poli udává, o jakou hodnotu se může změnit kontrolní číslo v podmínce *podmínka energie*. Tato hodnota se odvíjí od maximální energie políček a hodnota v poli určuje, kolik procent této hodnoty políček je nejvyšší možná změna v podmínce.

## Ovládání posuvníků a polí s hodnotami
Hodnotu posuvníku lze měnit buďto kliknutím nad nebo pod držadlo (pro preciznější změnu), nebo posouváním držadla se stisknutým levým tlačítkem myši. Hodnotu pole s hodnotou lze měnit buďto kliknutím na šipky na pravém okraji pole, nebo přímým zadáním hodnoty do pole.
