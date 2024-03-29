import sqlite3
import os
from pathlib import Path

from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / 'database' / 'euro_counter.sqlite3'


# This is mostly a test function, the database should not be destroyed from now on.
@DeprecationWarning
def recreate_database(recreate=False):
    """
    Function for creating or recreating the entire database. USE WITH CAUTION.
    :param recreate: Whether the database is being created from scratch or being recreated,
    if it is being recreated then it is necessary to delete the tables first and then create the database.
    :return: Nothing
    """
    conn = sqlite3.connect(DB_PATH.__str__())
    cur = conn.cursor()

    if recreate:  # If the database is not being created for the first time, we need to destroy it.
        cur.execute("DROP TABLE video_type;")
        cur.execute('DROP TABLE video;')
        cur.execute('DROP TABLE measurement;')

    cur.execute("CREATE TABLE video_type("
                "type_id serial PRIMARY KEY, description VARCHAR);")

    cur.execute("CREATE TABLE video("
                "video_id serial PRIMARY KEY, name VARCHAR, "
                "link VARCHAR, type_id INTEGER REFERENCES video_type(type_id));")

    cur.execute("CREATE TABLE measurement("
                "measurement_id serial PRIMARY KEY, measurement_time TIMESTAMP, "
                #"views BIGINT, likes BIGINT, dislikes BIGINT, comment_count BIGINT, "
                "views BIGINT, likes BIGINT, comment_count BIGINT, "
                "video_id INTEGER REFERENCES video(video_id));")
    cur.close()
    conn.close()


def store_data(data):
    # TODO: This could be further clarified.
    """
    Function for storing the data in the database. It has to go through various checks to see if the tables
    it is inserting already exist.

    :param data: The data that should be inserted.
    :return: Nothing.
    """
    conn = sqlite3.connect(DB_PATH.__str__())
    cur = conn.cursor()

    cur.execute('SELECT COUNT(1) FROM video_type WHERE description = (?)', (data['description'],))
    type_exists = cur.fetchall()[0][0]

    if not type_exists:
        cur.execute('INSERT INTO video_type (description) VALUES (?)', (data['description'],))

    #video_type = cur.lastrowid

    cur.execute('SELECT rowid FROM video_type WHERE description = (?)', (data['description'],))
    video_type = cur.fetchall()[0][0]

    for video_data in data['videos']:
        cur.execute('SELECT COUNT(1) FROM video WHERE link = (?)', (video_data,))
        video_exists = cur.fetchall()[0][0]

        if not video_exists:
            cur.execute('INSERT INTO video (name, link, type_id) VALUES (?, ?, ?)',
                        (data['videos'][video_data]['name'], video_data, video_type))

        #video_id = cur.lastrowid
        cur.execute('SELECT rowid FROM video WHERE link = (?)', (video_data,))
        video_id = cur.fetchall()[0][0]

        # cur.execute('INSERT INTO measurement (measurement_time, views, likes, dislikes, comment_count, video_id)'
        cur.execute('INSERT INTO measurement (measurement_time, views, likes, comment_count, video_id)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (data['timestamp'], data['videos'][video_data]['views'],
                     # data['videos'][video_data]['likes'], data['videos'][video_data]['dislikes'],
                     data['videos'][video_data]['likes'],
                     data['videos'][video_data]['comments'], video_id))

    conn.commit()
    cur.close()
    conn.close()
    
    
def read_data():

    conn = sqlite3.connect(DB_PATH.__str__())
    cur = conn.cursor()

    cur.execute('SELECT measurement.views, measurement.measurement_time, video.name, video_type.description '
                'FROM video '
                'JOIN measurement ON video.rowid = measurement.video_id '
                'JOIN video_type ON video.type_id = video_type.rowid '
                #'WHERE video_type.description = "Euro semi finals unofficial 2018" '
                'WHERE video_type.description = "Euro semi finals 1 2018" '
                'OR video_type.description = "Euro semi finals 2 2018" '
                'OR video_type.description = "Euro semi finals unofficial 2018" '
                'ORDER BY video.name ASC, measurement.measurement_time ASC;')
    data_from_db = cur.fetchall()

    #print(data_from_db)

    cur.close()
    conn.close()

    return data_from_db


def read_data_with_video_type(video_type_input_list, year):

    # Cutoff point for the relevant data, later data is irrelevant.
    if year == '2021':
        last_relevant_date = datetime(year=int(year), month=5, day=25)
    else:
        last_relevant_date = datetime(year=int(year), month=5, day=22)
    #last_relevant_date = datetime(year=int(year), month=6, day=1)

    conn = sqlite3.connect(DB_PATH.__str__())
    cur = conn.cursor()

    question_marks = '?' * len(video_type_input_list)  # Create as many question marks as the list is long.

    # Formatted query string, for arbitrary number of variables for 'video_type.description'
    query = """
      SELECT measurement.views, measurement.measurement_time, video.name, video_type.description, 
      measurement.likes, measurement.comment_count 
      FROM video 
      JOIN measurement ON video.rowid = measurement.video_id 
      JOIN video_type ON video.type_id = video_type.rowid 
      WHERE video_type.description IN ({}) 
      AND measurement_time < ? 
      ORDER BY video.name ASC, measurement.measurement_time ASC;
    """.format(','.join(question_marks))

    query_args = list(video_type_input_list)
    query_args.extend([last_relevant_date])  # All of the queried variables in a single list.

    cur.execute(query, query_args)  # Execute the query.

    data_from_db = cur.fetchall()

    cur.close()
    conn.close()

    return data_from_db


def read_data_with_year(year_input):

    first_date = datetime(year=int(year_input), month=1, day=1)
    print('first date: ', first_date)
    last_date = datetime(year=int(year_input), month=12, day=31)
    print('last_date:', last_date)

    conn = sqlite3.connect(DB_PATH.__str__())
    cur = conn.cursor()
    cur.execute('SELECT measurement.views, measurement.measurement_time, video.name, video_type.description '
                'FROM video '
                'JOIN measurement ON video.rowid = measurement.video_id '
                'JOIN video_type ON video.type_id = video_type.rowid '
                'WHERE measurement_time > ?'
                ' AND measurement_time < ?'
                ' AND video_type.description = ?'
                ' ORDER BY video.name ASC, measurement.measurement_time ASC;', (first_date, last_date))
    data_from_db = cur.fetchall()

    cur.close()
    conn.close()
    return data_from_db
