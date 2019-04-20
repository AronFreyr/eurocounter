

class EuroData:

    def __init__(self, name, views, likes, time, video_type):
        self.name = name
        self.views = views
        self.likes = likes
        self.time = time
        self.video_type = video_type

    def get_name(self):
        return self.name

    def get_views(self):
        return self.views

    def get_likes(self):
        return self.likes

    def get_time(self):
        return self.time

    def get_type(self):
        return self.video_type
