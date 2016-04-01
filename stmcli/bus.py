#!/usr/bin/env python3

import sqlite3
import time


def next_departures(bus_number, stop_code, date, time, nb_departure, db_file):
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

    query_result = []
    for i in c.fetchall():
        query_result.append(i[0])
    conn.close()

    result = []
    departures_listed = 0
    for i in query_result:
        dep_time = i.split(':')
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
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    sql_var = (bus_number, time.strftime('%Y%m%d'))

    c.execute("""SELECT stop_name, stop_code, trip_headsign
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
    query_result = c.fetchall()
    result = ["---------"]
    result.append("Direction {0}".format(query_result[0][2]))
    result.append("----------")

    for i in query_result:
        result.append("[{0}] {1}".format(i[0], i[1]))

    c.execute("""SELECT stop_name, stop_code, trip_headsign
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
    query_result = c.fetchall()
    result.append("----------")
    result.append("Direction {0}".format(query_result[0][2]))
    result.append("----------")

    for i in query_result:
        result.append("[{0}] {1}".format(i[0], i[1]))

    conn.close()

    return result


def all_bus_for_stop_code(stop_code, db_file):
    # Getting all bus at this bus code
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    sql_var = (stop_code,)
    c.execute("""SELECT DISTINCT route_id
                 FROM trips t
                 INNER JOIN stop_times st
                     ON t.trip_id=st.trip_id
                 INNER JOIN stops s
                     ON st.stop_id=s.stop_id
                 AND s.stop_code=?""", sql_var)

    result = []
    for i in c.fetchall():
        result.append(i[0])
    conn.close()

    return result


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
