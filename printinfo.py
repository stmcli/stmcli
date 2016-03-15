#!/usr/bin/env python3

import sqlite3
import time


def next_departures(bus_number, stop_code, db_location):
    # Getting the 10 next departures
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    sql_var = (bus_number, stop_code, time.strftime('%Y%m%d'))
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
                 ORDER BY st.departure_time
                 LIMIT 10""", sql_var)

    return c.fetchall()

    conn.close()
