#!/usr/bin/env python3

import datetime
import os
import sqlite3
import time
import urllib
from urllib import error, request


def download_gtfs_zip():
    try:
        output_dir = os.path.dirname(os.path.realpath(__file__)) + "/gtfs.zip"
        zip_url = "http://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

        urllib.request.urlretrieve(zip_url, output_dir)

    except urllib.error.HTTPError as err:
        print("Error {0} while trying to downloads stm infos")
        exit(1)

    # Inserting date updated in db
    conn = sqlite3.connect('stm.db')
    c = conn.cursor()
    c.execute("UPDATE download_date SET download_date=DATE('now')")
    conn.commit()
    conn.close()


def check_for_update(): # Return True if update is needed, False if not
    now = int(time.time())
    current_year = time.strftime('%Y', time.localtime(now))

    # Getting last update date in stm.db
    conn = sqlite3.connect('stm.db')
    c = conn.cursor()
    c.execute('SELECT download_date FROM download_date')
    t = c.fetchone()[0]
    conn.close()

    last_update = datetime.date(*(int(s) for s in t.split('-')))
    last_update = (int(last_update.strftime("%s")))
    last_update_year = time.strftime('%Y', time.localtime(last_update))

    if str(current_year) != str(last_update_year):
        return True
    else:
        print(get_part_of_year(now))
        print(get_part_of_year(last_update))
        if get_part_of_year(now) == get_part_of_year(last_update):
            return False
        else:
            return True


def get_part_of_year(epoch_time):
    current_year = int(time.strftime('%Y'))

    # These are the dates where we need to update the gtfs datas
    jan4 = int(datetime.datetime(current_year, 1, 4, 5, 0).timestamp())
    mar21 = int(datetime.datetime(current_year, 3, 21, 5, 0).timestamp())
    jun20 = int(datetime.datetime(current_year, 6, 20, 5, 0).timestamp())
    aug29 = int(datetime.datetime(current_year, 8, 29, 5, 0).timestamp())
    oct31 = int(datetime.datetime(current_year, 10, 31, 5, 0).timestamp())

    if epoch_time > jan4 and epoch_time < mar21:
        epoch_time_part_of_year = 1
    elif epoch_time > mar21 and epoch_time < jun20:
        epoch_time_part_of_year = 2
    elif epoch_time > jun20 and epoch_time < aug29:
        epoch_time_part_of_year = 3
    elif epoch_time > aug29 and epoch_time < oct31:
        epoch_time_part_of_year = 4
    elif epoch_time > oct31 and epoch_time < jan4:
        epoch_time_part_of_year = 5

    return epoch_time_part_of_year
