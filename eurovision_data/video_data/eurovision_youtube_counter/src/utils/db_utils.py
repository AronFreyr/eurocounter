import os
import sqlite3


# Don't use again, it worked successfully the first time. No need to try to insert old data again.
@DeprecationWarning
def join_old_and_new_db():
    new_db_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), r'../../database/euro_counter.sqlite3')
    new_conn = sqlite3.connect(new_db_path)
    new_cur = new_conn.cursor()

    old_db_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), r'../../database/youtube_info.sqlite3')
    old_conn = sqlite3.connect(old_db_path)
    old_cur = old_conn.cursor()

    old_cur.execute('SELECT * FROM video;')
    old_video_data = old_cur.fetchall()
    for x in old_video_data:
        name = x[1]
        link = x[2]
        type_id = [3]
        new_cur.execute('SELECT * FROM video WHERE name=(?) AND link=(?)', (name, link))
        new_video_data = new_cur.fetchall()[0]
        print(new_video_data == x)
        #print(x)

    old_cur.execute('SELECT * FROM video_type;')
    old_video_data = old_cur.fetchall()
    for x in old_video_data:
        print(x)
    new_cur.execute('SELECT * FROM video_type;')
    new_video_data = new_cur.fetchall()
    print('----')
    for x in new_video_data:
        print(x)

    print('----')
    old_cur.execute('SELECT * FROM measurement WHERE video_id IS NOT NULL;')
    old_measurement_data = old_cur.fetchall()  # Measurements
    for x in old_measurement_data[100:]:
        video_id = x[6]  # measurement.video_id
        # Got to make sure that the video_id on the old measurement point to the right video in the new database.
        # We do that be getting the video in the old db and finding that video in the new db and use that video_id
        old_cur.execute('SELECT ROWID, name, link FROM video WHERE video.ROWID = (?)', (video_id,))
        old_video = old_cur.fetchall()[0]
        old_video_name = old_video[1]
        old_video_link = old_video[2]

        new_cur.execute('SELECT ROWID, name, link FROM video WHERE name = (?) AND link = (?)', (old_video_name, old_video_link))
        new_video = new_cur.fetchall()[0]
        new_video_id = new_video[0]
        new_video_name = new_video[1]
        new_video_link = new_video[2]

        if new_video_name == old_video_name and new_video_link == old_video_link:
            print(x)
            meas_time = x[1]
            meas_views = x[2]
            meas_likes = x[3]
            meas_dislikes = x[4]
            meas_comments = x[5]
            print('time:', meas_time)
            print('views', meas_views)
            print('likes', meas_likes)
            print('dislikes', meas_dislikes)
            print('comments',  meas_comments)
            new_cur.execute('INSERT INTO measurement (measurement_time, views, likes, dislikes, comment_count, video_id)'
                        ' VALUES (?, ?, ?, ?, ?, ?)',
                        (meas_time, meas_views,
                         meas_likes, meas_dislikes,
                         meas_comments, new_video_id))
        else:
            print('Something is wrong!!!!!!!')

        #new_cur.execute('SELECT ROWID, name, link FROM video where video.ROWID = (?)', (video_id,))
        #new_video = new_cur.fetchall()[0]
        #print('new_video: ', new_video)
        print('--')
        # print(x)

    old_cur.close()
    old_conn.close()

    new_conn.commit()
    new_cur.close()
    new_conn.close()

    """cur.execute('SELECT COUNT(1) FROM video_type WHERE description = (?)', (data['description'],))
    type_exists = cur.fetchall()[0][0]

    if not type_exists:
        cur.execute('INSERT INTO video_type (description) VALUES (?)', (data['description'],))

    # video_type = cur.lastrowid

    cur.execute('SELECT rowid FROM video_type WHERE description = (?)', (data['description'],))
    video_type = cur.fetchall()[0][0]

    for video_data in data['videos']:
        cur.execute('SELECT COUNT(1) FROM video WHERE link = (?)', (video_data,))
        video_exists = cur.fetchall()[0][0]

        if not video_exists:
            cur.execute('INSERT INTO video (name, link, type_id) VALUES (?, ?, ?)',
                        (data['videos'][video_data]['name'], video_data, video_type))

        # video_id = cur.lastrowid
        cur.execute('SELECT rowid FROM video WHERE link = (?)', (video_data,))
        video_id = cur.fetchall()[0][0]

        cur.execute('INSERT INTO measurement (measurement_time, views, likes, dislikes, comment_count, video_id)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (data['timestamp'], data['videos'][video_data]['views'],
                     data['videos'][video_data]['likes'], data['videos'][video_data]['dislikes'],
                     data['videos'][video_data]['comments'], video_id))
"""


if __name__ == '__main__':
    join_old_and_new_db()
