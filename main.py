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
import datetime
import sqlite3
import sys
import time
import os
import pandas as pd

import tilitindb as db
from bankinfo import bankinfo


def parse_args():
    args = sys.argv[1:]
    if len(args) == 2:
        db_name = str(args[0])
        csv_name = str(args[1])

    else:
        print("Usage: python3 tilitin_import.py [database] [csv]")
        sys.exit(0)
    return db_name, csv_name


def read_db(db_name):
    with sqlite3.connect(db_name) as tilitin_db:
        cursor = tilitin_db.cursor()
        cursor.execute('SELECT max(id) FROM document')
        last_document_id = cursor.fetchone()[0]
        # print(last_document_id)
        cursor.execute('SELECT number FROM document WHERE id={}'.format(last_document_id))
        last_document_number = cursor.fetchone()[0]
        cursor.execute('SELECT max(id) FROM entry')
        last_entry_id = cursor.fetchone()[0]
        periods = pd.read_sql('SELECT * FROM period', tilitin_db)

    return last_document_id, last_document_number, last_entry_id, periods


def read_csv(csv_name, delimiter):
    with codecs.open(csv_name, encoding='unicode_escape') as csvfile:
        csv_data = pd.read_csv(csvfile, delimiter=delimiter)
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
    for item in db_periods.itertuples():
        print(f"{item[1]}   {datetime.datetime.utcfromtimestamp(item[3] / 1000).strftime('%Y')}  "
              f" {'Kyllä' if item[4] == 1 else 'Ei'}")
    last_period_id = max(db_periods['id'])
    print()
    print(f"Uudet tapahtumat lisätään tilikaudelle {last_period_id}")
    print("Tapahtumat viedään kantaan tapahtumatilille ja väliaikaiselle vastatilille")
    vientitili = input("Anna tili, jolle tapahtumat viedään (tapahtimatili) 'q' lopettaa: ")
    if vientitili.lower() == 'q':
        sys.exit(0)
    temp_vastatili = input("Anna vastatili, jolle vienti tehdään (esim.8999) 'q' lopettaa: ")
    if temp_vastatili.lower() == 'q':
        sys.exit(0)
    return last_period_id, vientitili, temp_vastatili


def create_new_items(csv_data, last_document_id, last_document_number,
                     last_entry_id, period_id, vientitili, temp_vastatili):
    docs = []
    ents = []
    for item in csv_data.itertuples():
        print(item)




def main():
    db_name, csv_name = parse_args()
    last_document_id, last_document_number, last_entry_id, periods = read_db(db_name)
    csv_data = read_csv(csv_name, ';')
    last_period_id, vientitili, temp_vastatili = print_db_info(periods)
    create_new_items(csv_data, last_document_id, last_document_number,
                     last_entry_id, last_period_id, vientitili, temp_vastatili)




if __name__ == '__main__':
    main()
