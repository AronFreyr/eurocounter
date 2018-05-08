from django.test import TestCase

import json
from pprint import pprint
import os

from .eurovision_youtube_counter.src import db_connection_test as db


class JsonTests(TestCase):

    def test_open_json_file(self):
        file_path = os.path.join(os.path.abspath(''), r'video_data/eurovision_youtube_counter/videos.json')

        with open(file_path) as f:
            data = json.load(f)
        pprint(data)

    def test_read_json_file(self):
        file_path = os.path.join(os.path.abspath(''), r'video_data/eurovision_youtube_counter/videos.json')

        with open(file_path) as f:
            data = json.load(f)

        print(data['video_group'][0]['videos'][0]['link'])

        for x in data['video_group']:
            print(x['type'])


class DatabaseTests(TestCase):

    def test_read_from_db(self):
        print(db.read_data())
