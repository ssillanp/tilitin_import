tilitin_import.py lyhyt käyttöohje

Käyttö:
>python3 tilitin_import.py [tilitin_tietokanta.sqlite] [tapahtumat_csv.csv]

Skripti lukee kannasta tilikaudet ja tulostaa ne ruudulle:


>Tietokannassa kanta.sqlite on tilikausia 4 kappaletta
>
>[2] 31.12.2015 - 30.12.2016 Lukittu: 1
>[4] 31.12.2016 - 30.12.2017 Lukittu: 1
>[5] 31.12.2017 - 30.12.2018 Lukittu: 0
>[6] 31.12.2018 - 30.12.2019 Lukittu: 0
>
>Anna tilikausi: 6

Syötä käytettävän tilikauden numero. Kausi ei saa olla lukittu. Mikäli tuot tapahtumat uudelle tilikaudelle,
luo se ensi tilittimessä, jotta alkusaldot tulevat oikein.
Seuraavaksi skripti kytyy käytettänän pankin csv mallin:

>Valittu tilikausi 6
>Valitse tapahtumaluettelon (.csv) malli
>
>[1] - Osuuspankki
>[2] - Danske Bank
>[3] - Nodrea (ei käytössä vielä)
>[4] - Määrittele itse
>
>valitse: 2

Anna valittu malli tai syötä arvot itse, valitsemalla [4]. Malli pitää sisällään
- csv:n erottimen "," tai ";"
- Päivämääräformaatin esim: "%d.%m.%Y" tai "%m/%d/%y"
- Päivämääräsarakkeen numeron
- Summasarakkeen numeron
- Desc-sarakkeen numeron (esim: maksaja/saaja)

>Löytyi 6 Saraketta
>
>[0]  Pvm
>[1]  Saaja/Maksaja
>[2]  Mara
>[3]  Saldo
>[4]  Tila
>[5]  Tarkastus
>
>Voit syöttää joko vain tapahtumatilin ja antaa vastatilit tilittimessä,
>tai voit syöttää myös vastatilit nyt
>
>[1] - Vain tapahtumatili, vastatilit tilittimessä
>[2] - Myös vastatilit nyt
>
>Valitse [1]: 1

Skripti listaa löytyneet sarakkeet ja pyytää valitsemaan syöttötavan:
[1] - Syötä alussa tapahtumatili, jolle tapahtumat viedään, voit lisätä vastatilit tilittimessä.
[2] - Syötä tapahtumatilit ja vastatilit tässä.

Mikäli valitset 1, kysyy skripti tapahtumatilin numeron ja ajaa tapahtumat ko. tilille. 
Mikäli valitset 2, kysyy skripti jokaisen tapahtuman kohdalla tapahtuma- va vastatilin numeron. 
Skripti muistaa edellisen valinnan, jonka voi kuitata enterillä. Vatatilin syötön voi myös skipata valitsemalla "s".
  
>Syötä tili jolle tapahtumat viedään: 1911
>07.11.2019, -1566.76, Yritys A Oy 
>02.12.2019, -620, Kuljetus AB Oy 
>31.12.2019, -0.2, Lahdevero 
>31.12.2019, 0.73, Korko 
>17.02.2020, -334.8, Pekka Pee 
>Vienti ei ole annetulla tilikaudella, skipataan...
>Kirjoitetaanko seuraavat rivit kantaan:
>------------------------------------------------------
>INSERT INTO document VALUES (177, 42, 6, 1573077600000) -> Dokumentille 42, Vientipäivämäärä 06.11.2019
> INSERT INTO entry VALUES (351, 177, 12, 1, 1566.76, 'Yritys A Oy', 0, 0) -> 1566.76EUR, Tili: Pankkitili, Selite: Yritys A Oy
>------------------------------------------------------
>INSERT INTO document VALUES (178, 43, 6, 1575237600000) -> Dokumentille 43, Vientipäivämäärä 01.12.2019
> INSERT INTO entry VALUES (353, 178, 12, 1, 620.0, 'Kuljetus AB Oy', 0, 0) -> 620.0EUR, Tili: Pankkitili, Selite: Kuljetus AB Oy
>------------------------------------------------------
>INSERT INTO document VALUES (179, 44, 6, 1577743200000) -> Dokumentille 44, Vientipäivämäärä 30.12.2019
> INSERT INTO entry VALUES (355, 179, 12, 1, 0.2, 'Lahdevero', 0, 0) -> 0.2EUR, Tili: Pankkitili, Selite: Lahdevero
>------------------------------------------------------
>INSERT INTO document VALUES (180, 45, 6, 1577743200000) -> Dokumentille 45, Vientipäivämäärä 30.12.2019
> INSERT INTO entry VALUES (357, 180, 12, 0, 0.73, 'Korko', 0, 0) -> 0.73EUR, Tili: Pankkitili, Selite: Korko
>
>Kirjoita Y/N : 

Valitse Y,kirjoittaksesi tapahtumat tilitin kantaan.


