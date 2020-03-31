import sqlite3
import csv
import time
import datetime
import dataBase




svtk=sqlite3.connect('/home/sami/Documents/SVTK/svtk_test.sqlite')
svtk.row_factory = sqlite3.Row
sv=svtk.cursor()
sv.execute('SELECT * FROM period') # ORDER BY id DESC')
r = sv.fetchall()
print(f'Tietokannassa on tilikausia {len(r)} kappaletta')
print()
for itm in r:
    period = tuple(itm)[0]
    StartDate = tuple(itm)[1]
    StopDate = tuple(itm)[2]
    if tuple(itm)[3]==0:
        lukko = "EI"
    else:
        lukko="KYLLÄ"
    print("[{}] {} - {} Lukittu: {}".format(period, datetime.datetime.utcfromtimestamp(tuple(itm)[1]/1000).strftime("%d.%m.%Y"),\
                                            datetime.datetime.utcfromtimestamp(tuple(itm)[2]/1000).strftime("%d.%m.%Y"), lukko))

print()
#period = input("Valitse käytettävä tilikausi: ")
print(f'Valittu tilikausi {period}')

with open('/home/sami/Documents/SVTK/svtk.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    csvData = list(reader)
    print(f"Löytyi {len(csvData[0])} Saraketta")
    print()
    for i, itm in enumerate(csvData[0]):
        print(f"[{i}]  {itm}")

tapahtumaPvmSarake = int(input('Sarake, jossa tapahtuman päivämäärä : '))
tapahtumaDebitSarake = int(input('Sarake, jossa tapahtuman Debit : '))
tapahtumaDescSarake = int(input('Sarake, jossa tapahtuman maksaja : '))


print()
DebetTili = 0
KreditTili = 0
for i, row in enumerate(csvData):
   if i > 0:
       print("{}, {}, {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake]))
       if float(row[tapahtumaDebitSarake]) > 0:
           DebetTili = 1911
           DebetTili = input(f"Anna Debet tili : [{DebetTili}]") or DebetTili
           KreditTili = input(f"Anna Kredit tili : [{KreditTili}]")
           print("{}, {}, {} , {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake], DebetTili))
           print("{}, {}, {} , {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake], KreditTili))
       else:
           KreditTili = 1911
           KreditTili=input(f"Anna Kredit tili : [{KreditTili}]") or KreditTili
           DebetTili=input(f"Anna Debet tili : [{DebetTili}]")
           print("{}, {}, {} , {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake], KreditTili))
           print("{}, {}, {} , {}".format(row[tapahtumaPvmSarake], row[tapahtumaDebitSarake], row[tapahtumaDescSarake], DebetTili))







# with open('/home/sami/Documents/SVTK/svtk.csv') as csvfile:

