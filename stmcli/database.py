import itertools
import os
import sqlite3

import peewee
import unicodecsv

from stmcli import models


def init_database(db_file):
    models.db = peewee.SqliteDatabase(db_file)

    def is_peewee_class(x):
        attr = getattr(models, x)
        return (
            hasattr(attr, '_meta') and
            issubclass(attr, peewee.Model)
        )

    # retrieve the peewee models from the file
    tables_models = []
    for attr in dir(models):
        maybe_model = getattr(models, attr)
        if (hasattr(maybe_model, '_meta') and
                issubclass(maybe_model, peewee.Model)):
            tables_models.append(maybe_model)

    # associate the tables to the sqlite database
    for tbm in tables_models:
        setattr(tbm._meta, 'database', models.db)

    return tables_models


def init_tables(db_file):
    tables_models = init_database(db_file)

    models.db.connect()
    models.db.create_tables(tables_models)
    models.db.close()


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


def load_data(data_file, db_file, stmcli_data_dir):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    file_path = "{0}/stm/".format(stmcli_data_dir) + data_file
    with open(file_path, 'rb') as input_file:
        reader = unicodecsv.reader(input_file, delimiter=",")

        if 'agency' in data_file:
            table = 'agency'
            values = '(?, ?, ?, ?, ?, ?, ?)'
        elif 'stops' in data_file:
            table = 'stops'
            values = '(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        elif 'routes' in data_file:
            table = 'routes'
            values = '(?, ?, ?, ?, ?, ?, ?, ?)'
        elif 'trips' in data_file:
            table = 'trips'
            values = '(null, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        elif 'stop_times' in data_file:
            table = 'stop_times'
            values = '(null, ?, ?, ?, ?, ?)'
        elif 'calendar.' in data_file:
            table = 'calendar'
            values = '(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        elif 'calendar_dates' in data_file:
            table = 'calendar_dates'
            values = '(null, ?, ?, ?)'
        else:
            print("Ignored file {}".format(data_file))
            conn.close()
            return

        print(table)

        size = models.SQLITE_MAX_VARIABLE_NUMBER

        # optimizing sqlite for a huge bulk insert
        # ideas gotten here
        # http://codificar.com.br/blog/sqlite-optimization-faq/
        cursor.execute('PRAGMA synchronous=OFF')
        cursor.execute('PRAGMA count_changes=OFF')
        cursor.execute('PRAGMA temp_store=2')  # memory
        cursor.execute('PRAGMA cache_size=20000')
        for chunk in chunks(reader, size):
            cursor.executemany('''
                INSERT INTO {table}
                VALUES {values};
            '''.format(
                table=table,
                values=values), chunk)
            conn.commit()

        cursor.execute('PRAGMA synchronous=ON')
        cursor.execute('PRAGMA count_changes=ON')
        cursor.execute('PRAGMA temp_store=0')  # disk
        cursor.execute('PRAGMA cache_size=2000')
        conn.close()


def create_db(db_file):
    if not os.path.isfile(db_file):
        init_tables(db_file)
        print("Database Created")
    else:
        print("Database already exist")


def load_stm_data(db_file, stmcli_data_dir):
    stm_file_dir = os.listdir("{0}/stm".format(stmcli_data_dir))
    for filename in sorted(stm_file_dir):
        load_data(filename, db_file, stmcli_data_dir)
