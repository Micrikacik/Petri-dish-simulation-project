# Simulace
Popis jak probíhá simulace Petriho misky.
## Časový průběh
Simulace je rozdělena do cyklů. V každém cyklu proběhne simulace celé Petriho misky. Program mezi cykly dělá časové prodlevy, aby bylo možné interagovat se simulací a pozorovat její průběh.
### Průběh cyklu
1. Buňky vstřebají energii z políčka, na kterém se nachází a ztratí energii za existenci a navíc ztratí energii za každé políčko bez buňky okolo. Pokud bude mít buňka ve výsledky nula a méně energie, tak zahyne.
2. Buňky vyrostou a navíc vyrostou za každé políčko bez buňky okolo (tento bonusový růst je však základně nastaven na 0). Pokud bude mít buňka 10000 a větší velikost, tak zahyne.
3. Buňky provedou akci svého aktuálního stavu.
4. Buňky zkontrolují podmínku svého aktuálního stavu.
5. Buňky podle výsledku předchozího kroku a svého aktuálního stavu přejdou do jiného stavu.
6. Buňky, které skončily na jednom políčku jsou pohlceny největší buňkou na tomto políčku.
7. Vybraným políčkám v Petriho misce se obnový část energie.
## Stavba buněk
Každá buňka má energii, velikost, reprezentační obrázek a 10 možných stavů, přičemž v každém cyklu simulace je aktivní právě jeden stav.
### Stavy
Každý stav má akci, podmínku a výstupní stavy.
#### Akce stavů
* *
