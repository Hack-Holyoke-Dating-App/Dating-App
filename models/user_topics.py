class User_Topic:
    def __int__(self, id, user_id, topic, frequency):
        self.id = id
        self.user_id = user_id
        self.topic = topic
        self.frequency = frequency
        
    def to_dict(self):
        return {
                '_id' : self.id,
                'user_id' : self.user_id,
                'topic' : self.topic,
                'frequency' : self.frequency
                }