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
import sqlite3
import sys
import os
import logging
import pickle
import argparse
from progress.bar import Bar
from tilitindb import DbDocument, DbEntry, DbPeriod


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tilitin_import.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = argparse.ArgumentParser()
parser.add_argument("dbName", help="Name of the tilitin database")
parser.add_argument("csvName", help="Name of the csvfile")
parser.add_argument("-l", "--loglevel", help="sets the logging level",
                    type=str, choices=['debug', 'info', 'warning', 'error', 'critical'],
                    default='warning')

args = parser.parse_args()
loglevels = {'debug': logging.DEBUG,
             'info': logging.INFO,
             'warning': logging.WARNING,
             'error': logging.ERROR,
             'critical': logging.CRITICAL}

logger.setLevel(loglevels[args.loglevel])
# print(logger.level)


def read_db(db_name):
    """ Funtion reads from tilitin database
    :param db_name: database name
    :return: database limits ad db_limits (dict)
    :return: db_periods list of DbPeriod Objects (list)
    :return: vientitili_id db Id for the debit account to store
    :return: vastatili_id db Id for credit account
    """
    db_limits = {}
    db_periods = []
    vientitili, vastatili = get_tilit()
    try:
        with sqlite3.connect(db_name) as tilitin_db:
            cursor = tilitin_db.cursor()
            cursor.execute('SELECT max(id) FROM document')
            db_limits['last_document_id'] = cursor.fetchone()[0]
            # print(last_document_id)
            cursor.execute(f"SELECT number FROM document WHERE id={db_limits['last_document_id']}")
            db_limits['last_document_number'] = cursor.fetchone()[0]
            cursor.execute('SELECT max(id) FROM entry')
            db_limits['last_entry_id'] = cursor.fetchone()[0] or 0
            cursor.execute('SELECT * FROM period')
            periods = cursor.fetchall()
            for period in periods:
                db_periods.append(DbPeriod(period[0], period[1], period[2], period[3]))
            db_limits['last_period_id'] = db_periods[-1].id
            db_limits['last_period_year'] = datetime.datetime.utcfromtimestamp(db_periods[-1].endDate / 1000).strftime('%Y')
            # print(db_limits)
            tili = vientitili
            cursor.execute(f"SELECT id FROM account WHERE number={tili}")
            vientitili_id = cursor.fetchone()[0]
            tili = vastatili
            cursor.execute(f"SELECT id FROM account WHERE number={tili}")
            vastatili_id = cursor.fetchone()[0]
            logger.debug('DB OK - read_db()')
    except sqlite3.OperationalError:
        logger.error(f'DB ERROR (read_db()) db:{db_name}')
        print(f"Tietokantaa '{db_name} ei voitu avata, tai tietokanta ei ole tilitin-kanta")
        sys.exit(0)
    except TypeError:
        logger.error(f"ERROR PARSING ACC acc:'{tili}'")
        print(f"Tilinumeroa:'{tili}' ei löydy ")
        sys.exit(0)
    return db_limits, db_periods, vientitili_id, vastatili_id


def read_bank_csv(csv_name, csv_model):
    """ Read data from given csv-file
    :param csv_name: csv filename
    :param csv_model: bank model of the selected csv
    :return: data from the csv as csv_data (list)
    """
    try:
        with codecs.open(csv_name, encoding='unicode_escape') as csvfile:
            csv_data = list(csv.reader(csvfile, delimiter=csv_model['delimiter']))
        logger.debug('csv OK')
        return csv_data
    except FileNotFoundError:
        logger.error(f"CSV ERROR, csv:'{csv_name}'")
        print(f"Tapahtumatiedostoa {csv_name} ei ole")
        sys.exit(0)


def get_account_id(db_name, account_no):
    """ Function get account id from db based on account no
    :param db_name: db_filename
    :param account_no: number of the account
    :return: id of the account
    """
    try:
        with sqlite3.connect(db_name) as tilitin_db:
            cursor = tilitin_db.cursor()
            cursor.execute(f'SELECT id FROM account WHERE number = {account_no}')
            result = cursor.fetchone()[0]
        logger.debug('DB OK - get_account_id()')
        return result
    except sqlite3.OperationalError:
        logger.error(f'DB ERROR (get_account_id()), db:{db_name}')
        print(f"Tietokantaa '{db_name} ei voitu avata, tai tietokanta ei ole tilitin-kanta")
        sys.exit(0)

