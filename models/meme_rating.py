class Meme_Rating:
    def __init__(self, id, meme_id, user_id, liked):
        self.id = id
        self.meme_id = meme_id
        self.user_id = user_id
        self.liked = liked

    def to_dict(self):
        d = {
                'meme_id' : self.meme_id,
                'user_id' : self.user_id,
                'liked' : self.liked,
                }

        if (self.id):
            d['_id'] = self.id;

        return d

    def to_str_dict(self):
        d = self.to_dict()

        for key in ['meme_id', 'user_id', '_id']:
            if key in d:
                d[key] = str(d[key])

        return d
