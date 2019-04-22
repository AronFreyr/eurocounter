import json
import os


def get_video_urls(description_input=None):
    json_file = os.path.join(os.path.abspath(''), r'video_data/eurovision_youtube_counter/videos.json')
    with open(json_file) as f:
        data = json.load(f)

    print(data['video_group'])
