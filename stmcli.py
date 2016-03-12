#!/usr/bin/env python3

import argparse
import data
import database
import printinfo
import os

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bus-number", help="the # of the bus")
parser.add_argument("-s", "--bus-stop-code", help="the code of the bus stop")

db_file = "stm.db"


def main():

    # First time run test
    if not os.path.isfile(db_file):
        answer = input("No data found, update? [y/n] ")
        if answer == "y":
            data.download_gtfs_data()
            database.create_db()
            database.load_stm_data()
        else:
            print("Can't continue without data.")
            exit(0)

    # Checking for update
    if data.check_for_update():
        answer = input("Data update needed, update now? [y/n] ")
        if answer == "y":
            os.unlink(db_file)
            data.download_gtfs_data()
            database.create_db()
            database.load_stm_data()
        else:
            print("Data update needed for stmcli to work.")
            exit(0)

main()
