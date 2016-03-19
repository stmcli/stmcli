#!/usr/bin/env python3

import sqlite3
import time
from peewee import *


def next_departures(bus_number, stop_code, date, db_file):
    # Getting the 10 next departures
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    sql_var = (bus_number, stop_code, date)
    c.execute("""SELECT st.departure_time
                 FROM trips t
                 INNER JOIN stop_times st
                     ON t.trip_id=st.trip_id
                 INNER JOIN stops s
                     ON st.stop_id=s.stop_id
                 WHERE t.route_id=?
                 AND s.stop_code=?
                 AND service_id=(SELECT service_id
                     FROM calendar_dates
                     WHERE date=?)
                 ORDER BY st.departure_time""", sql_var)

    result = []
    for i in c.fetchall():
        result.append(i[0])
    conn.close()
    return result


def all_bus_stop(bus_number, db_file):
    # Getting all bus stop for this bus
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    sql_var = (bus_number, time.strftime('%Y%m%d'))

    c.execute("""SELECT stop_name, stop_code
                 FROM trips t
                 INNER JOIN stop_times st
                     ON t.trip_id=st.trip_id
                 INNER JOIN stops s
                     ON st.stop_id=s.stop_id
                 WHERE t.route_id=?
                 AND service_id=(SELECT service_id
                     FROM calendar_dates
                     WHERE date=?)
                 AND direction_id = 0
                 GROUP BY stop_code
                 ORDER BY stop_sequence
                 """, sql_var)

    result = ["Direction {0}".format("ADD DIRECTION 1 HERE")]
    for i in c.fetchall():
        result.append("[{0}] {1}".format(i[0], i[1]))

    c.execute("""SELECT stop_name, stop_code
                 FROM trips t
                 INNER JOIN stop_times st
                     ON t.trip_id=st.trip_id
                 INNER JOIN stops s
                     ON st.stop_id=s.stop_id
                 WHERE t.route_id=?
                 AND service_id=(SELECT service_id
                     FROM calendar_dates
                     WHERE date=?)
                 AND direction_id = 1
                 GROUP BY stop_code
                 ORDER BY stop_sequence
                 """, sql_var)

    result.append("Direction {0}".format("ADD DIRECTION 2 HERE"))
    for i in c.fetchall():
        result.append("[{0}] {1}".format(i[0], i[1]))

    conn.close()

    return result


def all_bus_for_stop_code(stop_code, db_file):
    # Getting all bus at this bus code
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    sql_var = (stop_code, time.strftime('%Y%m%d'))
    c.execute("""SELECT DISTINCT route_id
                 FROM trips t
                 INNER JOIN stop_times st
                     ON t.trip_id=st.trip_id
                 INNER JOIN stops s
                     ON st.stop_id=s.stop_id
                 AND s.stop_code=?
                 AND service_id=(SELECT service_id
                     FROM calendar_dates
                     WHERE date=?)""", sql_var)

    result = []
    for i in c.fetchall():
        result.append(i[0])
    conn.close()

    return result
