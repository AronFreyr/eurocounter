from django.urls import path
from . import views


app_name = 'video_data'
urlpatterns = [
    path('', views.index, name='index'),
    path('plot/', views.display_plot, name='plot-data'),
    path('plot/<str:year>/', views.display_plot_year, name='plot-data-year'),
    path('covid/', views.covid_year, name='covid-year')
]
