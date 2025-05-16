import json
from pathlib import Path

import src.db_connect as db
from src.youtube_connector import YoutubeConnect


def run_cron():
    """
    This function gets all the video links from the 'videos.json' file, then it uses the YouTubeConnect class
    to retrieve the data for each video and finally stores that data in the database.

    This is the Python function that should be executed by the 'run_cron.sh' script in the 'scripts' directory.
    The idea is to have CRON run 'run_cron.sh', which then runs this code, which then stores the video data
    in the database.
    This code should not be run directly, but always executed through 'run_cron.sh', unless you are testing something.
    :return: Nothing
    """
    # TODO change all of these prints out for proper logging.
    print('starting process')
    path_to_json = Path(__file__).resolve().parent / 'data' / 'videos.json'
    with open(path_to_json) as f:
        print('opening Json File')
        data = json.load(f)

    conf_location = Path(__file__).resolve().parent.parent.parent / 'eurovision_data' / 'config' / 'cron.ini'
    youtube = YoutubeConnect(config_location=conf_location)
    for video_groups in data['video_group']:
        link_list = [video_info['link'] for video_info in video_groups['videos']
                     if video_groups['type'] == 'Euro semi finals 1 2025'
                     or video_groups['type'] == 'Euro semi finals 2 2025']
        if link_list:
            video_dict = youtube.get_video_data_for_video_list(link_list, video_groups['type'])
            db.store_data(video_dict)
            print(f'data storage successful for type={video_groups["type"]}')

    print('ending process')
    return


# This tells the script to run the main function.
if __name__ == "__main__":
    run_cron()
