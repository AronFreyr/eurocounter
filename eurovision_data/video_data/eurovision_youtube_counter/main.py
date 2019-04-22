import json

#import eurovision_youtube_counter.db_connection_test as db
#import eurovision_data.video_data.eurovision_youtube_counter.src.db_connection_test as db
#import eurovision_data.video_data.eurovision_youtube_counter.src.youtube_view_count_v0_2 as eurocount
import src.db_connect as db
import src.youtube_view_count_v0_2 as eurocount
import src.plot_data as plot_data


def main():
    # Semi final 1
    #video_links_list = [
    #    'https://www.youtube.com/watch?v=nH6X2DVP8V4',
    #    'https://www.youtube.com/watch?v=058Yyhxsi7o',
    #    'https://www.youtube.com/watch?v=SznlioGhq2k',
    #    'https://www.youtube.com/watch?v=wY1fN0R5vXY',
    #    'https://www.youtube.com/watch?v=0td62XxnjBk',
    #    'https://www.youtube.com/watch?v=nVrlEB1bN3w',
    #    'https://www.youtube.com/watch?v=c3S3g0MKx08',
    #    'https://www.youtube.com/watch?v=prqZ8MSAPh4',
    #    'https://www.youtube.com/watch?v=B94IsBm4Y0Q',
    #    'https://www.youtube.com/watch?v=yKh8sLLXix4'
    #]

    #list_type = 'Euro semi finals 1'

    #with open('videos.json') as f:
    #    data = json.load(f)
    #for video_groups in data['video_group']:
    #    link_list = [x['link'] for x in video_groups['videos']]
    #    video_dict = eurocount.create_video_dict(video_groups['type'], link_list)
    #    print(video_dict)
    



    #db.recreate_database()
    #video_dict = eurocount.create_video_dict(list_type, video_links_list)
    #db.store_data(video_dict)
    data_from_db = db.read_data()
    plot_data.create_graph(data_from_db)
    #print(data_from_db)
    #print(plot_data.create_graph(data_from_db))
    #print(eurocount.get_video_list(video_links_list))


# This tells the script to run the main function.
if __name__ == "__main__":
    main()
