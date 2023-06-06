# Simulace
Popis jak probíhá simulace Petriho misky.
## Časový průběh
Simulace je rozdělena do cyklů. V každém cyklu proběhne simulace celé Petriho misky. Program mezi cykly dělá časové prodlevy, aby bylo možné interagovat se simulací a pozorovat její průběh.
### Průběh cyklu
1. Buňky vstřebají energii z políčka, na kterém se nachází a ztratí energii za existenci a navíc ztratí energii za každé políčko bez buňky okolo. Pokud bude mít buňka ve výsledky nula a méně energie, tak zahyne.
2. Buňky vyrostou a navíc vyrostou za každé políčko bez buňky okolo (tento bonusový růst je však základně nastaven na 0). Pokud bude mít buňka 10000 a větší velikost, tak zahyne.
3. Buňky provedou akci svého aktuálního stavu. Pokud buňka nemůže akci provést (např. nemá dost energie), tak ji neprovede.
4. Buňky zkontrolují podmínku svého aktuálního stavu.
5. Buňky podle výsledku předchozího kroku a svého aktuálního stavu přejdou do jiného stavu.
6. Pokud je na jednom políčku více než jedna buňka, tak na tomto proběhne pohlcování.
7. Vybraným políčkám v Petriho misce se obnový část energie.
## Stavba buněk
Každá buňka má energii, velikost, reprezentační obrázek a 10 možných stavů, přičemž v každém cyklu simulace je aktivní právě jeden stav.
### Stavy
Každý stav má akci, podmínku a výstupní stavy.
#### Akce stavů
* *odpočinek*  Buňka nedělá nic speciálního.
* *pohyb* Buňka spotřebuje energii a pohne se o jedno políčko v daném směru. Může se pohnout na políčko s buňkou.
* *buněčné dělení* Buňka spotřebuje energii a vytvoří novou buňku na daném okolním políčku, přičemž část své energie a velikosti dá této nové buňce. Nová buňka se může vytvořit na políčku s buňkou. Nová buňka má stavy stejné jako původní buňka ale je šance, že se nějak (ne příliš) její stavy pozmění. Může se změnit buďto celá akce, podmínka či výstupní stavy, nebo se změní jen hodnoty v akci či podmínce (např. směr, kontrolní číslo apod.).
* *sdílení energie* Buňka rovnoměrně předá část své energie buňkám na okolních políčkách.
#### Podmínky stavů
* *podmínka energie* Kontrola, zda je energie buňky pod (nebo nad) určitou hranicí, která se nazývá kontrolní číslo.
* *podmínka velikosti* Kontrola, zda je velikost buňky pod (nebo nad) určitou hranicí, která se nazývá kontrolní číslo.
* *podmínka senzoru* Kontrola, zda dané okolní políčko splňuje podmínku. Ta může být: Je na políčku buňka? (neuvažuje stěny), Je políčko prázdné? (uvažuje stěny), Má políčko více energie naž má moje?.
#### Výstupní stavy
Jeden stav má 2 výstupní stavy A a B. Do stavu A se přejde pokud je podmínka splněna, do stavu B pokud splněna není.
## Mutování
Mutování může proběhnout pouze při akci *buněčné dělení* u nově vzniklé buňky. Mutování probíhá na jednom náhodně vybraném stavu buňky, a pokud se opakuje vícekrát při jednom dělení, tak může vícekrát ovlivnit jeden stav. Při mutaci stavu může nastat jedna z 5 možností:
* slabé mutování, číselně hodnoty se mohou změnit nejvýše o nastavené maximum změny:
  1. změna hodnot akce (jako směr, procento sdílení apod.)
  2. změna hodnot podmínky (jako směr, kontrolní číslo apod.)
* silné mutování:
  1. změna celé akce na jinou, náhodně vybranou
  2. změna celé podmínky na jinou, náhodně vybranou
  3. změna výstupních stavů na náhodně vybrané (mohou být stejné)
## Pohlcování
Největší buňka pohltí druhou největší, získá část její energie a velikosti a pokud je moc velká (nad 10000) tak zahyne. Poté se proces opakuje s (případně) aktuálně největší buňkou.
