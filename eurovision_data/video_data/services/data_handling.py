import logging


logger = logging.getLogger(__name__)


class EuroData:

    def __init__(self, name, views, likes, comments, time, description, dislikes=1, year=None):
        self.name = name
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments
        self.time = time
        self.description = description
        self.year = year

    def get_name(self):
        return self.name

    def get_views(self):
        return self.views

    def get_likes(self):
        return self.likes

    def get_dislikes(self):
        return self.dislikes

    def get_comments(self):
        return self.comments

    def get_time(self):
        return self.time

    def get_description(self):
        return self.description

    def get_proportion(self):
        return self.likes/self.dislikes

    def get_like_percentage(self):
        return self.likes/self.views * 100

    def get_clean_name(self):
        """
        Every year there seems to be a new format for the names of the videos.
        I want them to generally end up like this: COUNTRY - SONG - ARTIST - SEMI_FINAL
        If formatting breaks at any point it should return the name unformatted.
        :return: A nicely formatted name.
        """
        delim = ' - '
        try:
            if self.year == '2023':
                split_name = self.name.split(' | ')
                artist_and_song = split_name[0]
                artist, song_name = artist_and_song.split(' - ')
                song_name = song_name.replace(' (LIVE)', '')
                country = split_name[1][:-3]
                nr_semi = split_name[2]
                if 'First' in nr_semi:
                    nr_semi = 'SF1'
                elif 'Second' in nr_semi:
                    nr_semi = 'SF2'
                clean_name = country + delim + song_name + delim + artist + delim + nr_semi
                return clean_name

            elif self.year == '2017':
                # example: Salvador Sobral - Amar Pelos Dois (Portugal) LIVE at the first Semi-Final
                split_name = self.name.split(' - ')
                artist = split_name[0]
                split_on_left_bracket = split_name[1].split(' (')
                song_name = split_on_left_bracket[0]
                split_on_right_bracket = split_on_left_bracket[1].split(') ')
                country = split_on_right_bracket[0]
                nr_semi = split_on_right_bracket[1]
                if 'first' in nr_semi:
                    nr_semi = 'SF1'
                elif 'second' in nr_semi:
                    nr_semi = 'SF2'
                clean_name = country + delim + song_name + delim + artist + delim + nr_semi
                return clean_name

            else:
                split_name = self.name.split(' - ')
                song_name = split_name[1]
                artist = split_name[0]
                nr_semi = split_name[4]
                if 'First' in nr_semi:
                    nr_semi = 'SF1'
                elif 'Second' in nr_semi:
                    nr_semi = 'SF2'
                year = self.time[:4]
                country = split_name[2]
                if country == 'LIVE':  # Some of the names of the youtube videos have less than perfect formatting.
                    country = split_name[3]
                clean_name = country + delim + song_name + delim + artist + delim + nr_semi# + delim + year
                return clean_name

        except IndexError as e:
            logger.warning(f'Could not get clean name for song: ({self.get_name().encode("utf-8")}), error: {e}')
            # If there is something broken in the formatting then return the 'unclean' name.
            return self.get_name()
