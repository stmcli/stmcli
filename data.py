#!/usr/bin/env python3

import os
import urllib
import urllib.error
import urllib.request


def download_gtfs_zip():
    try:
        output_dir = os.path.dirname(os.path.realpath(__file__)) + "/gtfs.zip"
        zip_url = "http://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

        urllib.request.urlretrieve(zip_url, output_dir)

    except urllib.error.HTTPError as err:
        print("Error {0} while trying to downloads stm infos")
        exit(1)
