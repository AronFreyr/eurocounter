#! python3
# -*- coding: utf-8 -*-

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import datetime
import db_connect


# This function is a little misleading, it's input is only a single video_id and it returns data on a single video,
# not a list of videos.
def videos_list_by_id(part, video_id):
    """
    A function for calling the Youtube API and receiving data about a given video.
    :param part: Which parts of the video data we want to get from the API.
    :param video_id: The ID of the video that we are querying the API for.
    :return: The results from the API query. This is all of the information about the video with the video ID of 
    'video_id'. Must of this info is useless, but some of it, like name and view-count, needs to be extracted
    from it elsewhere.
    """

    # TODO: Change this function so we don't establish a new connection to the Youtube API every time we query a
    # TODO: video. We should only do it once and use the same connection every time.

    # Youtube API -----------------------------------------------------
    developer_key = "AIzaSyAtKot3NSpIBTbUHziloc9TddNdo9qNzRU"  # My youtube developer key.
    api_service_name = "youtube"  # The name of the API that's being called.
    api_version = "v3"  # The version of the API that't being used.
    # Youtube API -----------------------------------------------------

    service = build(api_service_name, api_version, developerKey=developer_key)  # The connection to the API.

    # This executes a search through Youtube, using the API connection 'service', and returns the relevant information
    # 'parts' about a video that has id 'video_id'.
    results = service.videos().list(
        id=video_id,
        part=part
    ).execute()
    return results


def get_video_list(video_links_list):
    """
    Creates the list of videos. A list of videos is simply a list of tuples. Tuples are objects that come in pairs,
    here the pair is 'video name' and 'video view-count'.
    :param video_links_list: A list of youtube links.
    :return: A list of tuples with name and view-count, sorted in descending order. This is a list of tuples and 
    each tuple has two values, the name of the video and the view-count of the video.
    """
    list_of_videos = []  # Create an initial list of videos and have it empty to begin with.
    for video in video_links_list:  # for each video URL in a list of video URL's.
        video_id = video.split('=')[1]  # split the video URL on '=' and use the latter half of the split.
        video_results = videos_list_by_id('snippet,contentDetails,statistics', video_id)  # Get info on the video.
        # Add the relevant info to the list_of_videos as a tuple.
        list_of_videos.append((video_results['items'][0]['snippet']['title'],
                               int(video_results['items'][0]['statistics']['viewCount'])))

    # This is a lambda function. it sorts the video list based on tup[1], which is the view-count,
    # and sorts it in reverse order, so the highest viewed video is first.
    list_of_videos.sort(key=lambda tup: tup[1], reverse=True)
    return list_of_videos


def create_video_dict(list_type, video_links_list):
    video_dict = {'timestamp': datetime.datetime.now(), 'description': list_type, 'videos': {}}
    for video in video_links_list:
        video_dict['videos'][video] = {}
        video_id = video.split('=')[1]  # split the video URL on '=' and use the latter half of the split.
        video_results = videos_list_by_id('snippet,contentDetails,statistics', video_id)  # Get info on the video.
        video_dict['videos'][video]['views'] = int(video_results['items'][0]['statistics']['viewCount'])
        video_dict['videos'][video]['likes'] = int(video_results['items'][0]['statistics']['likeCount'])
        video_dict['videos'][video]['dislikes'] = int(video_results['items'][0]['statistics']['dislikeCount'])
        video_dict['videos'][video]['comments'] = int(video_results['items'][0]['statistics']['commentCount'])
        video_dict['videos'][video]['name'] = video_results['items'][0]['snippet']['title']
    return video_dict


def print_video_statistics(list_of_videos, list_type):
    """
    Opens a txt file and writes the tuples (the video names and view-count) to the file, along with the video
    list type.
    :param list_of_videos: List of tuples (video name and view-count pairs) that contain the relevant info
    about the videos.
    :param list_type: The type of video list that is being written to file. e.x. 'Euro semi finals 1'.
    :return: Nothing. This function writes to the file and then stops.
    """
    if list_of_videos:  # If the list of videos is not an empty list.
        print('Attempting to open txt file')

        # Open a text file with the 'correct' encoding and in mode 'a' for 'append'.
        # If the mode were 'r', which means 'read', then you could only read from the file and not write to it.
        # If the mode were 'w', which means 'write', then you could only write to it and not read it.
        # 'a', or 'append' is better than 'w', because 'w' overwrites the contents of the txt file while 'a'
        # appends to it (adds to it).
        f = open('video views.txt', 'a', encoding='utf-8')
        # TODO: This encoding may be broken, it has trouble with many non-latin letters.
        f.write('---------------------------------------\n')  # Write to the txt file.
        f.write(str(datetime.datetime.now()) + '\n')  # Write the date and time for  RIGHT NOW, EXACTLY.
        f.write(list_type)  # Write what type of list it is.
        for video in list_of_videos:  # for each video info in a list of them (tuples)
            # Write to the file using a different encoding, it may fix the problems with the non-latin letters.
            # video[0] is the name (which needs to be encoded and converted to a string (for some reason...))
            #  and video[1] is the view count (which needs to be converted to a string because it's an integer).
            f.write(str(video[0].encode('cp1250')) + ' - ' + str(video[1]) + '\n')
        f.write('---------------------------------------\n')
        print('Closing txt file.')
        f.close()  # close the txt file safely.


def main():
    """
    The main function of the script.
    :return: NOTHING
    """

    # Semi final 1
    video_links_list = [
        'https://www.youtube.com/watch?v=nH6X2DVP8V4',
        'https://www.youtube.com/watch?v=058Yyhxsi7o',
        'https://www.youtube.com/watch?v=SznlioGhq2k',
        'https://www.youtube.com/watch?v=wY1fN0R5vXY',
        'https://www.youtube.com/watch?v=0td62XxnjBk',
        'https://www.youtube.com/watch?v=nVrlEB1bN3w',
        'https://www.youtube.com/watch?v=c3S3g0MKx08',
        'https://www.youtube.com/watch?v=prqZ8MSAPh4',
        'https://www.youtube.com/watch?v=B94IsBm4Y0Q',
        'https://www.youtube.com/watch?v=yKh8sLLXix4'
    ]

    list_type = 'Euro semi finals 1'
    video_dict = create_video_dict(list_type, video_links_list)
    db_connect.store_data(video_dict)

    video_links_list2 = [
        'https://www.youtube.com/watch?v=clltO-wwfRE',
        'https://www.youtube.com/watch?v=mX8LYc5eaEM',
        'https://www.youtube.com/watch?v=c-VoiE7R9lc',
        'https://www.youtube.com/watch?v=UXdOA2mSG20',
        'https://www.youtube.com/watch?v=tS-R0YlbumQ',
        'https://www.youtube.com/watch?v=tkP0xw_i_Ho',
        'https://www.youtube.com/watch?v=e22HgB_pHxo',
        'https://www.youtube.com/watch?v=1zR3KyVw1-Q',
        'https://www.youtube.com/watch?v=jDXQm5JPEJc',
        'https://www.youtube.com/watch?v=RueNedKCvGA'
    ]
    list_type = 'Euro semi finals 2'
    video_dict2 = create_video_dict(list_type, video_links_list2)
    db_connect.store_data(video_dict2)
    db_connect.read_data()
    print('finished')


# This tells the script to run the main function.
if __name__ == "__main__":
    main()
