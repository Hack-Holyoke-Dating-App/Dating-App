class User_Topics:
    def __init__(self, id, user_id, topics):
        self.id = id
        self.user_id = user_id
        self.topics = topics

    @classmethod
    def from_db_document(cls, doc):
        return User_Topics(id=doc['_id'],
                          user_id=doc['user_id'],
                          topics=doc['topics'])

    def to_dict(self):
        d = {
            'user_id': self.user_id,
            'topics' : self.topics,
        }

        if (self.id):
            d['_id'] = self.id

        return d

    def to_str_dict(self):
        d = self.to_dict()

        d['user_id'] = str(d['user_id'])

        return d
