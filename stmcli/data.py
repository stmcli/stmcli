#!/usr/bin/env python3

from stmcli import database
import os
import sqlite3
import shutil
import time
import urllib
from urllib import error, request
import zipfile


def download_gtfs_data(data_dir):
    extract_location = "{0}/stm/".format(data_dir)

    try:
        output_zip = "{0}/gtfs.zip".format(data_dir)
        zip_url = "http://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

        urllib.request.urlretrieve(zip_url, output_zip)

    except urllib.error.HTTPError as err:
        print("Error {0} while trying to downloads stm infos")
        exit(1)

    # Extracting
    if not os.path.isdir(extract_location):
        os.makedirs(extract_location)

    zip = zipfile.ZipFile(output_zip)
    zip.extractall(path=extract_location)

    os.unlink(output_zip)


def check_for_update(db_file, data_dir, force_update):
    # Check if db_file exist
    if not os.path.isfile(db_file):
        answer = "y"
        if not force_update:
            answer = input("No data found, update? [y/n] ")
        if answer == "y":
            download_gtfs_data(data_dir)
            database.create_db(db_file)
            database.load_stm_data(db_file, data_dir)
            shutil.rmtree("{0}/stm".format(data_dir))
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
        answer = "y"
        if not force_update:
            answer = input("Data update needed, update now? [y/n] ")
        if answer == "y":
            os.unlink(db_file)
            download_gtfs_data(data_dir)
            database.create_db(db_file)
            database.load_stm_data(db_file, data_dir)
            shutil.rmtree("{0}/stm".format(data_dir))
        else:
            print("Data update needed for stmcli to work.")
            exit(0)


def date_in_scope(date, db_file):

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT * FROM calendar_dates WHERE date={0}'.format(date))
    t = c.fetchone()
    conn.close()

    if t is None:
        return False
    else:
        return True