def get_account_name(db_name, account_id):
    """ Function returns the name of the account, with given number
    :param db_name: database filename
    :param account_id: Id of the requested account
    :return: Name of the account with given Id
    """
    try:
        with sqlite3.connect(db_name) as tilitin_db:
            cursor = tilitin_db.cursor()
            cursor.execute(f'SELECT name FROM account WHERE id = {account_id}')
            result = cursor.fetchone()[0]
        logger.debug('DB OK - get_account_name()')
        return result
    except sqlite3.OperationalError:
        logger.error(f'DB ERROR (get_account_name()), db:{db_name}')
        print(f"Tietokantaa '{db_name} ei voitu avata, tai tietokanta ei ole tilitin-kanta")
        sys.exit(0)


def print_db_info(db_periods, db_limits):
    """ Function prints the periods found in db for user info
    :param db_periods: periods in db, as a list of DbPariod-items (list)
    :param db_limits: info about the db as db_limits (dict)
    :return: None
    """
    print("Kannasta löytyvät seuraavat tilikaudet: ")
    print("ID  Vuosi  Lukittu")
    print("--  -----  -------")
    for item in db_periods:
        print(f"{item.id}   {datetime.datetime.utcfromtimestamp(item.endDate / 1000).strftime('%Y')}  "
              f" {'Kyllä' if item.locked == 1 else 'Ei'}")
    print()
    print(f"Uudet tapahtumat lisätään tilikaudelle {db_limits['last_period_id']}")
    valinta = input("Jatka k/e [k]: ") or 'k'
    if valinta.lower() != 'k':
        sys.exit(0)
    return None


def get_tilit():
    """ Function asks for the debit and credit accoun numbers from user and returns them
    :return: debit account as vientitili (str), credit account as vastatili (str)
    """
    print("Tapahtumat viedään kantaan tapahtumatilille ja väliaikaiselle vastatilille")
    vientitili = input("Anna tili, jolle tapahtumat viedään (tapahtimatili): ")
    vastatili = input("Anna vastatili, jolle vienti tehdään (esim.8999): ")
    return vientitili, vastatili


def pankkimalli(action):
    """ Function creates or deletes a bank csv_model (user given)
    :param action: Create - True, Delete - False
    :return: bank csv_model (dict), False if cancelled or deleted
    """
    try:
        with open('banks.pkl', 'rb') as f:
            banks = pickle.load(f)
        logger.debug(f"BANK MODEL READ PICKLE OK")
    except FileNotFoundError:
        logger.error(f"ERROR BANK PICKLE READING- NOT FOUND")
        print("'banks.pkl' tiedostoa ei löydy")
        return None

    while True:
        if action:
            print("Syötä uusi pankkimalli: ")
            nimi = input("Pankin nimi: ")
            delimiter = input("Kenttäerotin [,]: ") or ","
            timeformat = input("Timeformat [%d.%m.%Y]: ") or "%d.%m.%Y"
            datecolumn = input("Päivämäärän sarake [0]: ") or 0
            sumcolumn = input("Summan sarake [2]: ") or 2
            desc_column = input("Kuvauksen sarake [1]: ") or 1
            decimal_sep = input("Desimaalierotin [,]: ") or ','
            try:
                csv_model = {"delimiter": delimiter,
                             "timeformat": timeformat,
                             "datecol": int(datecolumn),
                             "sumcol": int(sumcolumn),
                             "descol": int(desc_column),
                             "decimal": decimal_sep}
                print()
                print("------------------------")
                print(f"Pankkimalli {nimi}:")
                for key, value in csv_model.items():
                    print(f"{key} : {value}")
                tallenna = input("Tallenna k/e: ")
                print("------------------------")
                print()
                if tallenna.lower() == 'k':
                    banks[nimi] = csv_model
                else:
                    csv_model = False
                    pass
                break
            except ValueError:
                print("saraketietojen tulee olla kokonaislukuja!")
                logger.error('ERROR USER INPUT WRONG DATATYPE')
                continue

        else:
            nro = input("Valitse poistettava pankkimalli, 'q'-lopettaa: ")
            if nro.lower() == 'q':
                csv_model = False
                break
            try:
                banks.pop(list(banks.keys())[int(nro)-1])
                logger.debug(f"BANK REMOVED, index='{nro}'")
                csv_model = False
                break
            except (IndexError, ValueError):
                logger.error(f"INDEX NOT VALID index='{nro}'")
                print("Anna validi numero!")

    try:
        with open('banks.pkl', 'wb') as f:
            pickle.dump(banks, f)
        logger.debug(f"BANK MODEL SAVING - PICKLE OK")
    except FileNotFoundError:
        logger.error(f"ERROR BANK PICKLE SAVING - NOT FOUND")
        print("'banks.pkl' tiedostoa ei löydy")

    return csv_model


