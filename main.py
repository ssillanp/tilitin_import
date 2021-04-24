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
import json
import sqlite3
import sys
import logging
from tilitindb import DbDocument, DbEntry

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
    with sqlite3.connect(db_name) as tilitin_db:
        cursor = tilitin_db.cursor()
        cursor.execute('SELECT max(id) FROM document')
        db_limits['last_document_id']  = cursor.fetchone()[0]
        # print(last_document_id)
        cursor.execute('SELECT number FROM document WHERE id={}'.format(db_limits['last_document_id']))
        db_limits['last_document_number'] = cursor.fetchone()[0]
        cursor.execute('SELECT max(id) FROM entry')
        db_limits['last_entry_id'] = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM period')
        periods = cursor.fetchall()

    return db_limits, periods




def read_bank_csv(csv_name, csv_model):
    tapahtumat = []
    with codecs.open(csv_name, encoding='unicode_escape') as csvfile:
        csv_data = list(csv.reader(csvfile, delimiter=csv_model['delimiter']))
    print(csv_data)
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


def print_db_info(db_periods):
    print("Kannasta löytyvät seuraavat tilikaudet: ")
    print("ID  Vuosi  Lukittu")
    print("--  -----  -------")
    for item in db_periods:
        print(f"{item[0]}   {datetime.datetime.utcfromtimestamp(item[2] / 1000).strftime('%Y')}  "
              f" {'Kyllä' if item[3] == 1 else 'Ei'}")
    last_period_id = max(period[0] for period in db_periods)
    print()
    print(f"Uudet tapahtumat lisätään tilikaudelle {last_period_id}")
    print("Tapahtumat viedään kantaan tapahtumatilille ja väliaikaiselle vastatilille")
    vientitili = input("Anna tili, jolle tapahtumat viedään (tapahtimatili) 'q' lopettaa: ")
    if vientitili.lower() == 'q':
        sys.exit(0)
    vastatili = input("Anna vastatili, jolle vienti tehdään (esim.8999) 'q' lopettaa: ")
    if vastatili.lower() == 'q':
        sys.exit(0)
    return last_period_id, vientitili, vastatili


def select_bank():
    print("Valitse pankki, tapahtuma csv:n malliin")
    print("1) OP")
    print("2) DANSKE")
    print("3) Syötä oma malli")
    while True:
        bank = input("Valitse CSV malli: ")
        try:
            bank = int(bank)
            if bank not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print(f"Valinta ei kelpaa, valitse 1, 2, tai 3")
            continue
    if bank == 1:
        bankname = 'op'
    elif bank == 2:
        bankname = 'danske'
    elif bank == 3:
        bankname = 'user'
    try:
        with open('bank_csv.json', 'r') as f:
            binfo = json.load(f)['banks'][bank-1][bankname][0]
            print(binfo)
    except FileNotFoundError:
        print("'bank_csv.json' tiedostoa ei löydy")
        binfo = None

    return binfo


def create_new_items(csv_data, db_limits, last_period_id,  vientitili, vastatili):
    docs = []
    for tapahtuma in csv_data[1:]:
        print(tapahtuma)
        docs.append(DbDocument(db_limits['last_document_id'] + 1,  db_limits['last_document_number'] + 1, 
                               last_period_id, tapahtuma[0]))




def main():
    db_name, csv_name = parse_args()
    db_limits, periods = read_db(db_name)
    last_period_id, vientitili, vastatili = print_db_info(periods)
    csv_model = select_bank()
    csv_data = read_bank_csv(csv_name, csv_model)
    create_new_items(csv_data, db_limits, last_period_id, vientitili, vastatili)




if __name__ == '__main__':
    main()
