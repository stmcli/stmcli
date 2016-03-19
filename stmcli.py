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
                    help="The number of departures to print. "
                         "Only works with both -b and -s specified")
parser.add_argument("-d", "--date",
                    help="specify the date to use when getting"
                         " Departure times. Format: aaaammjj")
parser.add_argument("-t", "--time",
                    help="specify the time to use when getting"
                    " Departure times. Format: HH:MM")
args = parser.parse_args()

db_file = "stm.db"


def first_time_check():
    if not os.path.isfile(db_file):
        answer = input("No data found, update? [y/n] ")
        if answer == "y":
            data.download_gtfs_data()
            database.create_db()
            database.load_stm_data()
        else:
            print("Can't continue without data.")
            exit(0)


def check_for_update():
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


def set_date():
    if not args.date:
        return time.strftime('%Y%m%d')
    else:
        if len(str(args.date)) != 8:
            print("date format is aaaammjj. Ex: 20160218")
            exit(1)
        else:
            return args.date


def set_time():
    if not args.time:
        return time.strftime('%H:%M').split(':')
    else:
        custom_time = args.time.split(':')
        if len(time) != 2:
            print("time format is HH:MM. Ex: 06:23")
            exit(1)
        elif len(str(time[0])) != 2 or len(str(time[1])) != 2:
            print("time format is HH:MM. Ex: 06:23")
            exit(1)

        return custom_time


def set_number_departure():
    if not args.number_departure:
        return 10
    else:
        return int(args.number_departure)


def main():

    # Checking for updates
    first_time_check()
    check_for_update()

    # Print the next departures
    if args.bus_number and args.bus_stop_code:

        # getting date and time
        date = set_date()
        time = set_time()
        number_departure = set_number_departure()

        next_departures = printinfo.next_departures(args.bus_number,
                                                    args.bus_stop_code,
                                                    date,
                                                    time,
                                                    number_departure,
                                                    db_file)

        for i in next_departures:
            print(i)

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
