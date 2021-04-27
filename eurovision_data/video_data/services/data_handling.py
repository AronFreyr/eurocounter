

class EuroData:

    def __init__(self, name, views, likes, dislikes, comments, time, description):
        self.name = name
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments
        self.time = time
        self.description = description

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

    def get_clean_name(self):
        try:
            split_name = self.name.split(' - ')
            delim = ' - '
            song_name = split_name[1]
            artist = split_name[0]
            nr_semi = split_name[4]
            if 'First' in nr_semi:
                nr_semi = 'Semi-Final 1'
            elif 'Second' in nr_semi:
                nr_semi = 'Semi-Final 2'
            year = self.time[:4]
            country = split_name[2]
            if country == 'LIVE':  # Some of the names of the youtube videos have less than perfect formatting.
                country = split_name[3]
            clean_name = country + delim + song_name + delim + artist + delim + nr_semi# + delim + year
            return clean_name
        except IndexError as e:
            # TODO: Report and log error in some way
            print(e)
            # If there is something broken in the formatting then return the 'unclean' name.
            return self.get_name()
