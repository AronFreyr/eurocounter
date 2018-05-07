import os
from eurovision_youtube_counter import db_connection_test as db
from eurovision_youtube_counter import plot_data as plot_data

from django.shortcuts import render


def index(request):
    #test_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir, 'eurovision_youtube_counter/plots'))
    data_from_db = db.read_data()
    plot_as_div = plot_data.create_graph(data_from_db)
    return render(request, 'video_data/index.html', {'plot': plot_as_div})
