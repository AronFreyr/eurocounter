import json
import os

import src.db_connect as db
from src.youtube_connector import YoutubeConnect


def run_cron():
    print('starting process')
    path_to_json = os.path.join(os.path.realpath(os.path.dirname(__file__)), r'videos.json')
    with open(path_to_json) as f:
        print('opening Json File')
        data = json.load(f)
        f.close()

    youtube = YoutubeConnect(config_location='../../eurovision_data/config/cron.ini')
    for video_groups in data['video_group']:
        link_list = [video_info['link'] for video_info in video_groups['videos']
                     if video_groups['type'] == 'Euro semi finals 1 2019'
                     or video_groups['type'] == 'Euro semi finals 2 2019']
        video_dict = youtube.get_video_data_for_video_list(link_list, video_groups['type'])
        db.store_data(video_dict)
        print('data storage successful')

    print('ending process')
    return


# This tells the script to run the main function.
if __name__ == "__main__":
    run_cron()
