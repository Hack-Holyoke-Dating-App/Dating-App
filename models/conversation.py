
class Conversation:
    def __init__(self, id, user_a_id, user_b_id):
        self.id = id
        self.user_a_id = user_a_id
        self.user_b_id = user_b_id

    @classmethod
    def from_db_document(cls, doc):
        return Conversation(id=doc['_id'],
                           user_a_id=doc['user_a_id'],
                           user_b_id=doc['user_b_id'])


    def to_dict(self):
        d = {
                'user_a_id' : self.user_a_id,
                'user_b_id' : self.user_b_id
                }

        if (self.id):
            d['_id'] = self.id

        return d

    def to_str_dict(self):
        d = self.to_dict()

        for key in ['_id', 'user_a_id', 'user_b_id']:
            if key in d:
                d[key] = str(d[key])

        return d
