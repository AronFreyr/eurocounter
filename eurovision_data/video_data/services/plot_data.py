import plotly as py
import plotly.graph_objs as go

import datetime


def create_graph(data_from_db, y_value='views', year=None):

    if not data_from_db:
        return 'No data was found.'

    # TODO: Final dates should be stored somewhere better, maybe in a database, maybe JSON.
    finals_dates = {'2017': datetime.datetime(day=13, month=5, year=2017, hour=19),
                    '2018': datetime.datetime(day=12, month=5, year=2018, hour=19),
                    '2019': datetime.datetime(day=18, month=5, year=2019, hour=19)}

    value_dict = {x.get_clean_name(): {'views': [], 'likes': [],
                                       'dislikes': [], 'comment_count': [],
                                       'time': [], 'type': []} for x in data_from_db}  # create empty dictionary for videos

    # data_from_db = data_from_db[::2]

    while len(data_from_db) > 10000:  # limiting the points displayed on the graph to improve performance.
        data_from_db = data_from_db[::2]

    for x in data_from_db:  # Create dictionary with lists for each value so the plot function understands it.
        name = x.get_clean_name()
        value_dict[name]['views'].append(x.get_views())
        value_dict[name]['time'].append(x.get_time())
        value_dict[name]['type'].append(x.get_description())
        value_dict[name]['likes'].append(x.get_likes())
        value_dict[name]['dislikes'].append(x.get_dislikes())
        #value_dict[name]['comment_count'].append(x.get_likes() / x.get_dislikes())
        value_dict[name]['comment_count'].append(x.get_comments())

    config = {'scrollZoom': True, 'displayModeBar': True, 'showLink': False,
              'modeBarButtonsToRemove': ['sendDataToCloud',  # Don't need that
                                         'lasso2d',  # Never got it to work
                                         'select2d',  # Don't know how it works
                                         'toggleSpikelines',  # Have no idea what it's supposed to do
                                         'zoom2d'  # There are much better ways to zoom
                                         ]
              }

    tracer_list = []

    if year:
        annotations = [
            # Dictionary for the arrow indicating the Eurovision Finals date.
            dict(
                x=finals_dates[year], y=0, arrowcolor="#000000",
                arrowhead=1, arrowsize=1, arrowwidth=1,
                ax=0, ay=-300, bgcolor="rgba(0,0,0,0)",
                bordercolor="#000000", borderpad=1, borderwidth=1,
                font=dict(color="#0000ff", family="Courier New", size=10),
                opacity=1, showarrow=True, text="Eurovision Finals",
                xref="x", yref="y"
            )]
    else:
        annotations = []

    layout = _define_graph_layout(year, y_value)

    layout['annotations'] = annotations
    layout['hovermode'] = 'closest'
    layout['legend'] = dict(bgcolor='#f8f8f8', bordercolor='#f4f4f4', borderwidth=2)

    for key, value in sorted(value_dict.items()):
        tracer = go.Scatter(x=value['time'], y=value[y_value], text=value['type'], mode='lines+markers', name=key)
        tracer_list.append(tracer)
    fig = go.Figure(data=tracer_list, layout=layout)
    #py.offline.plot(fig, filename=r'../plots/test-plot.html', auto_open=False)
    return py.offline.plot(fig, include_plotlyjs=True, output_type='div', config=config)


def _define_graph_layout(year, y_value):
    """
    Function for preparing the layout that Plotly needs when creating the graph. Here things like "Title",
     "X-Axis title" and "Y-Axis title" are defined.
    :param year: The year for the data on the graph, need it to be displayed in the graph title.
    :param y_value: The value that is displayed on the Y-axis, need it displayed on the graph.
    :return: The layout object.
    """

    layout = go.Layout(
        # Title text
        title=go.layout.Title(
            text='Eurovision ' + year, xref='paper', yref='paper',
            font=dict(family='Arial', size=30, color='rgb(37,37,37)')
        ),
        # X-axis text
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Time',
                font=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
            )
        ),
        # Y-axis text
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=y_value,
                font=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
            )
        )
    )
    return layout


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

