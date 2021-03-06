#!/usr/bin/python3

import codecs
import csv
import datetime
import sqlite3
import sys
import time
import os

import tilitindb as db
from bankinfo import bankinfo

os.system('clear')

# Kanta ja csv argumentteina
args = sys.argv[1:]
if len(args) == 2:
    dbName = str(args[0])
    csvName = str(args[1])
else:
    print("Usage: python3 tilitin_import.py [database] [csv]")
    sys.exit()


def get_account_id(account_no):
    """Funktio hakee kannasta tilin id:n annetun  tilinumeron perusteella"""
    sv.execute(f'SELECT id FROM account WHERE number = {account_no}')
    result = sv.fetchone()[0]
    return result

def get_account_name(account_id):
    """Funktio hakee kannasta tilin nimen annetun  id:n perusteella"""
    sv.execute(f'SELECT name FROM account WHERE id = {account_id}')
    result = sv.fetchone()[0]
    return result


def get_last_dbIndexes(period):
    """Funktio lukee kannasta annetun (period) tilikauden viimeisimmät id:nrot """
    sv.execute('SELECT max(id) FROM document')
    last_doc_id = sv.fetchone()[0]
    sv.execute(f'SELECT max(number) FROM document WHERE period_id = {period}')
    last_doc_number = sv.fetchone()[0]
    sv.execute('SELECT max(id) FROM entry')
    last_ent_id = sv.fetchone()[0] or 0
    return last_doc_id, last_doc_number, last_ent_id

# Yhdistetään kantaan
svtk = sqlite3.connect(dbName)
svtk.row_factory = sqlite3.Row
sv = svtk.cursor()

# Luetaan kannasta tilikausien määrä ja ajat
sv.execute('SELECT * FROM period')
r = sv.fetchall()
print(f'Tietokannassa \033[1;33;48m{dbName.split("/")[-1]}\033[1;37;48m on tilikausia '
      f'\033[1;33;48m{len(r)}\033[1;37;48m'f' kappaletta')
print()
periodsInDb=[]
validPeriods=[]

for y, itm in enumerate(r):
    periodsInDb.append(db.dbPeriod(tuple(itm)[0], tuple(itm)[1], tuple(itm)[2], tuple(itm)[3]))
    validPeriods.append(tuple(itm)[0])
    print("\033[1;33;48m[{}] {} - {} Lukittu: {}".format(periodsInDb[y].id, datetime.datetime
                                            .utcfromtimestamp(periodsInDb[y].startDate / 1000)
                                            .strftime("%d.%m.%Y"), datetime.datetime.
                                            utcfromtimestamp(periodsInDb[y].endDate / 1000).strftime("%d.%m.%Y"),
                                            periodsInDb[y].locked))

print("\033[1;37;48m")

while True:
    try:
        period = int(input("Anna tilikausi: "))
        if validPeriods.count(period) != 1 or periodsInDb[validPeriods.index(period, 0, len(validPeriods))].locked != 0:
            print(f"{period} ei ole validi tai on lukittu")
            continue
    except KeyboardInterrupt:
        raise
    except (TypeError, ValueError):
        print("Syöttämäsi arvo ei kelpaa")
        continue
    else:
        break

print(f'Valittu tilikausi \033[1;33;48m{period}\033[1;37;48m')

print("Valitse tapahtumaluettelon (.csv) malli")
print("\033[1;33;48m")
print("[1] - Osuuspankki")
print("[2] - Danske Bank")
print("[3] - Nodrea (ei käytössä vielä)")
print("[4] - Määrittele itse")
print("\033[1;37;48m")

bi = bankinfo()

while True:
    try:
        bank = int(input("valitse: "))
        if bank == 1:
            bank = bi.op
        elif bank == 2:
            bank = bi.danske
        elif bank == 4:
            bank = bi.user_defined()
        else:
            print('Antamasi arvo ei ole validi ')
            continue
    except KeyboardInterrupt:
        raise
    except (TypeError, ValueError):
        print('Antamasi arvo ei ole validi ')
        continue
    else:
        break

with codecs.open(csvName, encoding='unicode_escape') as csvfile:
    reader = csv.reader(csvfile, delimiter=bank.get('delimiter'))
    csvData = list(reader)
    print(f"Löytyi {len(csvData[0])} Saraketta")
    print("\033[1;33;48m")
    for i, itm in enumerate(csvData[0]):
        print(f"[{i}]  {itm}")


# csv sarakkeiden mäppäys
print("\033[1;37;48m")
tapahtumaTili = 0000
vastaTili = 0000
DocList=[]
LastDocId = get_last_dbIndexes(period)[0]
LastDocNum = get_last_dbIndexes(period)[1]
LastEntId = get_last_dbIndexes(period)[2]

print("Voit syöttää joko vain tapahtumatilin ja antaa vastatilit tilittimessä,")
print("tai voit syöttää myös vastatilit nyt")
print()
print("[1] - Vain tapahtumatili, vastatilit tilittimessä")
print("[2] - Myös vastatilit nyt")
print()

while True:
    try:
        tapa = int(input("Valitse [1]: ")) or 1
        if tapa != 1 and tapa != 2:
            print("Valitse joko 1, tai 2")
            continue
    except KeyboardInterrupt:
        raise
    except (TypeError, ValueError):
        print("Valitse joko 1, tai 2")
        continue
    else:
        break

