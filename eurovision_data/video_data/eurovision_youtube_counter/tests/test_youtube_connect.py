#from django.test import TestCase
import unittest
import os

from ..src.youtube_connector import YoutubeConnect


class YoutubeTests(unittest.TestCase):

    def setUp(self):
        current_location = os.path.realpath(os.path.dirname(__file__))
        self.config_location = os.path.join(current_location, '../../../eurovision_data/config/dev.ini')

    def test_youtube_class_connection_for_single_video(self):
        youtube = YoutubeConnect(config_location=self.config_location)
        youtube_video_id = 'clltO-wwfRE'
        results = youtube.get_single_video_data(youtube_video_id)
        print(results)

    def test_youtube_class_connection_for_video_list(self):
        video_list = ['https://www.youtube.com/watch?v=clltO-wwfRE',
                      'https://www.youtube.com/watch?v=mX8LYc5eaEM',
                      'https://www.youtube.com/watch?v=c-VoiE7R9lc']
        youtube = YoutubeConnect(config_location=self.config_location)
        results = youtube.get_video_data_for_video_list(video_list)
        print(results)
