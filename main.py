import sqlite3
import csv
import time
import datetime
import dataBase as db


def get_account_id(account_no):
    sv.execute(f'SELECT id FROM account WHERE number = {account_no}')
    return sv.fetchone()[0]

# SELECT number FROM document WHERE number=(SELECT max(number) FROM document WHERE period_id = 4)
# SELECT id FROM document WHERE id=(SELECT max(id) FROM document WHERE period_id = 4)

def get_last_numbers(period):
    sv.execute('SELECT max(id) FROM document')
    last_doc_id = sv.fetchone()[0]
    sv.execute(f'SELECT max(number) FROM document WHERE period_id = {period}')
    last_doc_number = sv.fetchone()[0]
    sv.execute('SELECT max(id) FROM entry')
    last_ent_id=sv.fetchone()[0]
    return last_doc_id, last_doc_number, last_ent_id


# Ava tiliote / tilitapahtuma .csv
# todo nimi argumenttina
# todo csv mallit eri pankeille
# todo mmerkistökoodus
# tämä malli dansken tapahtuma csv
svtk=sqlite3.connect('/home/sami/Documents/SVTK/svtk_test.sqlite')
svtk.row_factory=sqlite3.Row
sv=svtk.cursor()
sv.execute('SELECT * FROM period')  # ORDER BY id DESC')
r=sv.fetchall()
print(f'Tietokannassa on tilikausia {len(r)} kappaletta')
print()
periodsInDb=[]
validPeriods=[]
for y, itm in enumerate(r):
    periodsInDb.append(db.dbPeriod(tuple(itm)[0], tuple(itm)[1], tuple(itm)[2], tuple(itm)[3]))
    validPeriods.append(tuple(itm)[0])
    # print(periodsInDb[y].prepare_insert())

    # period = tuple(itm)[0]
    # StartDate = tuple(itm)[1]
    # StopDate = tuple(itm)[2]
    # if tuple(itm)[3]==0:
    #     lukko = "EI"
    # else:
    #     lukko="KYLLÄ"
    print("[{}] {} - {} Lukittu: {}".format(periodsInDb[y].id, datetime.datetime.utcfromtimestamp(
        periodsInDb[y].startDate / 1000).strftime("%d.%m.%Y"), \
                                            datetime.datetime.utcfromtimestamp(periodsInDb[y].endDate / 1000).strftime(
                                                "%d.%m.%Y"), periodsInDb[y].locked))

print()
period=int(input("Valitse käytettävä tilikausi: "))
while validPeriods.count(period) != 1:
    period=int(input(f"{period} ei ole validi, Valitse käytettävä tilikausi: "))

print(f'Valittu tilikausi {period}')

with open('/home/sami/Documents/SVTK/svtk.csv', newline='') as csvfile:
    reader=csv.reader(csvfile, delimiter=',')
    csvData=list(reader)
    print(f"Löytyi {len(csvData[0])} Saraketta")
    print()
    for i, itm in enumerate(csvData[0]):
        print(f"[{i}]  {itm}")

# csv sarakkeiden mäppäys
tapahtumaPvmSarake=0  # int(input('Sarake, jossa tapahtuman päivämäärä : '))
tapahtumaDebitSarake=2  # int(input('Sarake, jossa tapahtuman Debit : '))
tapahtumaDescSarake=1  # int(input('Sarake, jossa tapahtuman maksaja : '))

print()
tapahtumaTili=1911
vastaTili=4101
DocList=[]
LastDocId = get_last_numbers(period)[0]
LastDocNum = get_last_numbers(period)[1]
LastEntId = get_last_numbers(period)[2]
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
        if float(row[tapahtumaDebitSarake]) > 0:
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
        ts_pvm=int(time.mktime(datetime.datetime.strptime(f"{row[tapahtumaPvmSarake]}", '%m/%d/%y').timetuple()) * 1000)

        # Lisätää Doclist listaan tapahtuman dokumentti (class document)
        DocList.append(db.dbDocument(LastDocId + i, LastDocNum + i, period, ts_pvm))
        # lisätään Doclist dokumentille tapahtuman entryt (class document.entries class entry)
        print(i)
        dbet=db.dbEntry(LastEntId + i * 2 -1, LastDocId + i, tapahtumaTiliId, int(debit), abs(float((row[tapahtumaDebitSarake]))),
                        row[tapahtumaDescSarake], 0, 0)
        dbev=db.dbEntry(LastEntId + i * 2, LastDocId + i, vastaTiliId, int(not debit), abs(float(row[tapahtumaDebitSarake])),
                        row[tapahtumaDescSarake], 1, 0)
        DocList[i - 1].add_entry(dbet)
        DocList[i - 1].add_entry(dbev)
        print(DocList[i - 1].prepare_insert())
        print(DocList[i - 1].entries[0].prepare_insert())
        print(DocList[i - 1].entries[1].prepare_insert())
        #sv.execute(DocList[i - 1].prepare_insert())
        #sv.execute(DocList[i - 1].entries[0].prepare_insert())
        #sv.execute(DocList[i - 1].entries[1].prepare_insert())
        #svtk.commit()



svtk.close()

print('The End!')


def get_account_id(account_no):
    sv.execute('SELECT id FROM account WHERE number = ')

# with open('/home/sami/Documents/SVTK/svtk.csv') as csvfile:
