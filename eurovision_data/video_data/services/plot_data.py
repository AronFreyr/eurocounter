import plotly as py
import plotly.graph_objs as go
import datetime
import json

from django.conf import settings


def create_graph(data_from_db, y_value='views', year=None, mode='Normal graph'):

    if not data_from_db:
        return 'No data was found.'

    grand_finals_dates = _get_eurovision_finals_dates('eurovision_grand_final_dates')
    semi_finals_1_dates = _get_eurovision_finals_dates('eurovision_first_semi_final_dates')
    semi_finals_2_dates = _get_eurovision_finals_dates('eurovision_second_semi_final_dates')

    # create empty dictionary for videos
    value_dict = {x.get_clean_name(): {'views': [], 'likes': [], 'comment_count': [], 'country': [],
                                       'time': [], 'type': [], 'Likes per view (%)': []} for x in data_from_db}

    while len(data_from_db) > 10000:  # limiting the points displayed on the graph to improve performance.
        data_from_db = data_from_db[::2]

    for x in data_from_db:  # Create dictionary with lists for each value so the plot function understands it.
        name = x.get_clean_name()
        value_dict[name]['views'].append(x.get_views())
        if mode == 'Concurrent graph':
            time = x.get_time().split('.')[0][:-3]
            if time.split(':')[-1] == '30' or time.split(':')[-1] == '00':
                time_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
                if 'semi finals 1' in x.get_description():
                    time_delta = time_obj - semi_finals_1_dates[year]
                else:
                    time_delta = time_obj - semi_finals_2_dates[year]

                minutes = str((time_delta.seconds//60) % 60)
                if len(minutes) == 1:
                    minutes = '0' + minutes
                time_delta = str((time_delta.seconds // 3600) + (
                            time_delta.days * 24)) + ":" + minutes + ":00"
                # Adding an extra zeros to the time to make it be alphabetical.
                while time_delta[1] == ':' or time_delta[2] == ':':
                    time_delta = '0' + time_delta
                value_dict[name]['time'].append(time_delta)
        else:
            value_dict[name]['time'].append(x.get_time())

        value_dict[name]['type'].append(x.get_description())
        value_dict[name]['likes'].append(x.get_likes())
        value_dict[name]['comment_count'].append(x.get_comments())
        value_dict[name]['Likes per view (%)'].append(x.get_like_percentage())
        value_dict[name]['country'].append(x.get_clean_name().split(' - ')[0])

    config = {'scrollZoom': True, 'displayModeBar': True, 'showLink': False,
              'modeBarButtonsToRemove': ['sendDataToCloud',  # Don't need that
                                         'lasso2d',  # Never got it to work
                                         'select2d',  # Don't know how it works
                                         'toggleSpikelines',  # Have no idea what it's supposed to do
                                         'zoom2d'  # There are much better ways to zoom
                                         ]
              }

    tracer_list = []

    if year is not None and mode == 'Normal graph':
        annotations = [
            # Dictionary for the arrow indicating the Eurovision Finals date.
            dict(
                x=grand_finals_dates[year], y=0, arrowcolor="#000000",
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

    # Sort the dict to be the latest value of 'y_value', go from highest to lowest.
    for key, value in sorted(value_dict.items(), key=lambda x: x[1][y_value][-1], reverse=True):
        tracer = go.Scatter(x=value['time'], y=value[y_value], text=value['country'], mode='lines+markers', name=key,
                            hoverlabel={'namelength': 0})
        tracer_list.append(tracer)
    fig = go.Figure(data=tracer_list, layout=layout)
    fig.update_xaxes(categoryorder='category ascending')
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


def _get_eurovision_finals_dates(finals):
    """ Gets the date of every Eurovision final from the JSON and returns it as a dict. """
    with open(settings.JSON_LOCATION) as f:
        json_data = json.load(f)
    finals_data = json_data[finals]
    finals_dates = {}
    for key, value in finals_data.items():
        if value != 'None':
            finals_dates[key] = datetime.datetime.strptime(value + ' 19', '%Y-%m-%d %H')
        else:
            finals_dates[key] = value
    return finals_dates
