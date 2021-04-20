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
        accounts = pd.read_sql('SELECT * FROM account', tilitin_db)
        documents = pd.read_sql('SELECT * FROM document', tilitin_db)
        entries = pd.read_sql('SELECT * FROM entry', tilitin_db)
        periods = pd.read_sql('SELECT * FROM period', tilitin_db)

    accounts.set_index('id', inplace=True)
    documents = documents.assign(new=False)
    documents.set_index('id', inplace=True)
    entries = entries.assign(new=False)
    entries.set_index('id', inplace=True)
    periods = periods.assign(new=False)
    periods.set_index('id', inplace=True)

    return accounts, documents, entries, periods

def read_csv(csv_name, delimiter):
    with codecs.open(csv_name, encoding='unicode_escape') as csvfile:
        csv_data = pd.read_csv(csvfile)
        return csv_data

def main():
    db_name, csv_name = parse_args()
    accounts, documents, entries, periods = read_db(db_name)
    csv_data = read_csv(csv_name, ',')

    pass


if __name__ == '__main__':
    main()