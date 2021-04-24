#!/usr/bin/python3
# encoding: 'utf-8'

__author__ = "Sami Sillanpää"
__copyright__ = "Copyright 2021, (c) Sami Sillanpää"
__credits__ = ["Sami Sillanpää"]
__license__ = "GNU GPLv3"
__version__ = "0.1.1"
__maintainer__ = "Sami Sillanpää"
__email__ = "sami.sillanpaa@iki.fi"
__status__ = "Development"


import codecs
import csv
import datetime
import time
import json
import sqlite3
import sys
import logging
from tilitindb import DbDocument, DbEntry, DbPeriod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tilitin_import.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




def parse_args():
    args = sys.argv[1:]
    if len(args) == 2:
        db_name = str(args[0])
        csv_name = str(args[1])
        logger.info('ARGS OK')
    else:
        print("Usage: python3 tilitin_import.py [database] [csv]")
        logger.error('PROBLEM ARGS')
        sys.exit(0)
    return db_name, csv_name


def read_db(db_name):
    db_limits = {}
    db_periods = []
    vientitili, vastatili = get_tilit()
    with sqlite3.connect(db_name) as tilitin_db:
        cursor = tilitin_db.cursor()
        cursor.execute('SELECT max(id) FROM document')
        db_limits['last_document_id']  = cursor.fetchone()[0]
        # print(last_document_id)
        cursor.execute(f"SELECT number FROM document WHERE id={db_limits['last_document_id']}")
        db_limits['last_document_number'] = cursor.fetchone()[0]
        cursor.execute('SELECT max(id) FROM entry')
        db_limits['last_entry_id'] = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM period')
        periods = cursor.fetchall()
        for period in periods:
            db_periods.append(DbPeriod(period[0], period[1], period[2], period[3]))
        db_limits['last_period_id'] = max(item.id for item in db_periods)
        cursor.execute(f"SELECT id FROM account WHERE number={vientitili}")
        vientitili_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT id FROM account WHERE number={vastatili}")
        vastatili_id = cursor.fetchone()[0]

    return db_limits, db_periods, vientitili_id, vastatili_id




def read_bank_csv(csv_name, csv_model):
    tapahtumat = []
    with codecs.open(csv_name, encoding='unicode_escape') as csvfile:
        csv_data = list(csv.reader(csvfile, delimiter=csv_model['delimiter']))
    # print(csv_data)
    return csv_data

def get_account_id(db_name, account_no):
    """Funktio hakee kannasta tilin id:n annetun  tilinumeron perusteella"""
    with sqlite3.connect(db_name) as tilitin_db:
        cursor = tilitin_db.cursor()
        cursor.execute(f'SELECT id FROM account WHERE number = {account_no}')
        result = cursor.fetchone()[0]
        return result

def get_account_name(db_name, account_id):
    """Funktio hakee kannasta tilin nimen annetun  id:n perusteella"""
    with sqlite3.connect(db_name) as tilitin_db:
        cursor = tilitin_db.cursor()
        cursor.execute(f'SELECT name FROM account WHERE id = {account_id}')
        result = cursor.fetchone()[0]
    return result


def print_db_info(db_periods, db_limits):
    print("Kannasta löytyvät seuraavat tilikaudet: ")
    print("ID  Vuosi  Lukittu")
    print("--  -----  -------")
    for item in db_periods:
        print(f"{item.id}   {datetime.datetime.utcfromtimestamp(item.endDate / 1000).strftime('%Y')}  "
              f" {'Kyllä' if item.locked == 1 else 'Ei'}")
    print()
    print(f"Uudet tapahtumat lisätään tilikaudelle {db_limits['last_period_id']}")
    return None


def get_tilit():
    print("Tapahtumat viedään kantaan tapahtumatilille ja väliaikaiselle vastatilille")
    vientitili = 1911 #input("Anna tili, jolle tapahtumat viedään (tapahtimatili) 'q' lopettaa: ")
    # if vientitili.lower() == 'q':
    #     sys.exit(0)
    vastatili = 4551 #input("Anna vastatili, jolle vienti tehdään (esim.8999) 'q' lopettaa: ")
    # if vastatili.lower() == 'q':
    #     sys.exit(0)
    return vientitili, vastatili

