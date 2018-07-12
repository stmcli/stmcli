#!/usr/bin/env python3

import time
import urllib

import peewee

from stmcli.models import CalendarDate, Stop, StopTime, Trip


def next_departures(bus_number, stop_code, date, time, nb_departure, db_file):
    """
    Getting the 10 next departures
    
    How to check with tools database
    sqlite3 stm.db
    SELECT "t2"."departure_time" FROM "trips" AS t1 INNER JOIN "stop_times" AS t2 ON ("t1"."trip_id" = "t2"."trip_id_id") INNER JOIN "stops" AS t3 ON ("t2"."stop_id_id" = "t3"."stop_id") WHERE ((("t1"."route_id_id" = '51') AND ("t3"."stop_code" = '51176')) AND ("t1"."service_id" = (SELECT "t4"."service_id" FROM "calendar_dates" AS t4 WHERE ("t4"."date" = '20180626')))) ORDER BY "t2"."departure_time" ;
    Replace 20180626 with the expected date
    make it also for bus number '51' and '51176'
    """

    subquery = CalendarDate.select(CalendarDate.service_id)\
        .where(CalendarDate.date == date)
    # Use of .in as CalendarDate could return more than one value for a day since 06/2018
    query_result = Trip.select(StopTime.departure_time)\
        .join(StopTime, on=(Trip.trip_id == StopTime.trip_id))\
        .join(Stop, on=(StopTime.stop_id == Stop.stop_id))\
        .where(
            (Trip.route_id == bus_number) &
            (Stop.stop_code == stop_code) &
            (Trip.service_id .in_( subquery)))\
        .order_by(StopTime.departure_time)

    result = []
    departures_listed = 0
    for i in query_result.dicts():
        dep_time = i['departure_time'].split(':')
        if dep_time[0] == time[0] and dep_time[1] >= time[1]:
            result.append("{0}:{1}".format(dep_time[0], dep_time[1]))
            departures_listed += 1
        elif dep_time[0] > time[0]:
            result.append("{0}:{1}".format(dep_time[0], dep_time[1]))
            departures_listed += 1

        if departures_listed is nb_departure:
            break

    return result


def all_bus_stop(bus_number, db_file):
    # Getting all bus stop for this bus
    result = []

    subquery = CalendarDate.select(CalendarDate.service_id)\
        .where(CalendarDate.date == time.strftime('%Y%m%d'))

    query = Trip.select(Stop.stop_name, Stop.stop_code, Trip.trip_headsign)\
        .join(StopTime, on=(Trip.trip_id == StopTime.trip_id))\
        .join(Stop, on=(StopTime.stop_id == Stop.stop_id))\
        .where(
            (Trip.route_id == bus_number) &
            (Trip.service_id == subquery) &
            (Trip.direction_id == 0))\
        .group_by(Stop.stop_code)\
        .order_by(StopTime.stop_sequence)

    query_result = query.dicts()
    if len(query_result) > 0:
        result = ["---------"]
        result.append("Direction {0}".format(query_result[0]['trip_headsign']))
        result.append("----------")

        for i in query_result:
            result.append("[{0}] {1}".format(i['stop_name'], i['stop_code']))

    query = Trip.select(Stop.stop_name, Stop.stop_code, Trip.trip_headsign)\
        .join(StopTime, on=(Trip.trip_id == StopTime.trip_id))\
        .join(Stop, on=(StopTime.stop_id == Stop.stop_id))\
        .where(
            (Trip.route_id == bus_number) &
            (Trip.service_id == subquery) &
            (Trip.direction_id == 1))\
        .group_by(Stop.stop_code)\
        .order_by(StopTime.stop_sequence)

    query_result = query.dicts()
    if len(query_result) > 0:
        result = ["---------"]
        result.append("Direction {0}".format(query_result[0]['trip_headsign']))
        result.append("----------")

        for i in query_result:
            result.append("[{0}] {1}".format(i['stop_name'], i['stop_code']))

    return result


def all_bus_for_stop_code(stop_code, db_file):
    # Getting all bus at this bus code

    query = Trip.select(peewee.fn.Distinct(Trip.route_id))\
        .join(StopTime, on=(Trip.trip_id == StopTime.trip_id))\
        .join(Stop, on=(StopTime.stop_id == Stop.stop_id))\
        .where(Stop.stop_code == stop_code)

    for i in query.tuples():
        yield i[0]


def metro_status(line, language):
    # Getting XML data
    URL = "http://www2.stm.info/1997/alertesmetro/esm.xml"
    metro_website = urllib.request.urlopen(URL)
    metro_info = metro_website.read()
    metro_website.close()

    xml_data = xmltodict.parse(metro_info)

    for i in xml_data['Root']['Ligne']:
        nline = i["NoLigne"]
        if line == "green" and nline == "1" or line == "all" and nline == "1":
            print("Green line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))

        if line == "orange" and nline == "2" or line == "all" and nline == "2":
            print("Orange line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))

        if line == "yellow" and nline == "4" or line == "all" and nline == "4":
            print("Yellow line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))

        if line == "blue" and nline == "5" or line == "all" and nline == "5":
            print("Blue line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))
