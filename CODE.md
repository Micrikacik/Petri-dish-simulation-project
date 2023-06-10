# Kód
Popis základního fungování programu (celé je to jeden velký mišmaš tříd). Všechny funkce i třídy jsou jednoduše popsané v kódu. O zobrazování se stará knihovna Tkinter.
## Mřížka (class Hex_Grid)
Třída Hex_Grid představuje svět, nebo herní pole simulace. Je zde uložen 2D seznam jedinečných tříd políček (class Hex_Tile). Třída navíc obsahuje funkce pro manipulaci s mřížkou, jako přidání a odebrání buňky, doplnění energie políčkům v mřížce apod. Třída také počítá některé statistické údaje. Mřížky jsou používány dvě. Jedna slouží k ověřování podmínek a použití akce *sdílení energie* v daném cyklu a nemění se do konce cyklu, díky tomu všechny buňky vycházejí při vyhodnocování podmínek ze stejného základu. Druhá slouží k aplikování změn provedených v daném cyklu, jako pohyb, vytvoření buňky dělením apod. Na konci cyklu proběhne pohlcování buňěk, pokud jich je více na stejném políčku, a doplnění energie políček. Jakmile je vše dokončeno, tak se první mřížka aktualizuje, aby odpovídala druhé.
### Políčko (class Hex_Tile)
Třída Hex_Tile představuje políčko mřížky simulace, Na každém políčku tak můžou být uloženy informace jako množství energie na políčku, buňky na políčku, jaký obrázek má políčko reprezentovat apod.
### Souřadnice (class Hex_Pos)
Třída představující souřadnice v mřížce. Souřadnice jsou hexagonální, jsou 3 ale třetí je určena druhýma dvěma. Tyto souřadnice se dají sčítat jako vektory. První souřadnice udává řádek odshora, druhá udává šikmou řadu od levé dolní části mřížky a třetí udává šikmou řadu od levé horní části mřížky. Blíže vysvětleno na stránkách https://www.redblobgames.com/grids/hexagons/. Souřadnice okolních políček relativně vůči prostřednímu:

![Obrázek souřadnicového systému](/Petri_dish_simulation/Sprites/Coordinates.png)
## Buňky (class Cell)
Třída Cell představuje buňku. Ke každé buňce je přiřazen seznam tříd jejích stavů (class Cell_State). Tento seznam a třídy stavů jsou jedinečné pro jednu buňku. Všechny buňky v jednom experimentu a jejich stavy mají odkaz na jednu jedinoučnou instanci třídy Cell_And_State_Settings, která udržuje informace o nastavení experimentu, jako např. cena pohybu, šance na mutaci, rychlost růstu apod. a tyto informace jsou nastavovány uživatelem.
### Stavy buněk (class Cell_State)
Třída Cell_State představje stav buňky. Obsahuje odkazy na jedinečné třídy akce (class State_Action) a podmínky (class State_Condition) a umožňuje interakci s nimi.
### Akce (class State_Action)
Třída State_Action představuje akci buňky. Je to základní třída, ze které dědí speciální třídy konkrétních akcí.
### Podmínka (class State_Condition)
Třída State_Condition představuje akci buňky. Je to základní třída, ze které dědí speciální třídy konkrétních podmínek.
## Experiment (class Dish_Experiment)
Třída Dish_Experiment představuje simulovaný "experiment". Třída se stará o průběh cyklů simulace, nezajištuje ale jejich opakování, musí být proto obsluhována dokola vnějším cyklem (zde je cyklus někde v Tkinteru a ten udržuje chod simulace). Dále třída poskytuje a počítá statistické údaje.
## Laboratoř (class Laboratory)
Třída Laboratory představuje "laboratoř s experimentem". Stará se o zobrazování (prostřednictvím Tkinteru) všeho potřebného a o uživatelský vstup.
