#!/usr/bin/env python3
import os
import glob
from playhouse.csv_loader import *
from peewee import *

database = SqliteDatabase('stm.db')


class BaseModel(Model):
    class Meta:
        database = database


class Agency(BaseModel):
    agency_id = CharField()
    agency_name = CharField()
    agency_url = CharField()
    agency_timezone = CharField()
    agency_lang = CharField()
    agency_phone = CharField()
    agency_fare_url = CharField()


class Stops(BaseModel):
    stop_id = IntegerField()
    stop_code = IntegerField()
    stop_name = CharField()
    stop_lat = IntegerField()
    stop_lon = IntegerField()
    stop_url = CharField()
    wheelchair_accessible = BooleanField()


class Routes(BaseModel):
    route_id = IntegerField()
    agency = ForeignKeyField(Agency)
    route_short_name = CharField()
    route_long_name = CharField()
    route_type = CharField()
    route_url = CharField()
    route_color = CharField()
    route_text_color = CharField()


class Trips(BaseModel):
    route = ForeignKeyField(Routes)
    service = IntegerField()
    trip = IntegerField()
    trip_headsign = CharField()
    direction_id = BooleanField()
    wheelchair_accessible = IntegerField()
    shape_id = IntegerField()
    note_fr = CharField()
    note_en = CharField()


class Stop_Times(BaseModel):
    trip = ForeignKeyField(Trips)
    arrival_time = CharField()
    departure_time = CharField()
    stop = ForeignKeyField(Stops)
    stop_sequence = IntegerField()


class Calendar_Dates(BaseModel):
    service = ForeignKeyField(Trips)
    date = DateField()
    exception_type = BooleanField()


def create_tables():
    database.connect()
    database.create_tables([Agency, Stops,
                            Routes, Trips, Stop_Times, Calendar_Dates])


def load_data():
    for csv_file in glob.glob('stm/*.txt'):
        print('Loading' + csv_file)
        data = load_csv(database, csv_file)