def select_bank():
    """ Function prints available bank csv model and asks user a model number
    :return: selected model as csv_model (dict)
    """
    csv_model = False

    try:
        with open('banks.pkl', 'rb') as f:
            banks = pickle.load(f)
            logger.debug("BANKS LOAD PICKLE OK")
    except FileNotFoundError:
        logger.error("BANKS LOAD PKL NOT FOUND")
        print("'bank_csv.json' tiedostoa ei löydy")
        return None

    while not csv_model:
        print("Löytyi seuraavat csv mallit:  ")
        print('------------------------------')
        for i, key in enumerate(list(banks.keys())):
            print(f"{i + 1} - {key}")
        print()
        print("u - syötä uusi, d - poista")
        print('------------------------------')
        print("Valitse malli")
        valinta = input("Valitse: ")
        try:
            if valinta.lower() == 'u':
                csv_model = pankkimalli(True)
            elif valinta.lower() == 'd':
                csv_model = pankkimalli(False)
            elif int(valinta) > len(banks.keys()):
                logger.error(f"INVALID USER INPUT - csv-model input:'{valinta}'")
                print("Anna validi numero, u tai d ")
                csv_model = False
            else:
                csv_model = banks[list(banks.keys())[int(valinta) - 1]]
                # print(csv_model)
        except ValueError:
            logger.error(f"INVALID USER INPUT - csv-model input:'{valinta}'")
            print("Anna validi numero, u tai d ")
    return csv_model


