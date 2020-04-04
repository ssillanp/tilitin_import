import sqlite3
import csv
import time
import datetime
import dataBase as db
import sys
import codecs

args = sys.argv[1:]
if len(args)==2:
    dbName = str(args[0])
    csvName = str(args[1])
else:
    print("Usage: python3 tilitin_import.py [database] [csv]")
    sys.exit()

def get_account_id(account_no):
    sv.execute(f'SELECT id FROM account WHERE number = {account_no}')
    return sv.fetchone()[0]


# SELECT number FROM document WHERE number=(SELECT max(number) FROM document WHERE period_id = 4)
# SELECT id FROM document WHERE id=(SELECT max(id) FROM document WHERE period_id = 4)

def get_last_dbIndexes(period):
    sv.execute('SELECT max(id) FROM document')
    last_doc_id=sv.fetchone()[0]
    sv.execute(f'SELECT max(number) FROM document WHERE period_id = {period}')
    last_doc_number=sv.fetchone()[0]
    sv.execute('SELECT max(id) FROM entry')
    last_ent_id=sv.fetchone()[0]
    return last_doc_id, last_doc_number, last_ent_id


# Ava tiliote / tilitapahtuma .csv
# tämä malli dansken tapahtuma csv
svtk=sqlite3.connect(dbName)
svtk.row_factory=sqlite3.Row
sv=svtk.cursor()
sv.execute('SELECT * FROM period')  # ORDER BY id DESC')
r=sv.fetchall()
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
period=int(input("Valitse käytettävä tilikausi: "))
# Testi että valittu tk on ok.
periodOk=False
while periodOk == False:
    # Onko tk olemassa
    if validPeriods.count(period) != 1:
        period=int(input(f"{period} ei ole validi, Valitse käytettävä tilikausi: "))
    # onko tk lukittu
    elif periodsInDb[validPeriods.index(period, 0, len(validPeriods))].locked != 0:
        period=int(input(f"{period} on lukittu, valitse toinen tilikausi: "))
    else:
        periodOk=True

print(f'Valittu tilikausi \033[1;33;48m{period}\033[1;37;48m')

print("Valitse tapahtumaluettelon (.csv) malli")
print()
print("[1] - Osuuspankki")
print("[2] - Danske Bank")
print("[9] - Lopeta")
print()

bankOk=False
tmFormat=""
dlmtr= ","
tapahtumaPvmSarake=0
tapahtumaDebitSarake=0
tapahtumaDescSarake=0

bank=int(input("Valitse: "))
while bankOk == False:
    if bank == 1:
        dlmtr=";"
        tapahtumaPvmSarake=0
        tapahtumaDebitSarake=2
        tapahtumaDescSarake=5
        bankOk=True
        tmFormat='%d.%m.%Y'
    elif bank == 2:
        dlmtr=","
        tapahtumaPvmSarake=0
        tapahtumaDebitSarake=2
        tapahtumaDescSarake=1
        bankOk=True
        tmFormat='%d.%m.%Y'
    elif bank == 9:
        print("Lopetetaan")
        sys.exit()
    else:
        bank=int(input(f"{bank} ei ole validi, valitse: "))

with codecs.open(csvName, encoding='unicode_escape') as csvfile:
    reader=csv.reader(csvfile, delimiter=dlmtr)
    csvData=list(reader)
    print(f"Löytyi {len(csvData[0])} Saraketta")
    print()
    for i, itm in enumerate(csvData[0]):
        print(f"[{i}]  {itm}")

# csv sarakkeiden mäppäys


print()
tapahtumaTili=1911
vastaTili=4101
DocList=[]
LastDocId=get_last_dbIndexes(period)[0]
LastDocNum=get_last_dbIndexes(period)[1]
LastEntId=get_last_dbIndexes(period)[2]
print(LastDocId)
print(LastDocNum)
print(LastEntId)

for i, row in enumerate(csvData):
    # skipataan otsikkorivi
    if i == 0:
        pass
    else:
        print("{}, {}, {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake]))
        # testataan onko vienti ulos vai sisään
        # if float(row[tapahtumaDebitSarake].strip().replace(',', '.').replace(' ', '')) > 0:
        if str(row[tapahtumaDebitSarake]).find("-")>=0:
            debit=True  # jos rahaa sisään debet tapahtumatilille
        else:
            debit=False  # jos rahaa ulos kredit tapahtumatilille

        tapahtumaTili=input(f'Syötä tapahtumatili [{tapahtumaTili}]: ') or tapahtumaTili
        # Haetaan kannasta tilinumeroa vastaava id
        tapahtumaTiliId=get_account_id(tapahtumaTili)

        vastaTili=input(f'Syötä vastatili [{vastaTili}]: ') or vastaTili
        # Haetaan kannasta tilinumeroa vastaava id
        vastaTiliId=get_account_id(vastaTili)

        # muokataan tapahtuman päivämäärä oikeaan muotoon
        ts_pvm=int(time.mktime(datetime.datetime.strptime(f"{row[tapahtumaPvmSarake]}", tmFormat).timetuple()) * 1000)

        # Lisätää Doclist listaan tapahtuman dokumentti (class document)
        DocList.append(db.dbDocument(LastDocId + i, LastDocNum + i, period, ts_pvm))
        # lisätään Doclist dokumentille tapahtuman entryt (class document.entries class entry)
        print(i)
        dbet=db.dbEntry(LastEntId + i * 2 - 1, LastDocId + i, tapahtumaTiliId, debit,row[tapahtumaDebitSarake],
                        row[tapahtumaDescSarake], 0, 0)
        dbev=db.dbEntry(LastEntId + i * 2, LastDocId + i, vastaTiliId, not debit,row[tapahtumaDebitSarake],
                        row[tapahtumaDescSarake], 1, 0)
        DocList[i - 1].add_entry(dbet)
        DocList[i - 1].add_entry(dbev)

for itm in DocList:
    print(itm.prepare_insert())
    print(itm.entries[0].prepare_insert())
    print(itm.entries[1].prepare_insert())
kirjoitus = input("Yllä olevat rivit lisätään kantaan Y/N : ")
if kirjoitus == "y" or kirjoitus == "Y":
    print('kiroitetaan')
    for itm in DocList:
        sv.execute(itm.prepare_insert())
        sv.execute(itm.entries[0].prepare_insert())
        sv.execute(itm.entries[1].prepare_insert())
        svtk.commit()
else:
    print('lopetetaan')
    sys.exit()




svtk.close()

print('The End!')


def get_account_id(account_no):
    sv.execute('SELECT id FROM account WHERE number = ')

# with open('/home/sami/Documents/SVTK/svtk.csv') as csvfile:
