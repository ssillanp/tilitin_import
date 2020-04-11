# tilitin_import

Python script for importing bank csv into tilitin ( a finnish bookkeeping app)
Thanks to T.Helineva about the really handy Tilitin App.

This code is distributed under the The GNU GPLv3. A copy of the licence is in COPYING.txt  


Python skripti pankin csv-muotoisen tapahhtumaluettelon lisäämiseksi tilitin-kantaan.

HUOM!
Luo kannasta kopio, ennen kuin käytät. Kaikki vastuu mahdollisista virheistä ja tietojen hukkaamisista käyttäjällä

Testattu python 3.7. Ei toimi python 2.x tai vanhemmilla

Pankkimallit OP ja Danske, lisäksi csv:n mallin voi syöttää käsin.


Käyttö
>python3 tilitin_import.py [tilitin_kanta.sqlite] [pankki.csv]

Kannassa tulee olla lukitsemattomia tilikausia. 
Mikäli tuot tapahtumat uudelle kaudelle, luo uusi tilikausi tilittimessä, jotta alkusaldot ovat oikein.
