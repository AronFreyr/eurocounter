from .eurovision_youtube_counter.src import plot_data as plot_data, db_connect as db
from .eurovision_youtube_counter.src.data_handling import EuroData

from django.shortcuts import render


def index(request):
    return render(request, 'video_data/index.html')


def display_plot(request):

    data_from_db = db.read_data()
    plot_as_div = plot_data.create_graph(data_from_db)
    return render(request, 'video_data/plot.html', {'plot': plot_as_div})


def display_plot_year(request, year):

    if year not in ['2017', '2018', '2019']:
        raise ValueError
    y_axis_possibilities = ['views', 'likes', 'dislikes', 'comment_count']
    line_possibilities = ['Semi-finals 1', 'Semi-finals 2', 'Both semi-finals']
    video_desc_list = ['Euro semi finals 1 ' + year, 'Euro semi finals 2 ' + year]

    # if request.method == 'GET':
    y_axis = 'views'
    line_choice = 'Both semi-finals'

    if request.method == 'POST':
        if 'y_axis_choices' in request.POST:
            y_axis = request.POST['y_axis_choices']
        if 'line_choices' in request.POST:
            line_choice = request.POST['line_choices']
            if line_choice == 'Semi-finals 1':
                video_desc_list = ['Euro semi finals 1 ' + year]
            elif line_choice == 'Semi-finals 2':
                video_desc_list = ['Euro semi finals 2 ' + year]
            elif line_choice == 'Both semi-finals':
                video_desc_list = ['Euro semi finals 1 ' + year, 'Euro semi finals 2 ' + year]
            else:
                raise ValueError

    euro_object_list = []
    data_from_db = db.read_data_with_video_type(video_desc_list, year)

    for x in data_from_db:
        euro_object_list.append(EuroData(views=x[0], time=x[1], name=x[2], description=x[3],
                                         likes=x[4], dislikes=x[5], comments=x[6]))


    plot_as_div = plot_data.create_graph(euro_object_list, y_axis, year)
    #plot_as_div = plot_data.create_graph(data_from_db)
    return render(request, 'video_data/plot.html', {'plot': plot_as_div,
                                                    'year': year,
                                                    'y_axis_possibilities': y_axis_possibilities,
                                                    'y_axis_choice': y_axis,
                                                    'line_choices': line_possibilities,
                                                    'line_choice': line_choice})
