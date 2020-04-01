import sqlite3
import csv
import time
import datetime
import dataBase as db



# Ava tiliote / tilitapahtuma .csv
#todo nimi argumenttina
#todo csv mallit eri pankeille
#todo mmerkistökoodus
#tämä malli dansken tapahtuma csv
svtk=sqlite3.connect('/home/sami/Documents/SVTK/svtk_test.sqlite')
svtk.row_factory = sqlite3.Row
sv=svtk.cursor()
sv.execute('SELECT * FROM period') # ORDER BY id DESC')
r = sv.fetchall()
print(f'Tietokannassa on tilikausia {len(r)} kappaletta')
print()
periodsInDb = []
validPeriods = []
for y, itm in enumerate(r):
    periodsInDb.append(db.dbPeriod(tuple(itm)[0], tuple(itm)[1], tuple(itm)[2], tuple(itm)[3]))
    validPeriods.append(tuple(itm)[0])
    print(periodsInDb[y].prepare_insert())

    # period = tuple(itm)[0]
    # StartDate = tuple(itm)[1]
    # StopDate = tuple(itm)[2]
    # if tuple(itm)[3]==0:
    #     lukko = "EI"
    # else:
    #     lukko="KYLLÄ"
    print("[{}] {} - {} Lukittu: {}".format(periodsInDb[y].id, datetime.datetime.utcfromtimestamp(periodsInDb[y].startDate/1000).strftime("%d.%m.%Y"), \
                                             datetime.datetime.utcfromtimestamp(periodsInDb[y].endDate/1000).strftime("%d.%m.%Y"), periodsInDb[y].locked))

print()
period = int(input("Valitse käytettävä tilikausi: "))
while validPeriods.count(period) != 1:
    period = int(input(f"{period} ei ole validi, Valitse käytettävä tilikausi: "))

print(f'Valittu tilikausi {period}')

with open('/home/sami/Documents/SVTK/svtk.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    csvData = list(reader)
    print(f"Löytyi {len(csvData[0])} Saraketta")
    print()
    for i, itm in enumerate(csvData[0]):
        print(f"[{i}]  {itm}")

#csv sarakkeiden mäppäys
tapahtumaPvmSarake = 0 #int(input('Sarake, jossa tapahtuman päivämäärä : '))
tapahtumaDebitSarake = 2 #int(input('Sarake, jossa tapahtuman Debit : '))
tapahtumaDescSarake = 1 #int(input('Sarake, jossa tapahtuman maksaja : '))


print()
tapahtumaTili = 1911
vastaTili = 2000
DocList = []

for i, row in enumerate(csvData):
   if i == 0:
       pass
   else:
       print("{}, {}, {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake]))
       if float(row[tapahtumaDebitSarake]) > 0:
           debit = True
       else:
           debit = False
       tapahtumaTili = input(f'Syötä tapahtumatili [{tapahtumaTili}]: ') or tapahtumaTili
       vastaTili = input(f'Syötä vastatili [{vastaTili}]: ') or vastaTili
       ts_pvm = int(time.mktime(datetime.datetime.strptime(f"{row[tapahtumaPvmSarake]}", '%m/%d/%y').timetuple())*1000)
       DocList.append(db.dbDocument(i*2, i-1, period, ts_pvm))
       dbet = db.dbEntry(i, i*2, tapahtumaTili, int(debit), row[tapahtumaDebitSarake], row[tapahtumaDescSarake], 0, 0)
       dbev = db.dbEntry(i + 1, i*2, vastaTili, int(not debit), row[tapahtumaDebitSarake], row[tapahtumaDescSarake], 1, 0)
       DocList[i-1].add_entry(dbet)
       print(DocList[i-1].prepare_insert())
       print(DocList[i-1].entries[0].prepare_insert())
       DocList[i-1].add_entry(dbev)
       print(DocList[i-1].entries[1].prepare_insert())



print('The End!')














# with open('/home/sami/Documents/SVTK/svtk.csv') as csvfile:

