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
    y_axis_possibilities = ['views', 'likes', 'dislikes', 'comment_count']

    if year == '2018':
        video_desc_list = ['Euro semi finals 1 2018', 'Euro semi finals 2 2018']
    elif year == '2017':
        video_desc_list = ['Euro semi finals 1 2017', 'Euro semi finals 2 2017']
    elif year == '2019':
        video_desc_list = ['Euro semi finals 1 2019', 'Euro semi finals 2 2019']
    else:
        raise ValueError
    euro_object_list = []
    data_from_db = db.read_data_with_video_type(video_desc_list, year)

    for x in data_from_db:
        euro_object_list.append(EuroData(views=x[0], time=x[1], name=x[2], description=x[3],
                                         likes=x[4], dislikes=x[5], comments=x[6]))

    # if request.method == 'GET':
    y_axis = 'views'

    if request.method == 'POST':
        if 'y_axis_choices' in request.POST:
            y_axis = request.POST['y_axis_choices']

    plot_as_div = plot_data.create_graph(euro_object_list, y_axis)
    #plot_as_div = plot_data.create_graph(data_from_db)
    return render(request, 'video_data/plot.html', {'plot': plot_as_div,
                                                    'year': year,
                                                    'y_axis_possibilities': y_axis_possibilities})