def create_new_items(csv_data, csv_model, db_limits, vientitili_id, vastatili_id):
    """ Function creates new items DbDocument and DBEntry to be injected into database
    :param csv_data: items from csv as csv_data (list)
    :param csv_model: selected csv model as csv_model (dict)
    :param db_limits: db info as db_limits (dict)
    :param vientitili_id: debit account id as vientitili_id (int)
    :param vastatili_id: credit account id as vastatili_id (int)
    :return: list of created items as docs (list)
    """
    docs = []
    # loop through csv_data skipping the header row
    for d, tapahtuma in enumerate(csv_data[1:]):
        # parse the year of each csv item
        tapahtuma_year  = datetime.datetime.strptime(tapahtuma[csv_model['datecol']], csv_model['timeformat']).year
        # Check that the year matches the year of the selcted period and trash if not
        if tapahtuma_year != int(db_limits['last_period_year']):
            print(f"{tapahtuma[csv_model['datecol']]} : {tapahtuma[csv_model['sumcol']]} : {tapahtuma[csv_model['descol']]}"
                  f" ei ole vienti-tilikaudella, skipataan...")
            input("Paina enter jatkaaksesi...")
            continue
        # Parse the date to match db date format (ts * 1000)
        doc_date = int(time.mktime(datetime.datetime.strptime(f"{tapahtuma[csv_model['datecol']]}",
                                                              csv_model['timeformat']).timetuple()) * 1000)
        # Add a document item to docs list as DbDocument object
        docs.append(DbDocument(db_limits['last_document_id'] + d + 1,  db_limits['last_document_number'] + d + 1,
                               db_limits['last_period_id'], doc_date))
        # Parse the sum from csv item (remove whitespaces, match the decimal separator)
        tapahtuma_sum = tapahtuma[csv_model['sumcol']].replace(csv_model['decimal'], '.')\
            .replace('"', '').replace(' ', '')
        # Change sum datatype to float
        try:
            tapahtuma_sum = float(tapahtuma_sum)
        except ValueError:
            print(f"Ongelma CSV datan parsimisessa. summa väärää muotoa '{tapahtuma_sum}'")
            logger.error(f"CSV SUM ERROR sum:'{tapahtuma_sum}")
            sys.exit(0)
        if tapahtuma_sum < 0:
            debit = False
        else:
            debit = True
        docs[-1].add_entry(DbEntry(db_limits['last_entry_id'] + d * 2 + 1,
                                   docs[-1].id,
                                   vientitili_id,
                                   debit,
                                   abs(tapahtuma_sum),
                                   tapahtuma[csv_model['descol']],
                                   1
                                   ))
        docs[-1].add_entry(DbEntry(db_limits['last_entry_id'] + d * 2 + 2,
                                   docs[-1].id,
                                   vastatili_id,
                                   not debit,
                                   abs(tapahtuma_sum),
                                   tapahtuma[csv_model['descol']],
                                   2
                                   ))
    logger.debug(f"ADDED {len(docs)} DOCS, {len(docs) * 2} ENTRIES")
    return docs


def kirjoita_kantaan(docs_to_add, db_name):
    """ Function writes csv data into db
    :param docs_to_add: The data to ass as docs_to_add (list)
    :param db_name: filename of the db to add to
    :return: None
    """
    try:
        with sqlite3.connect(db_name) as tilitin_db:
            cursor = tilitin_db.cursor()
            max_bar = len(docs_to_add)*3
            with Bar("Kirjoitetaan...", max=max_bar) as bar:
                for itm in docs_to_add:
                    cursor.execute(itm.sql_str)
                    # print(itm.sql_str)
                    bar.next()
                    time.sleep(1 / max_bar)
                    for ent in itm.entries:
                        cursor.execute(ent.sql_str)
                        # print(ent.sql_str)
                        bar.next()
                        time.sleep(1 / max_bar)
                    # time.sleep(0.2)
                tilitin_db.commit()
    except sqlite3.OperationalError:
        logger.error(f'DB ERROR (kirjoita_kantaan()), db:{db_name}')
        print(f"Tietokantaa '{db_name} ei voitu avata, tai tietokanta ei ole tilitin-kanta")
        sys.exit(0)

    print()
    return None


def main():
    """ Main Loop
    :return: None
    """
    os.system('clear')
    logger.info("STARTED")
    db_name = args.dbName
    csv_name = args.csvName
    csv_model = select_bank()
    csv_data = read_bank_csv(csv_name, csv_model)
    db_limits, db_periods, vientitili_id, vastatili_id = read_db(db_name)
    os.system('clear')
    print_db_info(db_periods, db_limits)
    os.system('clear')
    # vientitili, vastatili = get_tilit()

    docs_to_add = create_new_items(csv_data, csv_model, db_limits, vientitili_id, vastatili_id)
    print(" DOC DNO    DATE    PER ENT DOC ROW ACC DEB        SUM  DESC")
    print("-----------------------------------------------------------------------------------")
    for item in docs_to_add:
        # print(item)
        for ent in item.entries:
            print(f"{item} {ent}")
    print("-----------------------------------------------------------------------------------")
    print()
    while True:
        kirjoitus = input("Kirjoitetaanko tiedot kantaan ? k/e : ")
        if kirjoitus.lower() == 'k':
            kirjoita_kantaan(docs_to_add, db_name)
            break
        elif kirjoitus.lower() == 'e':
            break
        else:
            print('Valitse k/e : ')
    logger.info("FINISHED")


if __name__ == '__main__':
    main()
