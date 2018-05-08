import json

#import eurovision_youtube_counter.db_connection_test as db
import eurovision_data.video_data.eurovision_youtube_counter.src.db_connection_test as db
import eurovision_data.video_data.eurovision_youtube_counter.src.youtube_view_count_v0_2 as eurocount


def run_cron():

    with open('videos.json') as f:
        data = json.load(f)
        
    for video_groups in data['video_group']:
        link_list = [x['link'] for x in video_groups['videos']]
        video_dict = eurocount.create_video_dict(video_groups['type'], link_list)
        print(video_dict)


    #db.recreate_database()
    #video_dict = eurocount.create_video_dict(list_type, video_links_list)
    #db.store_data(video_dict)
    #data_from_db = db.read_data()
    #print(data_from_db)
    #print(plot_data.create_graph(data_from_db))
    #print(eurocount.get_video_list(video_links_list))


# This tells the script to run the main function.
if __name__ == "__main__":
    run_cron()
