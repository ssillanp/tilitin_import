# tilitin_import
Import script for importing bank csv to tilitin

Python skripti pankin csv-muotoisen tapahhtumaluettelon lisäämiseki tilitin-kantaan.

HUOM!
Luo kannasta kopio, ennen kuin käytät. Kaikki vastuu mahdollisista virheistä ja tietojen hukkaamisista käyttäjällä

Käyttö
>python3 tilitin_import.py [tilitin_kanta.sqlite] [pankki.csv]

Kannassa tulee olla lukitsemattomia tilikausia. 
Luo uusi tilikausi tilittimessä, jotta alkusaldot ovat oikein.