if tapa == 1:
    # pyydetään tapahtumalle tapahtumatili ja testataan että annettu tili on kannassa
    while True:
        try:
            tapahtumaTili=input(f'Syötä tili jolle tapahtumat viedään: ')
            # Haetaan kannasta tilinumeroa vastaava id
            tapahtumaTiliId=get_account_id(tapahtumaTili)
        except KeyboardInterrupt:
            raise
        except (TypeError, ValueError, sqlite3.OperationalError):
            print('Syöttämäsi tilinumero ei kelpaa')
            continue
        else:
            break
# Poistetaan csv header rivi
csvData.remove(csvData[0])

# Sortataan lista vanhimmasta uusimpaan.
csvData.sort(key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y') )

# Luetaan tapahtumat sisään ja lisätään DocList-listaan.
for i, row in enumerate(csvData):
    print("\033[1;34;48m{}, {}, {} \033[1;37;48m".format(row[bank.get('datecol')], row[bank.get('sumcol')], row[bank.get('descol')]))
    # testataan onko vienti ulos vai sisään
    if str(row[bank.get('sumcol')]).find("-") >= 0:
        debit = False  # jos rahaa sisään
    else:
        debit = True  # jos rahaa ulos

    # muokataan tapahtuman päivämäärä oikeaan muotoon
    # Huom. Kannassa ajan esitys muodossa int(timestamp*1000)
    try:
        ts_pvm = int(time.mktime(datetime.datetime.strptime(f"{row[bank.get('datecol')]}", bank.get('timeformat'))
                           .timetuple()) * 1000)
    except KeyboardInterrupt:
        raise
    except ValueError:
        print(f"Tiedoston {csvName.split('/')[-1]} timeformat muoto ei ole pankkimallin mukainen {bank.get('timeformat')}")
        print("lopetetaan...")
        sys.exit()
    # Testataan että tapahtuma ajoittuu tilikaudelle, jos ei skipataan
    if ts_pvm < periodsInDb[validPeriods.index(period)].startDate or ts_pvm > periodsInDb[
        validPeriods.index(period)].endDate:
        print("\033[1;31;48mVienti ei ole annetulla tilikaudella, skipataan...\033[1;37;48m")
        continue

    # pyydetään tapahtumalle tapahtumatili ja testataan että annettu tili on kannassa
    if tapa != 1 or tapahtumaTili == 0:
        while True:
            try:
                tapahtumaTili = input(f'Syötä tapahtumatili [\033[1;32;48m{tapahtumaTili}\033[1;37;48m]: ') or tapahtumaTili
                # Haetaan kannasta tilinumeroa vastaava id
                tapahtumaTiliId=get_account_id(tapahtumaTili)
            except KeyboardInterrupt:
                raise
            except (TypeError, ValueError, sqlite3.OperationalError):
                print('Syöttämäsi tilinumero ei kelpaa')
                continue
            else:
                break

    if tapa != 1:
        # pyydetään tapahtumalle vastatili ja testataan että annettu tili on kannassa
        while True:
            try:
                vastaTili = input(f'Syötä vastatili ("s" skippaa) [\033[1;32;48m{vastaTili}\033[1;37;48m]: ') or vastaTili
                # Haetaan kannasta tilinumeroa vastaava id
                if vastaTili == "s":
                    break
                vastaTiliId=get_account_id(vastaTili)
            except KeyboardInterrupt:
                raise
            except (TypeError, ValueError, sqlite3.OperationalError):
                if vastaTili == "s":
                    break
                print('Syöttämäsi tilinumero ei kelpaa')
                continue
            else:
                break

    # Lisätää Doclist listaan tapahtuman dokumentti (class document)
    DocList.append(db.dbDocument(LastDocId + i + 1, LastDocNum + i + 1, period, ts_pvm))
    # lisätään Doclist dokumentille tapahtuman entryt (class document.entries class entry)
    DocList[-1].add_entry(
        db.dbEntry(LastEntId + i + 1, LastDocId + i + 1, tapahtumaTiliId, debit, row[bank.get('sumcol')],
                   row[bank.get('descol')], 0, 0))
    if vastaTili =="s" or tapa == 1:
       LastEntId += 1
       pass
    else:
        DocList[-1].add_entry(
            db.dbEntry(LastEntId + i + 2, LastDocId + i + 1, vastaTiliId, not debit, row[bank.get('sumcol')],
                       row[bank.get('descol')], 1, 0))
        LastEntId += 1

# tulostetaan SQL rivit näytölle tarkastamista varten
os.system('clear')

print("\033[1;32;48mKirjoitetaanko seuraavat rivit kantaan:")

for doc in DocList:
    print("------------------------------------------------------")
    print(f"{doc.prepare_insert()} \033[1;34;48m-> Dokumentille {doc.number}, "
          f"Vientipäivämäärä {datetime.datetime.utcfromtimestamp(doc.doc_date / 1000).strftime('%d.%m.%Y')}\033[1;32;48m")

    for ent in doc.entries:
        print(f" {ent.prepare_insert()} \033[1;34;48m-> {ent.amount}EUR, "
              f"Tili: {get_account_name(ent.account_id)}, Selite: {ent.description}\033[1;32;48m")

print("\033[1;37;48m")

# Varmistetaan kirjoitus kantaan
kirjoitus = input("Kirjoita Y/N : ")

# Lisätään rivit kantaan
if kirjoitus == "y" or kirjoitus == "Y":
    print('\033[1;33;48mkirjoitetaan', end='')
    for itm in DocList:
        sv.execute(itm.prepare_insert())
        for ent in itm.entries:
            sv.execute(ent.prepare_insert())
        print(".", end='')
        time.sleep(0.2)
    svtk.commit()
    print()
else:
    print('lopetetaan\033[1;37;48m')
    sys.exit()

svtk.close()

print("Valmis.")
