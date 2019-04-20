from django.urls import path
from . import views


app_name = 'video_data'
urlpatterns = [
    path('', views.index, name='index'),
    path('plot/', views.display_plot, name='plot-data'),
]