

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
