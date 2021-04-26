### tilitin_import.py lyhyt käyttöohje

Käyttö:

> python3 tilitin_import.py [tilitin_tietokanta.sqlite] [tapahtumat_csv.csv]

Luetaan valmiit pankkien csv mallit:



>Löytyi seuraavat csv mallit: 
> 
>------------------------------ 
>1 - op  
>2 - danske   
>  
>u - syötä uusi, d - poista  
> 
>------------------------------  
>Valitse malli
>Valitse: 


Valitse malli tai syötä uusi (u) tai poista olemassa oleva (d):


>Valitse: u  
>Syötä uusi pankkimalli:  
>Pankin nimi: pop     
>Kenttäerotin [,]:   
>Timeformat [%d.%m.%Y]:     
>Päivämäärän sarake [0]:   
>Summan sarake [2]:      
>Kuvauksen sarake [1]:       
>Desimaalierotin [,]:    
>
> 
> -----------------------     
>Pankkimalli pop:         
>delimiter : ,         
>timeformat : %d.%m.%Y    
>datecol : 0            
>sumcol : 2           
>descol : 1             
>decimal : ,          
>Tallenna k/e: k       


tai poista olemassa oleva (d):


>Valitse: d
>Valitse poistettava pankkimalli, 'q'-lopettaa: q


Anna tilinumerot joille viennit tehdään. Vastatilinä voi käyttää väliaikaista tiliä, 
josta siirtää tapahtumat oikeille tileille tilittimessä. Tai esimerkiksi tiliä jolle enen osa tapahtumista kuuluu, 
jolloin työtä tilittimessä on vähemmän.


>Tapahtumat viedään kantaan tapahtumatilille ja väliaikaiselle vastatilille
>Anna tili, jolle tapahtumat viedään (tapahtimatili): 1911
>Anna vastatili, jolle vienti tehdään (esim.8999): 8999


Luetaan kannasta tilikaudet ja valitaan uusin tilikausi, jolle tapahtumat viedään. valitse 'k' mikäli tilikausi oikein

>
>Kannasta löytyvät seuraavat tilikaudet:   
>ID   Vuosi   Lukittu     
> --  -----   ------- 
> 1   2020    Ei          
>
>Uudet tapahtumat lisätään tilikaudelle 1    
>Jatka k/e [k]: k               


Tulostetaan rivit wennen kantaan vientiä  
DOC = DokumenttiId kannassa  
DNO = Dokumenttinumero  
DATE = Tapahtumapäivä  
PER = Tilikauden Id  
ENT = Viennin Id  
ROW = Viennin dokumenttirivi  
ACC = TilinId  
DEB = 0 jos rahaa ulos, 1 jos sisään.  
SUM = Summa  
DESC = Kuvaus  



> DOC DNO   DATE    PER ENT DOC ROW ACC DEB        SUM  DESC
>
>-----------------------------------------------------------------------------------
> 125 124 27.12.2020   1 247 125   1  12   0    -620.00  Selite 1
> 125 124 27.12.2020   1 248 125   2  12   1     620.00  Selite 1
> 126 125 20.10.2020   1 249 126   1  12   0   -1146.13  Selite 2
> 126 125 20.10.2020   1 250 126   2  12   1    1146.13  Selite 2
> 127 126 06.10.2020   1 251 127   1  12   0    -207.60  Selite 3
> 127 126 06.10.2020   1 252 127   2  12   1     207.60  Selite 3
> 128 127 07.09.2020   1 253 128   1  12   0    -127.94  Selite 4
> 128 127 07.09.2020   1 254 128   2  12   1     127.94  Selite 4
> 129 128 03.09.2020   1 255 129   1  12   1     915.00  Selite 5
> 129 128 03.09.2020   1 256 129   2  12   0    -915.00  Selite 5
> 130 129 05.07.2020   1 257 130   1  12   1     132.60  Selite 6
> 130 129 05.07.2020   1 258 130   2  12   0    -132.60  Selite 6
> 131 130 16.06.2020   1 259 131   1  12   0    -148.80  Selite 7
> 131 130 16.06.2020   1 260 131   2  12   1     148.80  Selite 7
> 132 131 15.06.2020   1 261 132   1  12   1     172.60  Selite 8
> 132 131 15.06.2020   1 262 132   2  12   0    -172.60  Selite 8
> 133 132 08.06.2020   1 263 133   1  12   1      79.60  Selite 9
> 133 132 08.06.2020   1 264 133   2  12   0     -79.60  Selite 9
>-----------------------------------------------------------------------------------
>
>Kirjoitetaanko tiedot kantaan ? k/e : k
>Kirjoitetaan... |################################| 27/27
 
