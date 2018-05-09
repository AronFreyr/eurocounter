import json
import os

#import eurovision_youtube_counter.db_connection_test as db
#import eurovision_data.video_data.eurovision_youtube_counter.src.db_connection_test as db
import src.db_connection_test as db
#import eurovision_data.video_data.eurovision_youtube_counter.src.youtube_view_count_v0_2 as eurocount
import src.youtube_view_count_v0_2 as eurocount


def run_cron():
    print('starting process')
    path_to_json = os.path.join(os.path.realpath(os.path.dirname(__file__)), r'videos.json')
    print(path_to_json)
    with open(path_to_json) as f:
        print('opening Json File')
        data = json.load(f)
        f.close()
        
    for video_groups in data['video_group']:
        link_list = [x['link'] for x in video_groups['videos']]
        video_dict = eurocount.create_video_dict(video_groups['type'], link_list)
        db.store_data(video_dict)
        print('data storage successful')
        #print(video_dict)

    print('ending process')
    return
    #db.recreate_database()
    #video_dict = eurocount.create_video_dict(list_type, video_links_list)
    #db.store_data(video_dict)
    #data_from_db = db.read_data()
    #print(data_from_db)
    #db.recreate_database(True)
    #print(plot_data.create_graph(data_from_db))
    #print(eurocount.get_video_list(video_links_list))


# This tells the script to run the main function.
if __name__ == "__main__":
    run_cron()
