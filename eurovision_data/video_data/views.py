from django.shortcuts import render

from .eurovision_youtube_counter.src import db_connect as db
from .services import plot_data
from .services.data_handling import EuroData
from django.shortcuts import render
from django.conf import settings
import json
from django.template import RequestContext


def handler404(request, exception):
    context = {}
    response = render(request, "video_data/error.html", context=context)
    response.status_code = 404
    return response


def index(request):
    """ Simple index that displays the homepage. Currently only displays some text. """
    return render(request, 'video_data/index.html')


def display_plot(request):

    data_from_db = db.read_data()
    plot_as_div = plot_data.create_graph(data_from_db)
    return render(request, 'video_data/plot.html', {'plot': plot_as_div})


def covid_year(request):
    return render(request, 'video_data/2020.html')


def display_plot_year(request, year):

    if year not in ['2017', '2018', '2019', '2021', '2022']:
        return render(request, 'video_data/error.html')
        # TODO: more specific error and error description. Also catch the error and display an error page.
        raise ValueError
    y_axis_possibilities = ['views', 'likes', 'dislikes', 'comment_count', 'likes vs dislikes', 'Likes per view (%)']
    line_possibilities = ['Semi-finals 1', 'Semi-finals 2', 'Both semi-finals']
    video_desc_list = ['Euro semi finals 1 ' + year, 'Euro semi finals 2 ' + year]
    graph_choices = ['Normal graph', 'Concurrent graph']

    y_axis = 'views'
    line_choice = 'Both semi-finals'
    graph_choice = 'Normal graph'

    if request.method == 'GET':
        if 'y_axis_choices' in request.GET:
            y_axis = request.GET['y_axis_choices']
        if 'line_choices' in request.GET:
            line_choice = request.GET['line_choices']
            if line_choice == 'Semi-finals 1':
                video_desc_list = ['Euro semi finals 1 ' + year]
            elif line_choice == 'Semi-finals 2':
                video_desc_list = ['Euro semi finals 2 ' + year]
            elif line_choice == 'Both semi-finals':
                video_desc_list = ['Euro semi finals 1 ' + year, 'Euro semi finals 2 ' + year]
            else:
                raise ValueError
        if 'graph_choices' in request.GET:
            graph_choice = request.GET['graph_choices']

    country_list = []
    with open(settings.JSON_CONTEST_RESULTS_LOCATION, encoding='utf8') as f:
        json_data = json.load(f)
    for period in json_data['eurovision_final_results']:
        if year == period['year']:
            country_list = period['countries']
    #countries = json_data['eurovision_final_results']

    euro_object_list = []
    data_from_db = db.read_data_with_video_type(video_desc_list, year)

    for x in data_from_db:
        euro_object_list.append(EuroData(views=x[0], time=x[1], name=x[2], description=x[3],
                                         likes=x[4], comments=x[5]))

    plot_as_div = plot_data.create_graph(euro_object_list, y_axis, year, graph_choice)
    return render(request, 'video_data/plot.html', {'plot': plot_as_div,
                                                    'year': year,
                                                    'y_axis_possibilities': y_axis_possibilities,
                                                    'y_axis_choice': y_axis,
                                                    'line_choices': line_possibilities,
                                                    'line_choice': line_choice,
                                                    'graph_choices': graph_choices,
                                                    'graph_choice': graph_choice,
                                                    'country_list': country_list})
