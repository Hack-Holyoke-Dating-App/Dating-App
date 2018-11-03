class Meme_Rating:
    def __int__(self, id, meme_id, user_id, liked):
        self.id = id
        self.meme_id = meme_id
        self.user_id = user_id
        self.liked = liked
        
    def to_dict(self):
        return {
                '_id' : self.id,
                'meme_id' : self.meme_id,
                'user_id' : self.user_id,
                'liked' : self.liked,
                }