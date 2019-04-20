from .eurovision_youtube_counter.src import plot_data as plot_data, db_connection_test as db
from .eurovision_youtube_counter.src.data_handling import EuroData

from django.shortcuts import render


def index(request):
    #test_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir, 'eurovision_youtube_counter/plots'))
    return render(request, 'video_data/index.html')


def display_plot(request):

    data_from_db = db.read_data()

    data_object_list = []

    for x in range(len(data_from_db) - 1):
        data_line = data_from_db[x]
        name = data_line[2]
        views = data_line[0]
        time = data_line[1]
        video_type = data_line[3]

        # Create Eurovision data objects and append them to a list.
        data_object_list.append(EuroData(name=name, views=views, likes='', time=time, video_type=video_type))

    plot_as_div = plot_data.create_graph(data_from_db)
    return render(request, 'video_data/plot.html', {'plot': plot_as_div})
