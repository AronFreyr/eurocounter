import plotly as py
import plotly.graph_objs as go

import video_json_connect


def create_graph(data_from_db):

    value_dict = {x.get_name(): {'views': [], 'time': [], 'type': []} for x in data_from_db}  # create empty dictionary for videos

    video_json_connect.get_video_urls()

    for x in data_from_db:  # Create dictionary with lists for each value so the plot function understands it.
        name = x.get_name()
        value_dict[name]['views'].append(x.get_views())
        value_dict[name]['time'].append(x.get_time())
        value_dict[name]['type'].append(x.get_description())

    tracer_list = []
    for key, value in value_dict.items():
        tracer = go.Scatter(x=value['time'], y=value['views'], text=value['type'], mode='lines+markers', name=key)
        tracer_list.append(tracer)
    fig = go.Figure(data=tracer_list)
    #py.offline.plot(fig, filename=r'../plots/test-plot.html', auto_open=False)
    return py.offline.plot(fig, include_plotlyjs=True, output_type='div')


@DeprecationWarning
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

