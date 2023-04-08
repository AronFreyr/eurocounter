import unittest
from pathlib import Path

from ..src.youtube_connector import YoutubeConnect


class YoutubeTests(unittest.TestCase):

    def setUp(self):
        current_location = Path(__file__).resolve().parent
        self.config_location = current_location.parent.parent.parent / 'eurovision_data' / 'config' / 'dev.ini'

    def test_youtube_class_connection_for_single_video(self):
        youtube = YoutubeConnect(config_location=self.config_location)
        youtube_video_id = 'clltO-wwfRE'
        results = youtube.get_single_video_data(youtube_video_id)
        print(results)
        self.assertEqual(results['videos'][youtube_video_id]['name'],
                         'Nathan Trent - Running On Air (Austria) LIVE at the second Semi-Final')

    def test_youtube_class_connection_for_video_list(self):
        video_list = ['https://www.youtube.com/watch?v=clltO-wwfRE',
                      'https://www.youtube.com/watch?v=mX8LYc5eaEM',
                      'https://www.youtube.com/watch?v=c-VoiE7R9lc']
        youtube = YoutubeConnect(config_location=self.config_location)
        results = youtube.get_video_data_for_video_list(video_list)
        print(results)
        self.assertEqual(results['videos'][video_list[0]]['name'],
                         'Nathan Trent - Running On Air (Austria) LIVE at the second Semi-Final')
        self.assertEqual(results['videos'][video_list[1]]['name'],
                         'Ilinca ft. Alex Florea - Yodel It! (Romania) LIVE at the second Semi-Final')
        self.assertEqual(results['videos'][video_list[2]]['name'],
                         'OG3NE - Lights and Shadows (The Netherlands) LIVE at the second Semi-Final')
