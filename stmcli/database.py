#!/usr/bin/env python3

import os
import sqlite3
import unicodecsv


def init_table(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute('''CREATE TABLE agency
                 (agency_id char(3),
                 agency_name char(40) not null,
                 agency_url char(60) not null,
                 agency_timezone char(20) not null,
                 agency_lang char(10),
                 agency_phone char(20),
                 agency_fare_url char(255)
                 );''')
    conn.execute('''CREATE TABLE stops
                 (stop_id int primary key not null,
                 stop_code int,
                 stop_name char(50) not null,
                 stop_lat int not null,
                 stop_long int not null,
                 stop_url char(60),
                 wheelchair_accessible boolean
                 );''')
    conn.execute('''CREATE TABLE routes
                 (route_id int primary key not null,
                 agency_id int,
                 route_short_name char(10) not null,
                 route_long_name char(40) not null,
                 route_type char(10) not null,
                 route_url text,
                 route_color char(6),
                 route_text_color char(6)
                 );''')
    conn.execute('''CREATE TABLE trips
                 (route_id int not null,
                 service_id int not null,
                 trip_id char(20) primary key not null,
                 trip_headsign char(50),
                 direction_id boolean,
                 wheelchair_accessible int,
                 shape_id char(15),
                 note_fr char(255),
                 note_en char(255)
                 );''')
    conn.execute('''CREATE TABLE stop_times
                 (trip_id char(20) not null,
                 arrival_time char(8) not null,
                 departure_time char(8) not null,
                 stop_id int not null,
                 stop_sequence int not null
                 );''')
    conn.execute('''CREATE TABLE calendar_dates
                 (service_id char(3) not null,
                 date date not null,
                 exception_type boolean not null
                 );''')
    conn.close()


def load_data(data_file, db_file, stmcli_data_dir):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    file_path = "{0}/stm/".format(stmcli_data_dir) + data_file
    with open(file_path, 'rb') as input_file:
        reader = unicodecsv.reader(input_file, delimiter=",")
        data = [row for row in reader]

    if "agency" in data_file:
        print("agency")
        cursor.executemany('''INSERT INTO agency
                           VALUES (?, ?, ?, ?, ?, ?, ?);''', data)
    elif "stops" in data_file:
        print("stops")
        cursor.executemany('''INSERT INTO stops
                           VALUES (?, ?, ?, ?, ?, ?, ?);''', data)
    elif "routes" in data_file:
        print("routes")
        cursor.executemany('''INSERT INTO routes
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', data)
    elif "trips" in data_file:
        print("trips")
        cursor.executemany('''INSERT INTO trips
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', data)
    elif "stop_times" in data_file:
        print("stop_times")
        cursor.executemany('''INSERT INTO stop_times
                           VALUES (?, ?, ?, ?, ?);''', data)
    elif "calendar_dates" in data_file:
        print("calendar_dates")
        cursor.executemany('''INSERT INTO calendar_dates
                           VALUES (?, ?, ?);''', data)
    else:
        print("There is no table for " + data_file)
    conn.commit()
    conn.close()


def create_db(db_file):
    if not os.path.isfile(db_file):
        init_table(db_file)
        print("Database Created")
    else:
        print("Database already exist")


def load_stm_data(db_file, stmcli_data_dir):
    stm_file_dir = os.listdir("{0}/stm".format(stmcli_data_dir))
    for filename in stm_file_dir:
        load_data(filename, db_file, stmcli_data_dir)
