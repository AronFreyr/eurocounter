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

    conf_location = os.path.join(os.path.realpath(os.path.dirname(__file__)), r'../../eurovision_data/config/cron.ini')
    youtube = YoutubeConnect(config_location=conf_location)
    for video_groups in data['video_group']:
        link_list = [video_info['link'] for video_info in video_groups['videos']
                     if video_groups['type'] == 'Euro semi finals 1 2022'
                     or video_groups['type'] == 'Euro semi finals 2 2022']
        if link_list:
            video_dict = youtube.get_video_data_for_video_list(link_list, video_groups['type'])
            db.store_data(video_dict)
            print('data storage successful for type=' + video_groups["type"])

    print('ending process')
    return


# This tells the script to run the main function.
if __name__ == "__main__":
    run_cron()
