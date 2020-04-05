import codecs
import csv
import datetime
import sqlite3
import sys
import time

import dataBase as db
from bankCSV import bankinfo

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
    return sv.fetchone()[0]


def get_last_dbIndexes(period):
    """Funktio lukee kannasta annetun (period) tilikauden viimeisimmät id:nrot """
    sv.execute('SELECT max(id) FROM document')
    last_doc_id = sv.fetchone()[0]
    sv.execute(f'SELECT max(number) FROM document WHERE period_id = {period}')
    last_doc_number = sv.fetchone()[0]
    sv.execute('SELECT max(id) FROM entry')
    last_ent_id = sv.fetchone()[0]
    return last_doc_id, last_doc_number, last_ent_id


# Luetaan kannasta tilikausien määrä ja ajat
svtk = sqlite3.connect(dbName)
svtk.row_factory = sqlite3.Row
sv = svtk.cursor()
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
    print("[{}] {} - {} Lukittu: {}".format(periodsInDb[y].id, datetime.datetime
                                            .utcfromtimestamp(periodsInDb[y].startDate / 1000)
                                            .strftime("%d.%m.%Y"), datetime.datetime.
                                            utcfromtimestamp(periodsInDb[y].endDate / 1000).strftime("%d.%m.%Y"),
                                            periodsInDb[y].locked))

print()

while True:
    try:
        period = int(input("anna tilikausi: "))
        if validPeriods.count(period) != 1 or periodsInDb[validPeriods.index(period, 0, len(validPeriods))].locked != 0:
            print(f"{period} ei ole validi tai on lukittu ", end='')
            continue
        else:
            break
    except:
        print("Syöttämäsi arvo ei kelpaa")
        continue

print(f'Valittu tilikausi \033[1;33;48m{period}\033[1;37;48m')

print("Valitse tapahtumaluettelon (.csv) malli")
print()
print("[1] - Osuuspankki")
print("[2] - Danske Bank")
print("[3] - Nodrea (ei käytössä vielä)")
print("[4] - Määrittele itse")
print("[9] - Lopeta")
print()

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
        elif bank == 9:
            print("Lopetetaan")
            sys.exit()
        else:
            print('Antamasi arvo ei ole validi ')
            continue
    except:
        print('Antamasi arvo ei ole validi ')
        continue
    else:
        break

with codecs.open(csvName, encoding='unicode_escape') as csvfile:
    reader = csv.reader(csvfile, delimiter = bank.get('delimiter'))
    csvData = list(reader)
    print(f"Löytyi {len(csvData[0])} Saraketta")
    print()
    for i, itm in enumerate(csvData[0]):
        print(f"[{i}]  {itm}")

# csv sarakkeiden mäppäys

print()
tapahtumaTili = 0000
vastaTili = 0000
DocList=[]
LastDocId = get_last_dbIndexes(period)[0]
LastDocNum = get_last_dbIndexes(period)[1]
LastEntId = get_last_dbIndexes(period)[2]

# Luetaan tapahtumat csv sisään ja lisätään DocList-listaan.
for i, row in enumerate(csvData):
    # skipataan otsikkorivi
    if i == 0:
        pass
    else:
        print("{}, {}, {} ".format(row[bank.get('datecol')], row[bank.get('sumcol')], row[bank.get('descol')]))
        # testataan onko vienti ulos vai sisään
        # if float(row[tapahtumaDebitSarake].strip().replace(',', '.').replace(' ', '')) > 0:
        if str(row[bank.get('sumcol')]).find("-") >= 0:
            debit = True  # jos rahaa sisään debet tapahtumatilille
        else:
            debit = False  # jos rahaa ulos kredit tapahtumatilille

        # muokataan tapahtuman päivämäärä oikeaan muotoon
        ts_pvm = int(time.mktime(datetime.datetime.strptime(f"{row[bank.get('datecol')]}", bank.get('timeformat'))
                               .timetuple()) * 1000)
        if ts_pvm < periodsInDb[validPeriods.index(period)].startDate or ts_pvm > periodsInDb[
            validPeriods.index(period)].endDate:
            print("Vienti ei ole annetulla tilikaudella")
            continue

        # pyydetään tapahtumalle tapahtumatili ja testataan että annettu tili on kannassa
        while True:
            try:
                tapahtumaTili = input(f'Syötä tapahtumatili [{tapahtumaTili}]: ') or tapahtumaTili
                # Haetaan kannasta tilinumeroa vastaava id
                tapahtumaTiliId = get_account_id(tapahtumaTili)
            except:
                print('Syöttämäsi tilinumero ei kelpaa')
                continue
            else:
                break

        # pyydetään tapahtumalle vastatili ja testataan että annettu tili on kannassa
        while True:
            try:
                vastaTili = input(f'Syötä vastatili [{vastaTili}]: ') or vastaTili
                # Haetaan kannasta tilinumeroa vastaava id
                vastaTiliId = get_account_id(vastaTili)
            except:
                print('Syöttämäsi tilinumero ei kelpaa')
                continue
            else:
                break

        # Lisätää Doclist listaan tapahtuman dokumentti (class document)
        DocList.append(db.dbDocument(LastDocId + i, LastDocNum + i, period, ts_pvm))
        # lisätään Doclist dokumentille tapahtuman entryt (class document.entries class entry)
        DocList[-1].add_entry(
            db.dbEntry(LastEntId + i * 2 - 1, LastDocId + i, tapahtumaTiliId, debit, row[bank.get('sumcol')],
                       row[bank.get('descol')], 0, 0))
        DocList[-1].add_entry(
            db.dbEntry(LastEntId + i * 2, LastDocId + i, vastaTiliId, not debit, row[bank.get('sumcol')],
                       row[bank.get('descol')], 1, 0))

# tulostetaan SQL rivit näytölle tarkastamista varten

for itm in DocList:
    print(itm.prepare_insert())
    for ent in itm.entries:
        print(ent.prepare_insert())

# Varmistetaan kirjoitus kantaan
kirjoitus = input("Yllä olevat rivit lisätään kantaan Y/N : ")

# Lisätään rivit kantaan
if kirjoitus == "y" or kirjoitus == "Y":
    print('kirjoitetaan ', end='')
    for itm in DocList:
        sv.execute(itm.prepare_insert())
        for ent in itm.entries:
            sv.execute(ent.prepare_insert())
        print(".", end='')
        time.sleep(0.2)
    svtk.commit()
    print()
else:
    print('lopetetaan')
    sys.exit()

svtk.close()

print("Valmis.")
