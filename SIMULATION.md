# Simulace
Popis jak probíhá simulace Petriho misky.
## Časový průběh
Simulace je rozdělena do cyklů. V každém cyklu proběhne simulace celé Petriho misky. Program mezi cykly dělá časové prodlevy, aby bylo možné interagovat se simulací a pozorovat její průběh.
### Průběh cyklu
1. Buňky vstřebají energii z políčka, na kterém se nachází a ztratí energii za existenci a navíc ztratí energii za každé políčko bez buňky okolo. Pokud bude mít buňka ve výsledky nula a méně energie, tak zahyne.
2. Buňky vyrostou a navíc vyrostou za každé políčko bez buňky okolo (tento bonusový růst je však základně nastaven na 0). Pokud bude mít buňka 10000 a větší velikost, tak zahyne.
3. Buňky provedou akci svého aktuálního stavu. Poku buňka nemůže akci provést (např. nemá dost energie), tak ji neprovede.
4. Buňky zkontrolují podmínku svého aktuálního stavu.
5. Buňky podle výsledku předchozího kroku a svého aktuálního stavu přejdou do jiného stavu.
6. Buňky, které skončily na jednom políčku jsou pohlceny největší buňkou na tomto políčku.
7. Vybraným políčkám v Petriho misce se obnový část energie.
## Stavba buněk
Každá buňka má energii, velikost, reprezentační obrázek a 10 možných stavů, přičemž v každém cyklu simulace je aktivní právě jeden stav.
### Stavy
Každý stav má akci, podmínku a výstupní stavy.
#### Akce stavů
* *odpočinek*  Buňka nedělá nic speciálního.
* *pohyb* Buňka spotřebuje energii a pohne se o jedno políčko v daném směru. Může se pohnout na políčko s buňkou.
* *buněčné dělení* Buňka spotřebuje energii a vytvoří novou buňku na daném okolním políčku, přičemž část své energie a velikosti dá této nové buňce. Nová buňka se může vytvořit na políčku s buňkou. Nová buňka má stavy stejné jako původní buňka ale je šance, že se nějak (ne příliš) její stavy pozmění. Může se změnit buďto celá akce, podmínka či výstupní stavy, nebo se změní jen hodnoty v akci či podmínce (např. směr a jiné)
* *sdílení energie*
#### Podmínky stavů
* *podmínka energie*
* *podmínka velikosti*
* *podmínka senzoru*
