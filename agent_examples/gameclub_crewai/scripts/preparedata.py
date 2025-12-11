# -*- coding: utf-8 -*-
# copyright 2025 Snow Leopard, Inc


# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///


import argparse
import csv
import os
import sqlite3
import sys

from datetime import date, datetime

from sqlalchemy import create_engine, insert, MetaData


program_name = 'preparedata'
program_description = 'convert metacritic csv file to sqlite'


def identity(o):
    """
    return the parameter unchanged.
    """
    return o


@staticmethod
def str_to_float_with_null_tbd(s):
    """
    dataset-specific converter from string to float.  the dataset uses "tbd" when a userscore
    hasn't been calculated yet.
    """
    return None if s == 'tbd' else float(s)


def short_us_date_str_to_date(s):
    """
    parse abbreviated US-ordered date string (e.g. 'Oct 10, 2017') into a datetime.date
    """
    dt = datetime.strptime(s, '%b %d, %Y')
    return date(dt.year, dt.month, dt.day)


def csv_to_sqlite(sqlite_path, csv_reader, table_name, columns):
    """
    convert the contents of a csv.DictReader to a table in a sqlite file
    """
    # read the first row of the CSV so csv_reader.fieldnames is populated
    row = next(csv_reader)

    # prepare column records from headers
    column_def = {}
    column_missing = []
    column_def_type = []
    for fieldname in csv_reader.fieldnames:
        cDef = columns.get(fieldname)
        if cDef is None:
            column_missing.append(fieldname)
        if not isinstance(cDef, tuple):
            column_def_type.append(fieldname)
        else:
            column_def[fieldname] = cDef

    if column_missing:
        raise ValueError(f"exact match(es) for column definition not found for: {', '.join(column_missing)}")
    if column_def_type:
        raise ValueError(f"expected tuple for column definition: {', '.join(column_def_type)}")
    if not columns:
        raise ValueError('no columns found')

    # create table, assuming it doesn't already exist
    # NOTE: we create the table manually instead of creating sqlalchemy metadata because we want
    #   to control the storage class of the sqlite columns through type affinity rules.  we may
    #   change this approach in the future if we want to support more sophisticated tables.
    column_sql = []
    converters = {}
    for fieldname, (column_name, column_type, column_converter) in column_def.items():
        column_sql.append(f'{column_name} {column_type}')
        converters[fieldname] = (column_name, column_converter if column_converter is not None else identity)
    # TODO: better SQL string replacement
    createTable = f"CREATE TABLE {table_name} ({', '.join(column_sql)})"

    with sqlite3.connect(sqlite_path) as conn:
        conn.execute(createTable)

    # make sqlalchemy engine and metadata
    engine = create_engine(f'sqlite:///{sqlite_path}')
    metadata = MetaData()

    # reflect the table we just created
    metadata.reflect(bind=engine, only=[table_name])
    table = metadata.tables[table_name]

    # populate table
    with engine.connect() as conn:
        try:
            reading = True
            while reading:
                try:
                    values = {}
                    for fieldname, (column_name, converter) in converters.items():
                        # NOTE: the first row is read at the beginning of the function
                        values[column_name] = converter(row[fieldname])
                    query = insert(table).values(**values)
                    conn.execute(query)
                    row = next(csv_reader)
                except StopIteration:
                    reading = False
            conn.commit()
        except Exception:
            print('failed to write data')
            conn.rollback()


def csv_to_sqlite_from_path(sqlite_path, csv_path, table_name, columns):
    """
    convert the contents of a .csv file at a given path to a table in a sqlite file
    """
    # NOTE: csv.reader() requires the newline='' kwarg for open()
    with open(csv_path, 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return csv_to_sqlite(sqlite_path, csv_reader, table_name, columns)


def get_metacritic_table_def():
    """
    return (table_name, column_defs) tuple, where:
      table_name, str: name of the table to create
      columns. dict[str, column_def]: the set of columns to create, order is preserved, where
        keys are the name of the column header from the .csv, and values are:
        column_def, tuple[str, str, Optional[Callable]]: a tulple of the column name, type name,
          and an optional converter function from the string value in the .csv to the desired
          type.  if the converter function is None, the string from the .csv is used directly.
    """
    columns = {
        'metascore': ('metascore_percent', 'INTEGER', int),
        'name': ('name', 'TEXT', None),
        'console': ('console', 'TEXT', None),
        'userscore': ('userscore_10_points', 'FLOAT', str_to_float_with_null_tbd),
        'date': ('date', 'DATE_CHAR', short_us_date_str_to_date),
    }

    return 'metacritic', columns


def parse_args(argv):
    parser = argparse.ArgumentParser(prog=program_name, description=program_description)

    parser.add_argument('--clean', '-c', action='store_true', help='when present, delete an existing sqlite file')
    parser.add_argument('csvfile', help='the metacritic CSV file')
    parser.add_argument('sqlitefile', help='the sqlite file to write to')

    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    # handle --clean option
    try:
        os.stat(args.sqlitefile)
    except FileNotFoundError:
        pass
    else:
        if not args.clean:
            print('refusing to replace output file without `--clean`:', repr(args.sqlitefile))
            return
        os.unlink(args.sqlitefile)

    table_name, columns = get_metacritic_table_def()

    csv_to_sqlite_from_path(args.sqlitefile, args.csvfile, table_name, columns)


if __name__ == '__main__':
    main()
