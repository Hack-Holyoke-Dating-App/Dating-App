class Meme:
    def __init__(self, id):
        self.id = id
        
    def to_dict(self):
        d = { 
                }
        
        if (self.id):
            d['_id'] = self.id
            
        return d
        