class Coversation:
    def __init__(self, id, user_a_id, user_b_id):
        self.id = id
        self.user_a_id = user_a_id
        self.user_b_id = user_b_id
        
    def to_dict(self):
        d = {
                'user_a_id' : self.user_a_id,
                'user_b_id' : self.user_b_id
                }
        
        if (self.id):
            d['_id'] = self.id
            
        return d
    