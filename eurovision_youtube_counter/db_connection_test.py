import sqlite3


def recreate_database(recreate=False):
    conn = sqlite3.connect('database\db_test.sqlite3')
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
                "views BIGINT, likes BIGINT, dislikes BIGINT, comment_count BIGINT, "
                "video_id INTEGER REFERENCES video(video_id));")
    cur.close()
    conn.close()


def store_data(data):
    conn = sqlite3.connect('database\db_test.sqlite3')
    cur = conn.cursor()

    cur.execute('SELECT COUNT(1) FROM video_type WHERE description = (?)', (data['description'],))
    type_exists = cur.fetchall()[0][0]

    if not type_exists:
        cur.execute(('INSERT INTO video_type (description) VALUES (?)'), (data['description'],))

    #video_type = cur.lastrowid

    cur.execute('SELECT rowid FROM video_type WHERE description = (?)', (data['description'],))
    video_type = cur.fetchall()[0][0]

    for video_data in data['videos']:
        cur.execute('SELECT COUNT(1) FROM video WHERE link = (?)', (video_data,))
        video_exists = cur.fetchall()[0][0]

        if not video_exists:
            cur.execute(('INSERT INTO video (name, link, type_id) VALUES (?, ?, ?)'),
                        (data['videos'][video_data]['name'], video_data, video_type))

        #video_id = cur.lastrowid
        cur.execute('SELECT rowid FROM video WHERE link = (?)', (video_data,))
        video_id = cur.fetchall()[0][0]
        #print('ttest', test)


        cur.execute('INSERT INTO measurement (measurement_time, views, likes, dislikes, comment_count, video_id)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (data['timestamp'], data['videos'][video_data]['views'],
                     data['videos'][video_data]['likes'], data['videos'][video_data]['dislikes'],
                     data['videos'][video_data]['comments'], video_id))

    conn.commit()
    cur.close()
    conn.close()
    
    
def read_data():
    conn = sqlite3.connect('database\db_test.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM measurement;")
    test = cur.fetchall()
    #print(test)

    cur.execute('SELECT measurement.views, measurement.measurement_time, video.name, video_type.description '
                'FROM video '
                'JOIN measurement ON video.rowid = measurement.video_id '
                'JOIN video_type ON video.type_id = video_type.rowid '
                #'WHERE video_type.description = "Euro semi finals 2" '
                'ORDER BY video.name ASC, measurement.measurement_time ASC;')
    data_from_db = cur.fetchall()

    #print(data_from_db)

    cur.close()
    conn.close()

    return data_from_db
