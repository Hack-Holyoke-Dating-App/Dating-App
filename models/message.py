class Message:
    def __init__(self, id, conversation_id, sending_user_id, time, text):
        self.id = id
        self.conversation_id = conversation_id
        self.sending_user_id = sending_user_id
        self.time = time
        self.text = text

    @classmethod
    def from_db_document(cls, doc):
        return Message(id=doc['_id'],
                       conversation_id=doc['conversation_id'],
                       sending_user_id=doc['sending_user_id'],
                       time=doc['time'],
                       text=doc['text'])

    def to_dict(self):
        d = {
                'conversation_id': self.conversation_id,
                'sending_user_id' : self.sending_user_id,
                'time' : self.time,
                'text' : self.text
                }

        if (self.id):
            d['_id'] = self.id

        return d
