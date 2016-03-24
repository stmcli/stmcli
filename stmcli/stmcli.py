#!/usr/bin/env python3

import argparse
import data
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


def set_date(db_file):
    if not args.date:
        return time.strftime('%Y%m%d')
    else:
        if len(str(args.date)) != 8:
            print("date format is aaaammjj. Ex: 20160218")
            exit(1)
        else:
            if not data.date_in_scope(args.date, db_file):
                print("We don't have any info for this date.")
                exit(1)
            else:
                return args.date


def set_time():
    if not args.time:
        return time.strftime('%H:%M').split(':')
    else:
        custom_time = args.time.split(':')
        if len(custom_time) != 2:
            print("time format is HH:MM. Ex: 06:23")
            exit(1)
        elif len(str(custom_time[0])) != 2 or len(str(custom_time[1])) != 2:
            print("time format is HH:MM. Ex: 06:23")
            exit(1)

        return custom_time


def set_number_departure():
    if not args.number_departure:
        return 10
    else:
        return int(args.number_departure)


def main():

    stmcli_data_dir = "{0}/.stmcli/".format(os.path.expanduser('~'))
    db_file = "{0}/stm.db".format(stmcli_data_dir)

    if not os.path.isdir(stmcli_data_dir):
        os.makedirs(stmcli_data_dir)

    # Checking for updates
    data.check_for_update(db_file, stmcli_data_dir)

    # Print the next departures
    if args.bus_number and args.bus_stop_code:

        # getting date and time
        date = set_date(db_file)
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
            print(i.encode('ascii', 'replace'))

    elif args.bus_stop_code:
        # Print all bus for a stop code
        bus = printinfo.all_bus_for_stop_code(args.bus_stop_code, db_file)

        for i in bus:
            print(i.encode('ascii', 'replace'))

main()
