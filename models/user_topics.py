class User_Topic:
    def __int__(self, id, user_id, topics):
        self.id = id
        self.user_id = user_id
        self.topics = topics

    def to_dict(self):
        d = {
            'topics' : self.topics,
            'frequency' : self.frequency
        }

        if (self.id):
            d['_id'] = self.id

        return d
