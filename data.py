#!/usr/bin/env python3

import data
import database
import os
import sqlite3
import time
import urllib
from urllib import error, request
import zipfile


def download_gtfs_data():
    try:
        output_dir = os.path.dirname(os.path.realpath(__file__)) + "/gtfs.zip"
        zip_url = "http://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

        urllib.request.urlretrieve(zip_url, output_dir)

    except urllib.error.HTTPError as err:
        print("Error {0} while trying to downloads stm infos")
        exit(1)

    # Extracting to stm/ and deleting zip
    extract_location = "stm/"

    if not os.path.isdir(extract_location):
        os.makedirs(extract_location)

    zip = zipfile.ZipFile('gtfs.zip')
    zip.extractall(path=extract_location)

    os.unlink("gtfs.zip")


def check_for_update(db_file):
    # Check if db_file exist
    if not os.path.isfile(db_file):
        answer = input("No data found, update? [y/n] ")
        if answer == "y":
            data.download_gtfs_data()
            database.create_db()
            database.load_stm_data()
        else:
            print("Can't continue without data.")
            exit(0)

    # Check if GTFS data update is needed
    curr_date = time.strftime('%Y%m%d')

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT * FROM calendar_dates WHERE date={0}'.format(curr_date))
    t = c.fetchone()
    conn.close()

    if t is None or not os.path.isfile(db_file):
        answer = input("Data update needed, update now? [y/n] ")
        if answer == "y":
            os.unlink(db_file)
            data.download_gtfs_data()
            database.create_db()
            database.load_stm_data()
        else:
            print("Data update needed for stmcli to work.")
            exit(0)


def date_in_scope(date):

    conn = sqlite3.connect('stm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM calendar_dates WHERE date={0}'.format(date))
    t = c.fetchone()
    conn.close()

    if t is None:
        return False
    else:
        return True
