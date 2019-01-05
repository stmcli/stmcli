import os
import shutil
import time
import unicodedata
import urllib
from urllib import error, request
import zipfile

import peewee

from stmcli import database, models
import datetime


def download_gtfs_data(data_dir):
    extract_location = "{0}/stm/".format(data_dir)

    try:
        output_zip = "{0}/gtfs.zip".format(data_dir)
        zip_url = "http://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

        urllib.request.urlretrieve(zip_url, output_zip)

    except urllib.error.HTTPError as err:
        print("Error {0} while trying to downloads stm infos".format(err))
        exit(1)

    # Extracting
    if not os.path.isdir(extract_location):
        os.makedirs(extract_location)

    zip = zipfile.ZipFile(output_zip)
    zip.extractall(path=extract_location)

    os.unlink(output_zip)


def check_for_update(db_file, data_dir, force_update):
    # Check if db_file exist
    database.init_database(db_file)
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
    try:
        # Use table Calendar as update from december 2018
        day_of_week = datetime.datetime.strptime(curr_date, "%Y%m%d").strftime("%A").lower()
        
        t = models.Calendar.get(
                (curr_date >= models.Calendar.start_date) & 
                (curr_date <= models.Calendar.end_date) &
                (getattr( models.Calendar, day_of_week) == 1)
                )
        
    except Exception as e:
        # Add robustness in case of unexpected exception from peewee when database does not have data 
        t = None

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
    models.db = peewee.SqliteDatabase(db_file)

    # Use table Calendar as update from december 2018
    day_of_week = datetime.datetime.strptime(date, "%Y%m%d").strftime("%A").lower()
    
    t = models.Calendar.get(
            (date >= models.Calendar.start_date) & 
            (date <= models.Calendar.end_date) &
            (getattr( models.Calendar, day_of_week) == 1)
            )

    if t is None:
        return False
    else:
        return True


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')
