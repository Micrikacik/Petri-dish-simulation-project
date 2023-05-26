# Rozhraní
Popis jednotlivých částí okna zleva doprava, shora dolů.
## Petriho miska
Levá polovina okna zobrazuje petriho misku a buňky v ní. Umožňuje interakci s konkrétními buňkami.
Kliknutím levým tlačítkem myši na buňku se buňka označí, bude zvýrazněná a lze ji dočasně uložit (více v **Interakční tlačítka**) a zvlášť pozorovat (více v **Informace o buňkách**).
Kliknutím pravým tlačítkem myši lze na dané políčko vložit uloženou buňku, nebo smazat z daného políčka buňku (více v Interakční tlačítka).
## Experimenty
Pomocí tří tlačítek s nápisy **EXPERIMENT 1**, **EXPERIMENT 2**, **EXPERIMENT 3** lze přepínat mezi pozorovanými experimentry v Petriho miskách.
Aktuálně pozorovaný experiment má své tlačítko vybarvené červeně. Všechny experimenty jsou simulovány zvlášť, nezávisle na pozorovaném experimentu.
Pod třemi tlačítky jsou vypsány celkové počty buněk v jednotlivých experimentech.
## Interakční tlačítka
Sloupeček 4 tlačítek **FLUSH**, **KILL ALL**, **COPY**, **MODE: ---** slouží k základní interakci s experimentem.
* ### FLUSH
  Po stisknutí (levým tlačítkem myši) smaže pozorovaný experiment a změní se na tlačítko **CREATE**.
* ### CREATE
  Po stisknutí vytvoří nový experiment s náhodnými buňkami. Experiment lze nastavit v části okna **Počáteční nastavení**.
* ### KILL ALL
  Po stisknutí všechny buňky v pozorovaném experimentu zahynou.
* ### COPY
  Po sisknutí dočasně uloží (aktuálně jen po dobu běhu programu) označenou buňku. Aktuálně lze mít uloženou nejvýše jednu buňku.
* ### MODE: ---
  Po stisknutí změní funkci pravého tlačítka myši. Pokud je **MODE: PASTE**, tak pravé tlačítko myši vloží dočasně uloženou buňku na políčko v petriho misce
  na kterém je kurzor. Pokud je **MODE: KILL**, tak pravé tlačítko myši smaže buňku z políčka v petriho misce na kterém je kurzor. 
  
