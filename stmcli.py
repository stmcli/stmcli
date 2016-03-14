#!/usr/bin/env python3

import argparse
import data
import database
import os

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bus-number", help="the # of the bus")
parser.add_argument("-s", "--bus-stop-code", help="the code of the bus stop")
args = parser.parse_args()

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

    if args.bus_number and args.bus_stop_code:
        print("TODO")
        # print_next_departures(args.bus_number, args.bus_stop_code)
    elif args.bus_number:
        print("TODO")
        # print_all_bus_stop(args.bus_number)
    elif args.bus_stop_code:
        print("TODO")
        # print_all_bus_for_stop_code(args.bus_stop_code)

main()
