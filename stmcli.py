#!/usr/bin/env python3

import argparse
import data
import database
import os
import printinfo
import time

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bus-number", help="the # of the bus")
parser.add_argument("-s", "--bus-stop-code", help="the code of the bus stop")
parser.add_argument("-n", "--number-departure",
                    help="the code of the bus stop. "
                         "Only works with both -b and -s specified")
parser.add_argument("-d", "--date",
                    help="specify the date to use when getting"
                         " Departure times. Format: aaaammjj")
parser.add_argument("-t", "--time",
                    help="specify the time to use when getting"
                    " Departure times. Format: HH:MM")
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
        # Print the 10 next departures
        if not args.date:
            curr_date = time.strftime('%Y%m%d')
        else:
            curr_date = args.date

        next_departures = printinfo.next_departures(args.bus_number,
                                                    args.bus_stop_code,
                                                    curr_date,
                                                    db_file)
        if not args.time:
            curr_time = time.strftime('%H:%M').split(':')
        else:
            curr_time = args.time.split(':')

        if not args.number_departure:
            max_departure = 10
        else:
            max_departure = int(args.number_departure)

        departures_listed = 0
        for i in next_departures:
            dep_time = i.split(':')
            if dep_time[0] >= curr_time[0] and dep_time[1] >= curr_time[1]:
                print(i)
                departures_listed += 1

            if departures_listed is max_departure:
                break

    elif args.bus_number:
        # Print all bus stops for a bus
        bus_stops = printinfo.all_bus_stop(args.bus_number, db_file)

        for i in bus_stops:
            print(i)

    elif args.bus_stop_code:
        # Print all bus for a stop code
        bus = printinfo.all_bus_for_stop_code(args.bus_stop_code, db_file)

        for i in bus:
            print(i)

main()
