class Message:
    def __init__(self, id, sending_user_id, time, text):
        self.id = id
        self.sending_user_id = sending_user_id
        self.time = time
        self.text = text
    
    def to_dict(self):
        d = {
                'sending_user_id' : self.sending_user_id,
                'time' : self.time,
                'text' : self.text
                }
        
        if (self.id):
            d['_id'] = self.id
            
        return d
    