import configparser
from googleapiclient.discovery import build
import datetime

from django.conf import settings


class YoutubeConnect:

    # TODO: Add a function for switching out api keys if one of them returns an error.

    api_key = ''
    api_service_name = ''
    api_version = ''
    api_service = ''
    default_part = ''

    def __init__(self, config_location=None):
        # Get parser object to read config files.
        parser = configparser.ConfigParser(allow_no_value=True)
        if config_location is None:
            parser.read(settings.CONFIG_FILE)  # Running in Django
        else:
            parser.read(config_location)  # Running outside Django
        # There might be multiple YouTube api keys, split them on , to create a list.
        api_key_list = parser['YOUTUBE']['API_KEYS'].split(',')
        # At first try, use the first api key.
        if len(api_key_list) == 1:
            self.api_key = api_key_list
        else:
            self.api_key = api_key_list[0].strip()

        self.api_service_name = parser['YOUTUBE']['SERVICE_NAME']
        self.api_version = parser['YOUTUBE']['VERSION']
        self.default_part = parser['YOUTUBE']['DEFAULT_PART']

        self.api_service = build(self.api_service_name, self.api_version, developerKey=self.api_key)

    def get_single_video_data_raw(self, video_id, part=None):
        """
        Gets the raw video data from a single video, does not trim it or put it in a dict or nothing.
         Just gets the raw data.
         It is recommended to use 'get_single_video_data' or 'get_video_data_for_video_list' instead but if you
         want to get the raw data then it is possible.
        :param video_id: The ID of the video, can either be an ID string or the URL of the video.
        If it is the URL then it will the ID will be gotten from it.
        :param part: The parameter parts of the video data we want.
        It is almost always 'snippet,contentDetails,statistics' but it is possible to use something else.
        Check the YouTube API documentation for what other options are available.
        :return: The raw results of the video data.
        """
        # YouTube needs to know what parts of the data we want to retrieve.
        # If no part was specified, use the default one that we store in the config file.
        if part is None:
            part = self.default_part
        # If the full video URL was used as an ID, just get the ID from the URL.
        if 'youtube' in video_id:
            video_id = self._retrieve_clean_video_id_(video_id)
        results = self.api_service.videos().list(id=video_id, part=part).execute()
        return results

    def get_single_video_data(self, video_id, video_type='Unlisted'):
        """
        Gets data for a single video.
        :param video_id: The ID of the video, if this string is the video URL,
         then the ID will be retrieved from the URL.
        :param video_type: The type of video that we are getting data about.
        This is important for sorting purposes. The default is 'Unlisted' but it is not recommended for use.
        Example: video_type='Euro semi finals 1 2019'
        :return: returns a dictionary with all of the relevant data for the video.
        """
        return self.get_video_data_for_video_list([video_id], video_type)

    def get_video_data_for_video_list(self, video_links_list, list_type='Unlisted'):
        """
        Gets data for a list of videos.
        :param video_links_list: A list of video IDs. If the list has the video URLs instead, then the IDs will
        be retrieved from the URLs.
        :param list_type: The type of video list that we are getting data about.
        This is important for sorting purposes. The default is 'Unlisted' but it is not recommended for use.
        Example: list_type='Euro semi finals 1 2019'
        :return: A dictionary with all of the relevent data for the video list.
        """
        video_dict = {'timestamp': datetime.datetime.now(), 'description': list_type, 'videos': {}}

        for video in video_links_list:
            video_dict['videos'][video] = {}
            # Returns the video ID if 'video' is the URL of the video.
            video_id = self._retrieve_clean_video_id_(video)
            video_results = self.get_single_video_data_raw(video_id)  # Get info on the video.

            video_dict['videos'][video]['views'] = int(video_results['items'][0]['statistics']['viewCount'])
            video_dict['videos'][video]['likes'] = int(video_results['items'][0]['statistics']['likeCount'])
            video_dict['videos'][video]['comments'] = int(video_results['items'][0]['statistics']['commentCount'])
            video_dict['videos'][video]['name'] = video_results['items'][0]['snippet']['title']
        return video_dict

    def _retrieve_clean_video_id_(self, video_string):
        """
        If a full video URL has been used as an ID, we just get the ID from the URL.
        Otherwise if the video ID has been used, we just return it unchanged.
        :param video_string: Either the video ID or the full video URL.
        :return: the ID of the video, retrieved from the URL.
        """
        if 'youtube' in video_string:
            # split the video URL on '=' and use the latter half of the split.
            video_string = video_string.split('=')[1]
            video_string = video_string.split('&')[0]
        return video_string