def uusi_pankkimalli():
    try:
        with open('bank_csv.json', 'r') as f:
            banks = json.load(f)
    except FileNotFoundError:
        print("'bank_csv.json' tiedostoa ei löydy")
        return None

    print("Syötä uusi pankkimalli: ")
    nimi = input("Pankin nimi: ")
    delimiter = input("Kenttäerotin [,]: ") or ","
    timeformat = input("Timeformat [%d.%m.%Y]: ") or "%d.%m.%Y"
    datecolumn = input("Päivämäärän sarake [0]: ") or 0
    sumcolumn = input("Summan sarake [2]: ") or 2
    desc_column = input("Kuvauksen sarake [1]: ") or 1
    csv_model = {"delimiter": delimiter,
                 "timeformat": timeformat,
                 "datecol": int(datecolumn),
                 "sumcol": int(sumcolumn),
                 "descol": int(desc_column)}
    banks['banks'].append({nimi: [csv_model]})
    with open('bank_csv.json', 'w') as f:
        json.dump(banks, f, indent=2)

    return csv_model

def select_bank():
    bank_sel = {}
    csv_model = {}
    try:
        with open('bank_csv.json', 'r') as f:
            banks = json.load(f)
    except FileNotFoundError:
        print("'bank_csv.json' tiedostoa ei löydy")
        return None
    print("Löytyi seuraavat csv mallit:  ")
    print('------------------------------')
    for i, bank in enumerate(banks['banks']):
        bank_sel[i + 1] = list(bank.keys())[0]
        print(f"{i + 1} - {bank_sel[i+1]}")
    print('------------------------------')
    print()
    valinta = input("Valitse malli, ('u'-syöttää uuden): ")
    for i in range(1, len(bank_sel) + 1):
        if valinta.lower() == 'u':
            csv_model = uusi_pankkimalli()
            break
        elif int(valinta) == i:
            csv_model = banks['banks'][i-1][bank_sel[i]][0]
            print(csv_model)
            break
    return csv_model


def create_new_items(csv_data, csv_model, db_limits, vientitili, vastatili):
    docs = []
    # print(csv_model)
    for d, tapahtuma in enumerate(csv_data[1:]):
        # print(tapahtuma)
        doc_date = int(time.mktime(datetime.datetime.strptime(f"{tapahtuma[csv_model['datecol']]}",
                                                              csv_model['timeformat']).timetuple()) * 1000)
        docs.append(DbDocument(db_limits['last_document_id'] + d + 1,  db_limits['last_document_number'] + d + 1,
                               db_limits['last_period_id'], doc_date))
        if tapahtuma[csv_model['sumcol']].startswith('-'):
            debit = False
        else:
            debit = True
        docs[-1].add_entry(DbEntry(db_limits['last_entry_id'] + d * 2 + 1, docs[-1].id, vientitili,
                                   debit, abs(float(tapahtuma[csv_model['sumcol']])),
                                   tapahtuma[csv_model['descol']], 1))
        docs[-1].add_entry(DbEntry(db_limits['last_entry_id'] + d * 2 + 2, docs[-1].id, vastatili,
                                   not debit, abs(float(tapahtuma[csv_model['sumcol']])),
                                   tapahtuma[csv_model['descol']], 2))

    return docs

def kirjoita_kantaan(docs_to_add, db_name):
    print('Kirjoitetaan')
    with sqlite3.connect(db_name) as tilitin_db:
        cursor = tilitin_db.cursor()
        for itm in docs_to_add:
            cursor.execute(itm.sql_str)
            print(itm.sql_str)
            time.sleep(0.2)
            for ent in itm.entries:
                cursor.execute(ent.sql_str)
                print(ent.sql_str)
                time.sleep(0.2)
            # time.sleep(0.2)
        tilitin_db.commit()
    print()



def main():
    db_name, csv_name = parse_args()
    db_limits, db_periods, vientitili_id, vastatili_id = read_db(db_name)
    last_period_id = print_db_info(db_periods, db_limits)
    # vientitili, vastatili = get_tilit()
    csv_model = select_bank()
    csv_data = read_bank_csv(csv_name, csv_model)
    docs_to_add = create_new_items(csv_data, csv_model, db_limits, vientitili_id, vastatili_id)
    print("ENT DOC ROW ACC DEB        SUM  DESC")
    print("-------------------------------------------------------")
    for item in docs_to_add:
        for ent in item.entries:
            print(ent)
    print("-------------------------------------------------------")
    print()
    while True:
        kirjoitus = input("Kirjoitetaanko tiedot kantaan ? k/e : ")
        if kirjoitus.lower() == 'k':
            kirjoita_kantaan(docs_to_add, db_name)
            break
        elif kirjoitus.lower() == 'e':
            break
        else:
            print('Valintse k/e : ')






if __name__ == '__main__':
    main()
