#!/usr/bin/env python3

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


def check_for_update():  # Return True if update is needed, False if not
    curr_date = time.strftime('%Y%m%d')

    # Getting last update date in stm.db
    conn = sqlite3.connect('stm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM calendar_dates WHERE date={0}'.format(curr_date))
    t = c.fetchone()
    conn.close()

    if t is None:
        return True
    else:
        return False
