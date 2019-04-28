import sqlite3
import plotly as py
import plotly.graph_objs as go


def recreate_database():
    conn = sqlite3.connect('database\youtube_info.sqlite')
    cur = conn.cursor()

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
    conn = sqlite3.connect('database\youtube_info.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT COUNT(1) FROM video_type WHERE description = (?)', (data['description'],))
    type_exists = cur.fetchall()[0][0]

    if not type_exists:
        cur.execute(('INSERT INTO video_type (description) VALUES (?)'), (data['description'],))

    #video_type = cur.lastrowid

    cur.execute('SELECT rowid FROM video_type WHERE description = (?)', (data['description'],))
    video_type = cur.fetchall()[0][0]
    #print('ttest', test)

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
    conn = sqlite3.connect('database\youtube_info.sqlite')
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
    videos = set(x[2] for x in data_from_db)
    value_dict = {x: {'views': [], 'time': [], 'type': []} for x in videos}

    for x in range(len(data_from_db) - 1):
        data_line = data_from_db[x]
        current_video_name = data_line[2]
        value_dict[current_video_name]['views'].append(data_line[0])
        value_dict[current_video_name]['time'].append(data_line[1])
        value_dict[current_video_name]['type'].append(data_line[3])

    #print(value_dict)

    tracer_list = []
    for key, value in value_dict.items():
        tracer = go.Scatter(x=value['time'], y=value['views'], text=value['type'], mode='lines+markers', name=key)
        tracer_list.append(tracer)
    fig = go.Figure(data=tracer_list)
    py.offline.plot(fig, filename='test-plot.html', auto_open=False)
    cur.close()
    conn.close()


def plot_raw(line_nr, device_id=None):
    with connection.cursor() as cur:
        cur.execute("SELECT device.mac_address, measurement.rssi, device.host_name, measurement.measurement_time, measurement.wireless_type "
                    "FROM device "
                    "JOIN measurement ON device.device_id = measurement.device_id "
                    "JOIN router ON device.router_id = router.router_id "
                    "WHERE router.line_nr = (%s) "
                    "AND measurement.measurement_time >= '2016-10-23' "
                    #"AND measurement.measurement_time < '2016-10-31' "
                    "ORDER BY device.mac_address ASC, measurement.measurement_time ASC;", (line_nr,))
        dataFromDB = cur.fetchall()
    MACAddresses = set(x[0] for x in dataFromDB)
    rssiDict = {x: {'rssi': [], 'time': [], 'name': [], 'type': []} for x in MACAddresses}

    """for i in range(len(dataFromDB) - 1):
        prev_data = next_data = 0
        dataLine = dataFromDB[i]
        if i != 0:
            prev_data = dataFromDB[i - 1][1]
        if i != len(dataFromDB):
            next_data = dataFromDB[i + 1][1]
        curr_mac = dataLine[0]
        if dataLine[1] != 0 or prev_data != 0 or next_data != 0:
            if dataLine[1] == 0:
                rssiDict[curr_mac]['rssi'].append(None)
            else:
                rssiDict[curr_mac]['rssi'].append(dataLine[1])
            rssiDict[curr_mac]['name'].append(dataLine[2])
            rssiDict[curr_mac]['time'].append(dataLine[3])
            rssiDict[curr_mac]['type'].append(dataLine[4])

    device_list = []
    for key, value in rssiDict.items():
        for rssi in value['rssi']:
            if rssi is not None:
                if rssi < 0:
                    device_list.append(key)
                    break
    """
    tracer_list = []

    # If the plot is supposed to plot only a single device.
    if device_id:
        with connection.cursor() as cur:
            cur.execute("SELECT device.mac_address "
                        "FROM device "
                        "WHERE device.device_id = (%s);", (device_id,))
            queried_device_mac = cur.fetchone()[0]

        traced_device = rssiDict[queried_device_mac]
        if traced_device['rssi']:
            tracer = go.Bar(x=traced_device['time'], y=traced_device['rssi'], text=traced_device['type'], name=traced_device['name'][0])
            tracer_list.append(tracer)

    # If the plot is supposed to plot every device associated with the router.
    else:
        for key, value in rssiDict.items():
            if value['rssi'] and key in device_list:
                tracer = go.Scatter(x=value['time'], y=value['rssi'], mode='lines', text=value['type'], name=value['name'][0], connectgaps=False)
                tracer_list.append(tracer)

    layout = go.Layout(yaxis = dict(range = [0, -90]))

    if tracer_list:
        fig = go.Figure(layout = layout, data = tracer_list)
        return (device_list, py.offline.plot(fig, include_plotlyjs=False, output_type='div'))