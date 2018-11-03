class Meme:
    def __init__(self, id):
        self.id = id
        
    def to_dict(self):
        return {
                'id' : self.id
                }
        